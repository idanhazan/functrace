import collections
import dataclasses
import functools
import inspect
import time
import traceback
import typing

from functrace.type_hints import *
from functrace.utilities import FunctionCall, ElapsedTime

__all__ = ('TraceResult', 'trace')


@dataclasses.dataclass(frozen=True)
class TraceResult:
    """
    Captures comprehensive metadata for a traced function, including
    performance metrics, input arguments, return values, and any exceptions
    encountered.

    This class provides a detailed snapshot of a function's execution,
    facilitating in-depth tracing and analysis. It includes information about
    the function's start, completion, and any errors that may have occurred,
    along with performance timing.

    Key features include:

    - **Detailed function call information**: Provides specifics about the
      function name, arguments, and other relevant metadata.
    - **Timing metrics for execution duration**: Measures the time taken for
      the function to execute, allowing performance analysis.
    - **Status indicators for function execution**: Flags to indicate whether
      the function has started, completed successfully, or failed.
    - **Captured return values and exceptions**: Records the function's return
      value upon successful completion or any exceptions raised during
      execution.

    This enables robust monitoring and debugging, offering insights into both
    successful executions and failures.

    Attributes
    ----------
    function_call : FunctionCall
        Contains details about the function call, such as the function's name,
        arguments, and other relevant metadata.
    elapsed_time : ElapsedTime
        Represents the duration of the function's execution. This attribute
        captures the time taken from the start to the end of the function, but
        it is only measured when the function has completed or failed.

        Specifically:

        - If `is_completed` is True or `is_failed` is True, `elapsed_time`
          represents the total execution time of the function from start to
          finish.
        - If `is_started` is True, indicating that the function is still in
          progress, `elapsed_time` will be set to NaN (Not a Number) to
          indicate that the time duration is not applicable or unavailable.

        This design ensures that `elapsed_time` accurately reflects the
        execution duration only when the function has fully completed or
        failed, providing relevant timing information.
    is_started : bool
        Indicates whether the function has started execution. This is set to
        True when the function begins execution.
    is_completed : bool
        Indicates whether the function has completed execution successfully.
        This is set to True when the function completes without raising an
        exception.
    is_failed : bool
        Indicates whether the function has failed during execution. This is set
        to True if the function raises an exception.
    returned_value : Any, optional
        The value returned by the function upon successful completion. This
        attribute is set only if `is_completed` is True. If the function does
        not return a value, this attribute will be None.
    exception : Exception, optional
        The exception raised during function execution, if any. This attribute
        is set only if `is_failed` is True. It provides details about the error
        encountered during execution.
    traceback : str, optional
        The traceback of the exception, if any. This provides a string
        representation of the stack trace where the exception occurred. This
        attribute is only set if `is_failed` is True and an exception was
        raised.

    Notes
    -----
    - Only one of `is_started`, `is_completed`, and `is_failed` can be True at
      any given time, reflecting the mutually exclusive states of function
      execution.
    - The `function_call` attribute is an instance of `FunctionCall` and
      contains detailed information about the function invocation, including
      its name and arguments.
    - The `elapsed_time` is represented by an `ElapsedTime` object, which
      provides a standardized way to measure and report time intervals.
    """
    @staticmethod
    def unmeasured():
        return ElapsedTime(seconds=float('nan'))

    function_call: FunctionCall
    elapsed_time: ElapsedTime = dataclasses.field(default_factory=unmeasured)
    is_started: bool = dataclasses.field(default=False)
    is_completed: bool = dataclasses.field(default=False)
    is_failed: bool = dataclasses.field(default=False)
    returned_value: typing.Any = dataclasses.field(default=None)
    exception: Exception | None = dataclasses.field(default=None)
    traceback: str | None = dataclasses.field(default=None)


