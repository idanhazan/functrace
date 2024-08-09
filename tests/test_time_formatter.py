import unittest

from functrace.utilities import ElapsedTime

__all__ = ('TestElapsedTime',)


class TestElapsedTime(unittest.TestCase):
    def setUp(self) -> None:
        self.units = [
            'week',
            'day',
            'hour',
            'minute',
            'second',
            'millisecond',
            'microsecond',
            'nanosecond',
        ]

    def tearDown(self) -> None:
        del self.units

    def test_singular(self) -> None:
        elapsed_time = ElapsedTime(seconds=694861.001001001)
        actual = elapsed_time.format(ignore_zeros=False)
        expected = ', '.join([f'{1} {unit}' for unit in self.units])
        self.assertEqual(first=expected, second=actual)

    def test_plural(self) -> None:
        elapsed_time = ElapsedTime(seconds=694861.001001001 * 2)
        actual = elapsed_time.format(ignore_zeros=False)
        expected = ', '.join([f'{2} {unit}s' for unit in self.units])
        self.assertEqual(first=expected, second=actual)

    def test_ignore_zeros(self) -> None:
        elapsed_time = ElapsedTime(seconds=0.0)
        actual = elapsed_time.format(ignore_zeros=False)
        expected = ', '.join([f'{0} {unit}s' for unit in self.units])
        self.assertEqual(first=expected, second=actual)
        actual = ElapsedTime(seconds=0.0).format(ignore_zeros=True)
        expected = '0 nanoseconds'
        self.assertEqual(first=expected, second=actual)

    def test_separator(self) -> None:
        elapsed_time = ElapsedTime(seconds=123.0)
        actual = elapsed_time.format(separator=' | ')
        expected = '2 minutes | 3 seconds'
        self.assertEqual(first=expected, second=actual)


if __name__ == '__main__':
    unittest.main()
