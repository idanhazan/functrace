import functools
import logging

from functrace import TraceResult, trace


def trace_callback(result: TraceResult):
    stack_level = result.function_call.stack_level
    function_call = result.function_call.format(pattern='{qualname}({params})')
    elapsed_time = result.elapsed_time.format()
    returned_value = repr(result.returned_value)
    exception = repr(result.exception)
    parts = [function_call]
    if result.is_started:
        parts.extend(['Started'])
    if result.is_completed:
        parts.extend(['Completed', elapsed_time, returned_value])
    if result.is_failed:
        parts.extend(['Completed', elapsed_time, exception])
    logging.getLogger().debug(msg=' | '.join(parts), stacklevel=stack_level)


@trace(callback=trace_callback)
def func():
    return 'function'


class Class1:
    @trace(callback=trace_callback, exclude='self')
    def func(self):
        return 'method'


class Class2:
    @classmethod
    @trace(callback=trace_callback, exclude='cls')
    def func(cls):
        return 'class method'


class Class3:
    @staticmethod
    @trace(callback=trace_callback)
    def func():
        return 'static method'


class Class4:
    @property
    @trace(callback=trace_callback, exclude='self')
    def func(self):
        return 'property'


class Class5:
    @functools.cached_property
    @trace(callback=trace_callback, exclude='self', stack_level=2)
    def func(self):
        return 'cached_property'


class Class6:
    @functools.cache
    @trace(callback=trace_callback, exclude='self')
    def func(self):
        return 'cache'


if __name__ == '__main__':
    logging.basicConfig(
        format='%(filename)s, line: %(lineno)d | %(message)s',
        level=logging.DEBUG,
    )

    c1 = Class1()
    c2 = Class2()
    c3 = Class3()
    c4 = Class4()
    c5 = Class5()
    c6 = Class6()

    func()
    c1.func()
    c2.func()
    c3.func()
    c4.func
    c5.func
    c6.func()

# builtins_logging.py, line: 82 | func() | Started
# builtins_logging.py, line: 82 | func() | Completed | X seconds | 'function'
# builtins_logging.py, line: 83 | Class1.func() | Started
# builtins_logging.py, line: 83 | Class1.func() | Completed | X seconds | 'method'
# builtins_logging.py, line: 84 | Class2.func() | Started
# builtins_logging.py, line: 84 | Class2.func() | Completed | X seconds | 'class method'
# builtins_logging.py, line: 85 | Class3.func() | Started
# builtins_logging.py, line: 85 | Class3.func() | Completed | X seconds | 'static method'
# builtins_logging.py, line: 86 | Class4.func() | Started
# builtins_logging.py, line: 86 | Class4.func() | Completed | X seconds | 'property'
# builtins_logging.py, line: 87 | Class5.func() | Started
# builtins_logging.py, line: 87 | Class5.func() | Completed | X seconds | 'cached_property'
# builtins_logging.py, line: 88 | Class6.func() | Started
# builtins_logging.py, line: 88 | Class6.func() | Completed | X seconds | 'cache'
