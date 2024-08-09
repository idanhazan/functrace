from __future__ import annotations

from inspect import getlineno, getmodule, signature
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import FunctionType, MethodType, FrameType, ModuleType
    from typing import Any, Callable, Dict, Optional, Tuple, Union

__all__ = ('FunctionCall', 'ElapsedTime')


class FunctionCall:
    """
    Represents a function call, encapsulating information about the function's
    execution, including its name, arguments, and the call pattern.
    """
    def __init__(
        self,
        function: Callable[..., Any],
        args: Tuple[str, ...],
        kwargs: Dict[str, Any],
        apply_defaults: bool,
        undefined_value: Any,
        include: Optional[Union[str, Tuple[str, ...]]],
        exclude: Optional[Union[str, Tuple[str, ...]]],
        frame: FrameType,
    ) -> None:
        self._function = function
        self._args = args
        self._kwargs = kwargs
        self._apply_defaults = apply_defaults
        self._undefined_value = undefined_value
        self._include = include
        self._exclude = exclude
        self._frame = frame

    @property
    def module(self) -> ModuleType:
        return getmodule(object=self._function)

    @property
    def frame(self) -> FrameType:
        return self._frame

    @property
    def func(self) -> Union[Callable[..., Any], FunctionType, MethodType]:
        return self._function

    @property
    def args(self) -> Tuple[Any, ...]:
        return self._args

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

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
        module = getmodule(object=self._function)
        function_signature = signature(obj=self._function)
        bound_arguments = function_signature.bind(*self._args, **self._kwargs)
        if self._apply_defaults:
            bound_arguments.apply_defaults()
        function_parameters = function_signature.parameters
        function_arguments = bound_arguments.arguments
        if self._include is None:
            include = set(function_signature.parameters)
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
            parameter: function_arguments.get(parameter, self._undefined_value)
            for parameter in filter(selected.__contains__, function_parameters)
        }
        return pattern.format(
            absolute_path=module.__file__,
            module_name=module.__name__,
            function_name=self._function.__name__,
            function_qualified_name=self._function.__qualname__,
            line_number=getlineno(frame=self._frame),
            arguments=separator.join(
                f'{key}{association}{value!r}'
                for key, value in arguments.items()
            )
        )


class ElapsedTime:
    """
    A class to represent elapsed time in seconds and provide various formats.

    Attributes
    ----------
    elapsed_time : float
        The elapsed time in seconds.
    """
    def __init__(self, elapsed_time: Optional[float] = None) -> None:
        self.elapsed_time = elapsed_time

    def format(
        self,
        *,
        ignore_zeros: bool = True,
        separator: str = ', ',
    ) -> Optional[str]:
        """
        Convert the elapsed time to a human-readable string representation.

        Parameters
        ----------
        ignore_zeros : bool, default True
            If True, zero-value units are omitted from the resulting string.
        separator : str, default ', '
            String used to separate different units in the resulting string.

        Examples
        --------
        >>> self.format()
        '2 minutes, 3 seconds'

        >>> self.format(ignore_zeros=False)
        '0 weeks, 0 days, 0 hours, 2 minutes, 3 seconds, '0 milliseconds, 0 microseconds, 0 nanoseconds'

        >>> self.format(separator=' | ')
        '2 minutes | 3 seconds'
        """
        if self.elapsed_time is None:
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