def trace(
    callback: collections.abc.Callable[[TraceResult], None],
    *,
    apply_defaults: bool = False,
    undefined_value: typing.Any = None,
    include: str | tuple[str, ...] | None = None,
    exclude: str | tuple[str, ...] | None = None,
    stack_level: int = 1,
) -> CallableType:
    """
    Creates a decorator that provides detailed tracing of function execution
    and invokes a callback with metadata about the execution. This decorator is
    useful for monitoring, debugging, and performance analysis.

    Parameters
    ----------
    callback : collections.abc.Callable
        A callable that will be invoked with a `TraceResult` instance at the
        beginning and end of the traced function's execution. The `TraceResult`
        provides information about the function call, such as parameters,
        return value, and execution status. This callback is useful for
        logging, monitoring, or other forms of tracing.
    apply_defaults : bool, default False
        If True, the decorator will apply default values to any missing
        arguments when creating the `TraceResult`. This means that if a
        function is called with fewer arguments than it expects, the missing
        arguments will be filled with their default values as defined in the
        function signature. If False, missing arguments are represented as
        `undefined_value` in the `TraceResult`.
    undefined_value : Any, default None
        The value to use for arguments that are missing or not provided if
        `apply_defaults` is set to False. This allows customization of how
        missing or undefined arguments are represented in the `TraceResult`.
        For example, you might use a specific placeholder object or value to
        indicate that an argument was not supplied.
    include : str, tuple of str, default None
        A selection of parameter names to include in the `TraceResult`. If set
        to None, all parameters of the traced function are included. This
        allows for filtering the parameters that are captured and reported by
        the callback. If specified, only the parameters listed will be included
        in the trace output, while others will be omitted.
    exclude : str, tuple of str, default None
        A selection of parameter names to exclude from the `TraceResult`. If
        set to None, no parameters are excluded, and all are included. This
        allows for excluding certain parameters from the trace output. For
        instance, you might exclude large data structures or sensitive
        information that should not be included in the trace.
    stack_level : int, default 1
        Specifies the number of stack frames to go back when tracing the
        function's execution. A stack level of 1 means inspecting the immediate
        caller's frame, a level of 2 means inspecting the caller of the
        immediate caller, and so on. This parameter controls how deep in the
        call stack the tracing occurs.

    Returns
    -------
    collections.abc.Callable
        A decorator that wraps the traced function. This decorator adds tracing
        functionality to the function, invoking the specified callback with
        `TraceResult` instances before and after the function execution.

    Notes
    -----
    - The `callback` function is invoked twice: once with an `is_started` flag
      before the function begins execution, and once with either `is_completed`
      or `is_failed` flag after the function finishes or raises an exception.
    - The `include` and `exclude` parameters provide fine-grained control over
      which function parameters are captured in the trace output.
    - The `stack_level` parameter helps in tracing functions through different
      layers of abstraction by adjusting how deep in the call stack the tracing
      occurs.

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
    func(a=1, b=2) | Completed | X seconds | 0.5

    Minimal example (raised exception):

    >>> @trace(callback=trace_callback)
    ... def func(a, b)
    ...     return a / b
    ...
    >>> func(1, 0)
    func(a=1, b=2) | Started
    func(a=1, b=2) | Failed | X seconds | ZeroDivisionError('division by zero')

    Applying defaults:

    >>> @trace(callback=trace_callback, apply_defaults=False)
    ... def func(a=1, b=2)
    ...     return a, b
    ...
    >>> func()
    func(a=None, b=None) | Started
    func(a=None, b=None) | Completed | X seconds | (1, 2)

    >>> @trace(callback=trace_callback, apply_defaults=True)
    ... def func(a=1, b=2)
    ...     return a, b
    ...
    >>> func()
    func(a=1, b=2) | Started
    func(a=1, b=2) | Completed | X seconds | (1, 2)

    Using undefined value:

    >>> @trace(callback=trace_callback, undefined_value=None)
    ... def func(a=1, b=None)
    ...     return a, b
    ...
    >>> func(b=None)
    func(a=None, b=None) | Started
    func(a=None, b=None) | Completed | X seconds | (1, None)

    >>> @trace(callback=trace_callback, undefined_value=Ellipsis)
    ... def func(a=1, b=None)
    ...     return a, b
    ...
    >>> func(b=None)
    func(a=Ellipsis, b=None) | Started
    func(a=Ellipsis, b=None) | Completed | X seconds | (1, None)

    Including one parameter:

    >>> @trace(callback=trace_callback, include='b')
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(b=2) | Started
    func(b=2) | Completed | X seconds | 6

    Including many parameters:

    >>> @trace(callback=trace_callback, include=('a', 'c'))
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(a=1, c=3) | Started
    func(a=1, c=3) | Completed | X seconds | 6

    Excluding one parameter:

    >>> @trace(callback=trace_callback, exclude='b')
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(a=1, c=3) | Started
    func(a=1, c=3) | Completed | X seconds | 6

    Excluding many parameters:

    >>> @trace(callback=trace_callback, exclude=('a', 'c'))
    ... def func(a, b, c)
    ...     return a + b + c
    ...
    >>> func(1, 2, 3)
    func(b=2) | Started
    func(b=2) | Completed | X seconds | 6
    """
    def decorator(function: CallableType) -> CallableType:
        @functools.wraps(wrapped=function)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
            frame = inspect.currentframe()
            for _ in range(stack_level):
                frame = frame.f_back
            partial_result = functools.partial(
                TraceResult,
                function_call=FunctionCall(
                    func=function,
                    args=args,
                    kwargs=kwargs,
                    apply_defaults=apply_defaults,
                    undefined_value=undefined_value,
                    include=include,
                    exclude=exclude,
                    frame=frame,
                    stack_level=stack_level,
                ),
            )
            tracer_result = partial_result(
                is_started=True,
                elapsed_time=ElapsedTime(seconds=float('nan'))
            )
            callback(tracer_result)
            start_time = time.time()
            try:
                result = function(*args, **kwargs)
                end_time = time.time()
                tracer_result = partial_result(
                    is_completed=True,
                    elapsed_time=ElapsedTime(seconds=end_time - start_time),
                    returned_value=result,
                )
                callback(tracer_result)
                return result
            except Exception as exception:
                end_time = time.time()
                tracer_result = partial_result(
                    is_failed=True,
                    elapsed_time=ElapsedTime(seconds=end_time - start_time),
                    exception=exception,
                    traceback=traceback.format_exc(),
                )
                callback(tracer_result)
                raise exception
        return wrapper
    return decorator
