import functools
import inspect
import unittest

from functrace.utilities import FunctionCall

__all__ = ('TestFunctionCall',)


def func(a=1, b=2) -> int:
    return a + b


class TestFunctionCall(unittest.TestCase):
    def setUp(self) -> None:
        self.function_call = functools.partial(
            FunctionCall,
            function=func,
            args=(),
            kwargs={},
            apply_defaults=False,
            undefined_value=None,
            include=None,
            exclude=None,
            frame=inspect.currentframe(),
        )

    def tearDown(self) -> None:
        del self.function_call

    def test_absolute_path(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{absolute_path}')
        expected = inspect.getmodule(object=func).__file__
        self.assertEqual(first=expected, second=actual)

    def test_module_name(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{module_name}')
        expected = inspect.getmodule(object=func).__name__
        self.assertEqual(first=expected, second=actual)

    def test_function_name(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{function_name}')
        expected = func.__name__
        self.assertEqual(first=expected, second=actual)

    def test_function_qualified_name(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{function_qualified_name}')
        expected = func.__qualname__
        self.assertEqual(first=expected, second=actual)

    def test_line_number(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{line_number}')
        expected = str(inspect.getlineno(frame=function_call.frame))
        self.assertEqual(first=expected, second=actual)

    def test_arguments(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{arguments}')
        expected = 'a=None, b=None'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_apply_defaults(self) -> None:
        function_call = self.function_call(apply_defaults=True)
        actual = function_call.format(pattern='{arguments}')
        expected = 'a=1, b=2'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with__undefined_value(self) -> None:
        function_call = self.function_call(undefined_value=0)
        actual = function_call.format(pattern='{arguments}')
        expected = 'a=0, b=0'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_include_a(self) -> None:
        function_call = self.function_call(include='a')
        actual = function_call.format(pattern='{arguments}')
        expected = 'a=None'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_include_ab(self) -> None:
        function_call = self.function_call(include=('a', 'b'))
        actual = function_call.format(pattern='{arguments}')
        expected = 'a=None, b=None'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_exclude_a(self) -> None:
        function_call = self.function_call(exclude='a')
        actual = function_call.format(pattern='{arguments}')
        expected = 'b=None'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_exclude_ab(self) -> None:
        function_call = self.function_call(exclude=('a', 'b'))
        actual = function_call.format(pattern='{arguments}')
        expected = ''
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_association(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{arguments}', association=': ')
        expected = 'a: None, b: None'
        self.assertEqual(first=expected, second=actual)

    def test_arguments_with_separator(self) -> None:
        function_call = self.function_call()
        actual = function_call.format(pattern='{arguments}', separator=' | ')
        expected = 'a=None | b=None'
        self.assertEqual(first=expected, second=actual)


if __name__ == '__main__':
    unittest.main()
