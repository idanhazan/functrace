import unittest

from tests.test_function_call import TestFunctionCall
from tests.test_time_formatter import TestElapsedTime

__all__ = ('test_suite',)


def test_suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(
        tests=loader.loadTestsFromTestCase(
            testCaseClass=TestFunctionCall,
        ),
    )
    suite.addTests(
        tests=loader.loadTestsFromTestCase(
            testCaseClass=TestElapsedTime,
        ),
    )
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test=test_suite())
