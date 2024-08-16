import collections
import decimal
import inspect
import math
import pathlib
import types
import typing
import warnings

from functrace.type_hints import *

__all__ = ('FunctionCall', 'ElapsedTime')


class FunctionCall:
    """
    Represents detailed information about a function call for tracing and
    debugging purposes.

    This class provides a comprehensive view of a function invocation,
    including its name, arguments, and contextual information related to the
    call. It is primarily used internally to capture and analyze the details of
    function execution, which can be useful for monitoring, performance
    analysis, and debugging.

    Notes
    -----
    - This class is intended for internal use within the tracing mechanism, and
      users should not instantiate it directly. Instead, instances of
      `FunctionCall` are created and managed by the tracing system to provide
      structured information about function calls and execution contexts.
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
        stack_level: int,
    ) -> None:
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._apply_defaults = apply_defaults
        self._undefined_value = undefined_value
        self._include = include
        self._exclude = exclude
        self._frame = frame
        self._stack_level = stack_level

    def __repr__(self) -> str:
        func = repr(self._func.__name__)
        args = len(self._args)
        kwargs = len(self._kwargs)
        signature = f'func={func}, args={args}, kwargs={kwargs}'
        return f'{self.__class__.__name__}({signature})'

    @property
    def module(self) -> types.ModuleType:
        """
        Retrieve the module in which the function is defined.

        This property provides access to the module object that contains the
        function, allowing you to understand the context in which the function
        resides.

        Returns
        -------
        types.ModuleType
            The module object where the function is defined. This can be useful
            for determining the origin of the function or for module-level
            debugging.
        """
        return inspect.getmodule(object=self._func)

    @property
    def func(self) -> CallableType | types.FunctionType | types.MethodType:
        """
        Retrieve the function object being called.

        This property provides the actual function or method object that was
        invoked, allowing you to access the function's attributes or examine
        its behavior.

        Returns
        -------
        collections.abc.Callable
            The function or method object that was called. This can be used to
            inspect or manipulate the function's attributes or execution
            characteristics.
        """
        return self._func

    @property
    def args(self) -> ArgsType:
        """
        Retrieve the positional arguments passed to the function.

        This property provides a tuple of the positional arguments that were
        supplied when the function was called. It reflects the order and values
        of the arguments.

        Returns
        -------
        tuple
            A tuple containing the positional arguments passed to the function.
            This can be used for inspecting or processing the arguments of the
            function call.
        """
        return self._args

    @property
    def kwargs(self) -> KwargsType:
        """
        Retrieve the keyword arguments passed to the function.

        This property provides a dictionary of the keyword arguments that were
        provided during the function call. It includes both the names and
        values of the keyword arguments.

        Returns
        -------
        dict
            A dictionary containing the keyword arguments passed to the
            function. This allows for detailed inspection and manipulation of
            the function's named parameters.
        """
        return self._kwargs

    @property
    def signature(self) -> inspect.Signature:
        """
        Retrieve the signature of the function.

        This property provides the `inspect.Signature` object of the function,
        which includes information about the function's parameters,
        return type, and other signature-related details.

        Returns
        -------
        inspect.Signature
            The `inspect.Signature` object representing the function's
            signature. This can be used to analyze the function's parameter
            structure and default values.
        """
        return inspect.signature(obj=self._func)

    @property
    def bound_arguments(self) -> inspect.BoundArguments:
        """
        Retrieve the bound arguments for the function call, including any
        default values if applicable.

        This property provides an `inspect.BoundArguments` object that binds
        the positional and keyword arguments to the function's parameters,
        applying default values if `apply_defaults` is set to True.

        Returns
        -------
        inspect.BoundArguments
            The `inspect.BoundArguments` object that shows how the arguments
            from the call are bound to the function's parameters. It includes
            default values if `apply_defaults` is True.
        """
        bound_arguments = self.signature.bind(*self._args, **self._kwargs)
        if self._apply_defaults:
            bound_arguments.apply_defaults()
        return bound_arguments

    @property
    def frame(self) -> types.FrameType:
        """
        Retrieve the frame object where the function is being called.

        This property provides the frame object that represents the context of
        the function call, including information about the call stack and
        execution environment.

        Returns
        -------
        types.FrameType
            The frame object associated with the function call. This can be
            useful for debugging and understanding the execution context of the
            function.
        """
        return self._frame

    @property
    def stack_level(self) -> int:
        """
        Retrieve the stack level for the function call context.

        This property provides the depth of the call stack where the function
        was invoked, which can be particularly useful for logging purposes. It
        helps in understanding the position of the function call within the
        broader call stack.

        Returns
        -------
        int
            The stack level relative to the function's invocation. This value
            is useful for logging and debugging to track where the function
            call occurs in the call stack.

        Notes
        -----
        - This value can be used to log the stack level, aiding in tracing and
          diagnosing function call sequences and their context within the
          application.
        - Higher stack levels indicate deeper positions in the call stack,
          which can assist in understanding complex call chains.
        """
        return self._stack_level + 2

    def format(
        self,
        pattern: str = '{name}({params})',
        *,
        association: str = '=',
        separator: str = ', ',
    ) -> str:
        """
        Generates a string representation of the function call based on the
        specified pattern.

        This method formats the details of the function call according to the
        provided pattern and customization options, allowing for flexible
        and informative string representations of function invocations.

        Parameters
        ----------
        pattern : str, default '{name}({params})'
            The format string used to represent the function call. It supports
            the following placeholders:

            - `{path}` : The file path where the function is defined.
            - `{file}` : The file name where the function is defined, including
              the extension
            - `{module}` : The module name where the function is located.
            - `{name}` : The function name.
            - `{qualname}` : The fully qualified name of the function
              (including class name if applicable).
            - `{line}` : The line number where the function call occurs.
            - `{params}` : A string representing the function's parameters and
              their values.
        association : str, default '='
            The string used to separate argument names from their values in the
            formatted representation.
        separator : str, default ', '
            The string used to separate multiple arguments in the formatted
            representation.

        Returns
        -------
        str
            A formatted string representing the function call, customized
            according to the specified pattern, association, and separator.

        Examples
        --------
        Given the following setup:

        >>> # /home/user/python/project/module/file.py
        ...
        >>> from functrace import trace
        ...
        >>> class MyClass:
        ...     @trace(callback=...)
        ...     def my_func(self, a, b):
        ...         ...
        ...
        >>> MyClass().my_func(123, 'abc')

        Formatting the function name and its parameters:

        >>> self.format('{name}({params})')
        'my_func(a=123, b='abc')'

        Displaying the file path and line number:

        >>> self.format('{path}, line: {line}')
        '/home/user/python/project/module/file.py, line: 10'

        Showing the file name where the function is defined:

        >>> self.format('filename: {file}')
        'filename: file.py'

        Including the module name and fully qualified function name:

        >>> self.format('{module} - {qualname}')
        'module.file - MyClass.my_func'

        Customizing the parameter representation with a different separator and
        association:

        >>> self.format('{params}', association=': ', separator=' | ')
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
        if '{absolute_path}' in pattern:
            old, new = '{absolute_path}', '{path}'
            pattern = pattern.replace(old, new)
            warnings.warn(
                message=f'use {new} instead of {old}',
                category=DeprecationWarning,
                stacklevel=2,
            )
        if '{module_name}' in pattern:
            old, new = '{module_name}', '{module}'
            pattern = pattern.replace(old, new)
            warnings.warn(
                message=f'use {new} instead of {old}',
                category=DeprecationWarning,
                stacklevel=2,
            )
        if '{function_name}' in pattern:
            old, new = '{function_name}', '{name}'
            pattern = pattern.replace(old, new)
            warnings.warn(
                message=f'use {new} instead of {old}',
                category=DeprecationWarning,
                stacklevel=2,
            )
        if '{function_qualified_name}' in pattern:
            old, new = '{function_qualified_name}', '{qualname}'
            pattern = pattern.replace(old, new)
            warnings.warn(
                message=f'use {new} instead of {old}',
                category=DeprecationWarning,
                stacklevel=2,
            )
        if '{line_number}' in pattern:
            old, new = '{line_number}', '{line}'
            pattern = pattern.replace(old, new)
            warnings.warn(
                message=f'use {new} instead of {old}',
                category=DeprecationWarning,
                stacklevel=2,
            )
        if '{arguments}' in pattern:
            old, new = '{arguments}', '{params}'
            pattern = pattern.replace(old, new)
            warnings.warn(
                message=f'use {new} instead of {old}',
                category=DeprecationWarning,
                stacklevel=2,
            )
        return pattern.format(
            path=module.__file__,
            file=pathlib.Path(module.__file__).name,
            module=module.__name__,
            name=self._func.__name__,
            qualname=self._func.__qualname__,
            line=inspect.getlineno(frame=self._frame),
            params=separator.join(
                f'{key}{association}{value!r}'
                for key, value in arguments.items()
            )
        )


