import inspect
import math
import types
import typing
import warnings

from functrace.type_hints import *

__all__ = ('FunctionCall', 'ElapsedTime')


class FunctionCall:
    """
    Represents a function call, encapsulating information about the function's
    execution, including its name, arguments, and the call pattern.

    Parameters
    ----------
    func : callable
        The function object being called.
    args : tuple
        Positional arguments passed to the function.
    kwargs : dict
        Keyword arguments passed to the function.
    apply_defaults : bool
        Whether to apply default values for missing arguments.
    undefined_value : typing.Any
        Value used to represent undefined arguments.
    include : str or tuple of str or None
        Specifies which arguments to include in the call representation.
        If None, all arguments are included.
    exclude : str or tuple of str or None
        Specifies which arguments to exclude from the call representation.
        If None, no arguments are excluded.
    frame : types.FrameType
        The frame object where the function is being called.
    """
    def __init__(
        self,
        func: CallableType,
        args: ArgsType,
        kwargs: KwargsType,
        apply_defaults: bool,
        undefined_value: typing.Any,
        include: str | tuple[str, ...] | None,
        exclude: str | tuple[str, ...] | None,
        frame: types.FrameType,
    ) -> None:
        self._function = func
        self._args = args
        self._kwargs = kwargs
        self._apply_defaults = apply_defaults
        self._undefined_value = undefined_value
        self._include = include
        self._exclude = exclude
        self._frame = frame

    @property
    def module(self) -> types.ModuleType:
        """
        Get the module in which the function is defined.

        Returns
        -------
        types.ModuleType
            The module object containing the function.
        """
        return inspect.getmodule(object=self._function)

    @property
    def func(self) -> CallableType | types.FunctionType | types.MethodType:
        """
        Get the function object being called.

        Returns
        -------
        callable
            The function or method object.
        """
        return self._function

    @property
    def args(self) -> ArgsType:
        """
        Get the positional arguments passed to the function.

        Returns
        -------
        tuple
            A tuple of positional arguments.
        """
        return self._args

    @property
    def kwargs(self) -> KwargsType:
        """
        Get the keyword arguments passed to the function.

        Returns
        -------
        dict
            A dictionary of keyword arguments.
        """
        return self._kwargs

    @property
    def signature(self) -> inspect.Signature:
        """
        Get the signature of the function.

        Returns
        -------
        inspect.Signature
            The signature object of the function.
        """
        return inspect.signature(obj=self._function)

    @property
    def bound_arguments(self) -> inspect.BoundArguments:
        """
        Get the bound arguments for the function call, including default values
        if applicable.

        Returns
        -------
        inspect.BoundArguments
            The bound arguments, including any defaults applied if
            `apply_defaults` is True.
        """
        bound_arguments = self.signature.bind(*self._args, **self._kwargs)
        if self._apply_defaults:
            bound_arguments.apply_defaults()
        return bound_arguments

    @property
    def frame(self) -> types.FrameType:
        """
        Get the frame object where the function is being called.

        Returns
        -------
        types.FrameType
            The frame object associated with the function call.
        """
        return self._frame

    def format(
        self,
        pattern: str = '{function_name}({arguments})',
        *,
        association: str = '=',
        separator: str = ', ',
    ) -> str:
        """
        Generate a string representation of a function call based on the
        provided pattern.

        Parameters
        ----------
        pattern : str, default '{function_name}({arguments})'
            String pattern to format the function call. Supports placeholders:
            - {absolute_path}
            - {module_name}
            - {function_name}
            - {function_qualified_name}
            - {line_number}
            - {arguments}
        association : str, default '='
            String used to associate argument names with their values.
        separator : str, default ', '
            String used to separate different arguments.

        Returns
        -------
        str
            A formatted string representing the function call with the
            specified pattern.

        Examples
        --------
        >>> self.format()
        'func(a=123, b='abc')'

        >>> self.format('{absolute_path}, line: {line_number}')
        '/home/user/python/project/module/file.py, line: 100'

        >>> self.format('{module_name} - {function_qualified_name}')
        'module.file - Class.func'

        >>> self.format('{arguments}', association=': ', separator=' | ')
        'a: 123 | b: 'abc''
        """
        module = self.module
        signature = self.signature
        bound_arguments = self.bound_arguments
        parameters = signature.parameters
        arguments = bound_arguments.arguments
        if self._include is None:
            include = set(parameters)
        elif isinstance(self._include, str):
            include = {self._include}
        else:
            include = set(self._include)
        if self._exclude is None:
            exclude = set()
        elif isinstance(self._exclude, str):
            exclude = {self._exclude}
        else:
            exclude = set(self._exclude)
        selected = include - exclude
        arguments = {
            parameter: arguments.get(parameter, self._undefined_value)
            for parameter in filter(selected.__contains__, parameters)
        }
        return pattern.format(
            absolute_path=module.__file__,
            module_name=module.__name__,
            function_name=self._function.__name__,
            function_qualified_name=self._function.__qualname__,
            line_number=inspect.getlineno(frame=self._frame),
            arguments=separator.join(
                f'{key}{association}{value!r}'
                for key, value in arguments.items()
            )
        )


