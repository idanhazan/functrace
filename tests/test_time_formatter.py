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

    def test_nanoseconds(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.nanoseconds
        expected = seconds * 1e9
        self.assertEqual(first=expected, second=actual)

    def test_microseconds(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.microseconds
        expected = seconds * 1e6
        self.assertEqual(first=expected, second=actual)

    def test_milliseconds(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.milliseconds
        expected = seconds * 1e3
        self.assertEqual(first=expected, second=actual)

    def test_seconds(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.seconds
        expected = seconds
        self.assertEqual(first=expected, second=actual)

    def test_minutes(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.minutes
        expected = seconds / 60
        self.assertEqual(first=expected, second=actual)

    def test_hours(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.hours
        expected = seconds / 3600
        self.assertEqual(first=expected, second=actual)

    def test_days(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.days
        expected = seconds / 86400
        self.assertEqual(first=expected, second=actual)

    def test_weeks(self) -> None:
        seconds = 1.0
        elapsed_time = ElapsedTime(seconds=seconds)
        actual = elapsed_time.weeks
        expected = seconds / 604800
        self.assertEqual(first=expected, second=actual)

    def test_time_parts(self) -> None:
        elapsed_time = ElapsedTime(seconds=0.0000000001)
        actual = elapsed_time.format(time_parts=False)
        expected = '0.1 nanoseconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.000000001)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 nanosecond'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.000000002)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 nanoseconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.000001)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 microsecond'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.000002)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 microseconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.001)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 millisecond'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.002)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 milliseconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=1.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 second'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=2.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 seconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=60.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 minute'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=120.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 minutes'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=3600.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 hour'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=7200.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 hours'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=86400.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 day'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=172800.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 days'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=604800.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '1 week'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=1209600.0)
        actual = elapsed_time.format(time_parts=False)
        expected = '2 weeks'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=0.0000000001)
        actual = elapsed_time.format(time_parts=True)
        expected = '0.1 nanoseconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=694861.001001001)
        actual = elapsed_time.format(time_parts=True)
        expected = ', '.join([f'{1} {unit}' for unit in self.units])
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=694861.001001001 * 2)
        actual = elapsed_time.format(time_parts=True)
        expected = ', '.join([f'{2} {unit}s' for unit in self.units])
        self.assertEqual(first=expected, second=actual)

    def test_separator(self) -> None:
        elapsed_time = ElapsedTime(seconds=123.0)
        actual = elapsed_time.format(time_parts=True, separator=' | ')
        expected = '2 minutes | 3 seconds'
        self.assertEqual(first=expected, second=actual)
        elapsed_time = ElapsedTime(seconds=123.0)
        actual = elapsed_time.format(time_parts=False, decimals=2)
        expected = '2.05 minutes'
        self.assertEqual(first=expected, second=actual)

    def test_decimals(self) -> None:
        elapsed_time = ElapsedTime(seconds=97.5)
        actual = elapsed_time.format(decimals=3)
        expected = '1.625 minutes'
        self.assertEqual(first=expected, second=actual)
        actual = elapsed_time.format(decimals=2)
        expected = '1.63 minutes'
        self.assertEqual(first=expected, second=actual)
        actual = elapsed_time.format(decimals=1)
        expected = '1.6 minutes'
        self.assertEqual(first=expected, second=actual)
        actual = elapsed_time.format(decimals=0)
        expected = '2 minutes'
        self.assertEqual(first=expected, second=actual)


if __name__ == '__main__':
    unittest.main()