class ElapsedTime:
    """
        Represents elapsed time in seconds, with support for multiple time
        units and human-readable formatting.

    This class provides a structured way to represent and manage elapsed time.
    It is primarily used internally to track the duration of function
    executions within the tracing mechanism. This includes formatting elapsed
    time for monitoring and debugging purposes.

    Notes
    -----
    - This class is intended for internal use within the tracing system. Users
      should not instantiate it directly. Instead, instances of `ElapsedTime`
      are created and managed by the tracing mechanism to handle and format
      time-related information.
    """
    def __init__(self, seconds: float) -> None:
        self._seconds = seconds

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(seconds={self._seconds})'

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
        decimals=2,
        trailing_zeros=False,
        time_parts: bool = False,
        separator: str = ', ',
        ignore_zeros: bool = True,
    ) -> str | None:
        """
        Convert the elapsed time to a human-readable string representation.

        Parameters
        ----------
        decimals : int, default 2
            Number of decimal places to display for the elapsed time. This
            parameter is applicable when `time_parts` is `False` or when the
            elapsed time is less than 1 nanosecond.
        trailing_zeros : bool, default False
            Determines whether to include trailing zeros after the decimal
            point. If `True`, trailing zeros will be included in the output; if
            `False`, they will be removed.
        time_parts : bool, default False
            If `True`, the elapsed time is broken down into its component units
            (e.g., hours, minutes, seconds). If `False`, the elapsed time is
            displayed as a single unit with the specified decimal precision.
        separator : str, default ', '
            The string used to separate different units in the formatted output
            when `time_parts` is `True`
        ignore_zeros : bool, default True
            **Deprecated**. When set to `True`, zero-value units are excluded
            from the formatted output. This option is no longer recommended, as
            it may be removed in future versions.

        Returns
        -------
        str or None
            A formatted string representing the elapsed time. If the elapsed
            time is `float('nan')`, the method returns `None`.

        Examples
        --------
        Assume the elapsed time was 75 seconds:

        >>> self.seconds
        75.0
        >>> self.minutes
        1.25
        >>> self.format(decimals=2)
        '1.25 minutes'
        >>> self.format(decimals=1)
        '1.3 minutes'
        >>> self.format(decimals=0)
        '1 minute'

        Assume the elapsed time was 60 seconds:

        >>> self.seconds
        60.0
        >>> self.minutes
        1.0
        >>> self.format(trailing_zeros=False)
        '1 minute'
        >>> self.format(trailing_zeros=True)
        '1.00 minute'

        Assume the elapsed time was 3723 seconds:

        >>> self.seconds
        3723.0
        >>> self.minutes
        62.05
        >>> self.format(time_parts=True)
        '1 hour, 2 minutes, 3 seconds'
        >>> self.format(time_parts=True, separator=' | ')
        '1 hour | 2 minutes | 3 seconds'
        """
        if math.isnan(self._seconds):
            return
        value, unit = self._single_unit()
        if time_parts:
            parts = self._multi_units(ignore_zeros=ignore_zeros)
            result = separator.join(f'{value} {unit}' for value, unit in parts)
            if result:
                return result
        value = self._round(
            value=value,
            decimals=decimals,
            trailing_zeros=trailing_zeros,
        )
        return f'{value} {unit}'

    @staticmethod
    def _round(value: float, decimals: int, trailing_zeros: bool) -> str:
        result = decimal.Decimal(
            value=value,
        ).quantize(
            exp=decimal.Decimal(value=f'1e-{decimals}'),
            rounding=decimal.ROUND_HALF_UP,
        )
        if not trailing_zeros:
            result = str(result).rstrip('0').rstrip('.')
        return result

    def _single_unit(self) -> tuple[float, str]:
        if (value := self.weeks) >= 1:
            unit = f'week{'' if value == 1 else 's'}'
        elif (value := self.days) >= 1:
            unit = f'day{'' if value == 1 else 's'}'
        elif (value := self.hours) >= 1:
            unit = f'hour{'' if value == 1 else 's'}'
        elif (value := self.minutes) >= 1:
            unit = f'minute{'' if value == 1 else 's'}'
        elif (value := self.seconds) >= 1:
            unit = f'second{'' if value == 1 else 's'}'
        elif (value := self.milliseconds) >= 1:
            unit = f'millisecond{'' if value == 1 else 's'}'
        elif (value := self.microseconds) >= 1:
            unit = f'microsecond{'' if value == 1 else 's'}'
        else:
            value = self.nanoseconds
            unit = f'nanosecond{'' if value == 1 else 's'}'
        return value, unit

    def _multi_units(self, ignore_zeros: bool) -> tuple[tuple[int, str], ...]:
        weeks = int(self._seconds // 604800)
        days = int(self._seconds % 604800 // 86400)
        hours = int(self._seconds % 86400 // 3600)
        minutes = int(self._seconds % 3600 // 60)
        seconds = int(self._seconds % 60)
        milliseconds = int(self._seconds * 1e3 % 1e3)
        microseconds = int(self._seconds * 1e6 % 1e3)
        nanoseconds = int(self._seconds * 1e9 % 1e3)
        parts = (
            (weeks, f'week{'' if weeks == 1 else 's'}'),
            (days, f'day{'' if days == 1 else 's'}'),
            (hours, f'hour{'' if hours == 1 else 's'}'),
            (minutes, f'minute{'' if minutes == 1 else 's'}'),
            (seconds, f'second{'' if seconds == 1 else 's'}'),
            (milliseconds, f'millisecond{'' if milliseconds == 1 else 's'}'),
            (microseconds, f'microsecond{'' if microseconds == 1 else 's'}'),
            (nanoseconds, f'nanosecond{'' if nanoseconds == 1 else 's'}'),
        )
        if ignore_zeros:
            parts = tuple((value, unit) for value, unit in parts if value)
        else:
            warnings.warn(
                message='ignore_zeros is deprecated',
                category=DeprecationWarning,
                stacklevel=2,
            )
        return parts