class ElapsedTime:
    """
    Represents elapsed time in seconds with support for multiple time units and
    human-readable formatting.

    Parameters
    ----------
    seconds : float
        The elapsed time in seconds.
    """
    def __init__(self, seconds: float) -> None:
        self._seconds = seconds

    @property
    def elapsed_time(self) -> float:
        warnings.warn(
            message='use .seconds instead of .elapsed_time',
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.seconds

    @property
    def nanoseconds(self) -> float:
        """
        Calculate the elapsed time in nanoseconds.

        Returns
        -------
        float
            Elapsed time expressed in nanoseconds.
        """
        return self._seconds * 1e9

    @property
    def microseconds(self) -> float:
        """
        Calculate the elapsed time in microseconds.

        Returns
        -------
        float
            Elapsed time expressed in microseconds.
        """
        return self._seconds * 1e6

    @property
    def milliseconds(self) -> float:
        """
        Calculate the elapsed time in milliseconds.

        Returns
        -------
        float
            Elapsed time expressed in milliseconds.
        """
        return self._seconds * 1e3

    @property
    def seconds(self) -> float:
        """
        Calculate the elapsed time in seconds.

        Returns
        -------
        float
            Total elapsed time in seconds.
        """
        return self._seconds

    @property
    def minutes(self) -> float:
        """
        Calculate the elapsed time in minutes.

        Returns
        -------
        float
            Elapsed time expressed in minutes.
        """
        return self._seconds / 60

    @property
    def hours(self) -> float:
        """
        Calculate the elapsed time in hours.

        Returns
        -------
        float
            Elapsed time expressed in hours.
        """
        return self._seconds / 3600

    @property
    def days(self) -> float:
        """
        Calculate the elapsed time in days.

        Returns
        -------
        float
            Elapsed time expressed in days.
        """
        return self._seconds / 86400

    @property
    def weeks(self) -> float:
        """
        Calculate the elapsed time in weeks.

        Returns
        -------
        float
            Elapsed time expressed in weeks.
        """
        return self._seconds / 604800

    def format(
        self,
        *,
        ignore_zeros: bool = True,
        separator: str = ', ',
    ) -> str | None:
        """
        Convert the elapsed time to a human-readable string representation.

        Parameters
        ----------
        ignore_zeros : bool, default True
            If True, zero-value units are omitted from the resulting string.
        separator : str, default ', '
            String used to separate different units in the resulting string.

        Returns
        -------
        str or None
            A human-readable string representation of the elapsed time,
            formatted according to the `ignore_zeros` and `separator`
            parameters.
            Returns `None` if the elapsed time is `float('nan')`.

        Examples
        --------
        >>> self.format()
        '2 minutes, 3 seconds'

        >>> self.format(ignore_zeros=False)
        '0 weeks, 0 days, 0 hours, 2 minutes, 3 seconds, '0 milliseconds, 0 microseconds, 0 nanoseconds'

        >>> self.format(separator=' | ')
        '2 minutes | 3 seconds'
        """
        if math.isnan(self._seconds):
            return
        weeks = int(self.elapsed_time // 604800)
        days = int(self.elapsed_time % 604800 // 86400)
        hours = int(self.elapsed_time % 86400 // 3600)
        minutes = int(self.elapsed_time % 3600 // 60)
        seconds = int(self.elapsed_time % 60)
        milliseconds = int(self.elapsed_time * 1e3 % 1e3)
        microseconds = int(self.elapsed_time * 1e6 % 1e3)
        nanoseconds = int(self.elapsed_time * 1e9 % 1e3)
        parts = (
            (weeks, 'week' + ('' if weeks == 1 else 's')),
            (days, 'day' + ('' if days == 1 else 's')),
            (hours, 'hour' + ('' if hours == 1 else 's')),
            (minutes, 'minute' + ('' if minutes == 1 else 's')),
            (seconds, 'second' + ('' if seconds == 1 else 's')),
            (milliseconds, 'millisecond' + ('' if milliseconds == 1 else 's')),
            (microseconds, 'microsecond' + ('' if microseconds == 1 else 's')),
            (nanoseconds, 'nanosecond' + ('' if nanoseconds == 1 else 's')),
        )
        if ignore_zeros:
            parts = tuple((value, unit) for value, unit in parts if value)
        string = separator.join(f'{value} {unit}' for value, unit in parts)
        return string or '0 nanoseconds'
