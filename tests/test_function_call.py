import functools
import inspect
import pathlib
import unittest

from functrace.utilities import FunctionCall

__all__ = ('TestFunctionCall',)


def func(a=1, b=2) -> int:
    return a + b


class TestFunctionCall(unittest.TestCase):
    def setUp(self) -> None:
        self.function_call = functools.partial(
            FunctionCall,
            func=func,
            args=(),
            kwargs={},
            apply_defaults=False,
            undefined_value=None,
            include=None,
            exclude=None,
            frame=inspect.currentframe(),
            stack_level=0,
        )

    def tearDown(self) -> None:
        del self.function_call

    def test_path(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{path}')
        expected = inspect.getmodule(object=func).__file__
        self.assertEqual(first=expected, second=actual)

    def test_file(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{file}')
        expected = pathlib.Path(inspect.getmodule(object=func).__file__).name
        self.assertEqual(first=expected, second=actual)

    def test_module(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{module}')
        expected = inspect.getmodule(object=func).__name__
        self.assertEqual(first=expected, second=actual)

    def test_name(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{name}')
        expected = func.__name__
        self.assertEqual(first=expected, second=actual)

    def test_qualname(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{qualname}')
        expected = func.__qualname__
        self.assertEqual(first=expected, second=actual)

    def test_line(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{line}')
        expected = str(inspect.getlineno(frame=function_call.frame))
        self.assertEqual(first=expected, second=actual)

    def test_params(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{params}')
        expected = 'a=None, b=None'
        self.assertEqual(first=expected, second=actual)

    def test_params_with_apply_defaults(self) -> None:
        function_call = self.function_call(apply_defaults=True)
        actual = function_call.format(pattern='{params}')
        expected = 'a=1, b=2'
        self.assertEqual(first=expected, second=actual)

    def test_params_with__undefined_value(self) -> None:
        function_call = self.function_call(undefined_value=0)
        actual = function_call.format(pattern='{params}')
        expected = 'a=0, b=0'
        self.assertEqual(first=expected, second=actual)

    def test_params_with_include_a(self) -> None:
        function_call = self.function_call(include='a')
        actual = function_call.format(pattern='{params}')
        expected = 'a=None'
        self.assertEqual(first=expected, second=actual)

    def test_params_with_include_ab(self) -> None:
        function_call = self.function_call(include=('a', 'b'))
        actual = function_call.format(pattern='{params}')
        expected = 'a=None, b=None'
        self.assertEqual(first=expected, second=actual)

    def test_params_with_exclude_a(self) -> None:
        function_call = self.function_call(exclude='a')
        actual = function_call.format(pattern='{params}')
        expected = 'b=None'
        self.assertEqual(first=expected, second=actual)

    def test_params_with_exclude_ab(self) -> None:
        function_call = self.function_call(exclude=('a', 'b'))
        actual = function_call.format(pattern='{params}')
        expected = ''
        self.assertEqual(first=expected, second=actual)

    def test_params_with_association(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{params}', association=': ')
        expected = 'a: None, b: None'
        self.assertEqual(first=expected, second=actual)

    def test_params_with_separator(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{params}', separator=' | ')
        expected = 'a=None | b=None'
        self.assertEqual(first=expected, second=actual)


if __name__ == '__main__':
    unittest.main()
