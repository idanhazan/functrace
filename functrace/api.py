from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial, wraps
from inspect import currentframe
from time import time
from traceback import format_exc
from typing import TYPE_CHECKING

from functrace.utilities import FunctionCall, ElapsedTime

if TYPE_CHECKING:
    from typing import Any, Callable, Optional, Tuple, Union

__all__ = ('TraceResult', 'trace')


@dataclass(frozen=True)
class TraceResult:
    """
    Captures detailed execution metadata for a traced function,
    including performance metrics, arguments, return values, and exceptions.

    Attributes
    ----------
    function_call : FunctionCall
        Contains details about the function call, including name and arguments.
    elapsed_time : ElapsedTime
        Represents the time taken for the function execution.
    is_started : bool
        Indicates if the function has started.
    is_completed : bool
        Indicates if the function has completed.
    is_failed : bool
        Indicates if the function has failed.
    returned_value : Any, optional
        The return value of the function.
    exception : Exception, optional
        The exception raised during function execution (if any).
    traceback : str, optional
        The traceback of the exception (if any).

    Notes
    -----
    Only one of `is_started`, `is_completed`, and `is_failed` can be True.
    """
    @staticmethod
    def empty_elapsed_time():
        return ElapsedTime()

    function_call: FunctionCall
    elapsed_time: ElapsedTime = field(default_factory=empty_elapsed_time)
    is_started: bool = field(default=False)
    is_completed: bool = field(default=False)
    is_failed: bool = field(default=False)
    returned_value: Any = field(default=None)
    exception: Optional[Exception] = field(default=None)
    traceback: Optional[str] = field(default=None)


def trace(
    callback: Callable[[TraceResult], None],
    *,
    apply_defaults: bool = False,
    undefined_value: Any = None,
    include: Optional[Union[str, Tuple[str, ...]]] = None,
    exclude: Optional[Union[str, Tuple[str, ...]]] = None,
) -> Callable[..., Any]:
    """
    Creates a decorator that traces function execution and invokes a callback.

    Parameters
    ----------
    callback : callable
        A callable that will be invoked with a :class:`TraceResult` instance at
        the beginning and end of the traced function's execution.
    apply_defaults : bool, default False
        If True, applies default values to missing function arguments.
        Otherwise, missing arguments are represented as `undefined_value`.
    undefined_value : Any, default None
        The value to return for missing arguments.
    include : str, tuple of str, default None
        Select parameters to include in the TracerResult.
        If None, all parameters are included.
    exclude : str, tuple of str, default None
        Select parameters to exclude from the TracerResult.
        If None, no parameters are excluded.

    Returns
    -------
    callable
        A decorator that wraps the traced function.

    Notes
    -----
    The decorator invokes the callback twice: once with the `is_started` flag,
    and again with either the `is_completed` or `is_failed` flag accordingly.

    Examples
    --------
    Defining a callback function:

    >>> from functrace import TraceResult, trace
    ...
    >>> def trace_callback(result: TraceResult) -> None:
    ...     function_call = result.function_call.format()
    ...     elapsed_time = result.elapsed_time.format()
    ...     returned_value = repr(result.returned_value)
    ...     exception = repr(result.exception)
    ...     parts = [function_call]
    ...     if result.is_started:
    ...         parts.extend(['Started'])
    ...     if result.is_completed:
    ...         parts.extend(['Completed', elapsed_time, returned_value])
    ...     if result.is_failed:
    ...         parts.extend(['Failed', elapsed_time, exception])
    ...     message = ' | '.join(parts)
    ...     print(message)

    Minimal example:

    >>> @trace(callback=trace_callback)
    ... def func(a, b)
    ...     return a / b
    ...
    >>> func(1, 2)
    func(a=1, b=2) | Started
    func(a=1, b=2) | Completed | 1 microsecond, 200 nanoseconds | 0.5

    Minimal example (raised exception):

    >>> @trace(callback=trace_callback)
    ... def func(a, b)
    ...     return a / b
    ...
    >>> func(1, 0)
    func(a=1, b=2) | Started
    func(a=1, b=2) | Failed | 1 microsecond, 200 nanoseconds | ZeroDivisionError('division by zero')

    Applying defaults:

    >>> @trace(callback=trace_callback, apply_defaults=False)
    ... def func(a=1, b=2)
    ...     return a, b
    ...
    >>> func()
    func(a=None, b=None) | Started
    func(a=None, b=None) | Completed | 1 microsecond, 200 nanoseconds | (1, 2)

    >>> @trace(callback=trace_callback, apply_defaults=True)
    ... def func(a=1, b=2)
    ...     return a, b
    ...
    >>> func()
    func(a=1, b=2) | Started
    func(a=1, b=2) | Completed | 1 microsecond, 200 nanoseconds | (1, 2)

    Using undefined value:

    >>> @trace(callback=trace_callback, undefined_value=None)
    ... def func(a=1, b=None)
    ...     return a, b
    ...
    >>> func(b=None)
    func(a=None, b=None) | Started
    func(a=None, b=None) | Completed | 1 microsecond, 200 nanoseconds | (1, None)

    >>> @trace(callback=trace_callback, undefined_value=Ellipsis)
    ... def func(a=1, b=None)
    ...     return a, b
    ...
    >>> func(b=None)
    func(a=Ellipsis, b=None) | Started
    func(a=Ellipsis, b=None) | Completed | 1 microsecond, 200 nanoseconds | (1, None)

    Including one parameter:

    >>> @trace(callback=trace_callback, include='b')
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(b=2) | Started
    func(b=2) | Completed | 1 microsecond, 200 nanoseconds | 6

    Including many parameters:

    >>> @trace(callback=trace_callback, include=('a', 'c'))
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(a=1, c=3) | Started
    func(a=1, c=3) | Completed | 1 microsecond, 200 nanoseconds | 6

    Excluding one parameter:

    >>> @trace(callback=trace_callback, exclude='b')
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(a=1, c=3) | Started
    func(a=1, c=3) | Completed | 1 microsecond, 200 nanoseconds | 6

    Excluding many parameters:

    >>> @trace(callback=trace_callback, exclude=('a', 'c'))
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(b=2) | Started
    func(b=2) | Completed | 1 microsecond, 200 nanoseconds | 6
    """
    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(wrapped=function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            partial_result = partial(
                TraceResult,
                function_call=FunctionCall(
                    function=function,
                    args=args,
                    kwargs=kwargs,
                    apply_defaults=apply_defaults,
                    undefined_value=undefined_value,
                    include=include,
                    exclude=exclude,
                    frame=currentframe().f_back,
                ),
            )
            tracer_result = partial_result(is_started=True)
            callback(tracer_result)
            start_time = time()
            try:
                result = function(*args, **kwargs)
                end_time = time()
                elapsed_time = ElapsedTime(elapsed_time=end_time - start_time)
                tracer_result = partial_result(
                    is_completed=True,
                    elapsed_time=elapsed_time,
                    returned_value=result,
                )
                callback(tracer_result)
                return result
            except Exception as exception:
                end_time = time()
                elapsed_time = ElapsedTime(elapsed_time=end_time - start_time)
                tracer_result = partial_result(
                    is_failed=True,
                    elapsed_time=elapsed_time,
                    exception=exception,
                    traceback=format_exc(),
                )
                callback(tracer_result)
                raise exception
        return wrapper
    return decorator
