from __future__ import annotations

from unittest import TestLoader, TestSuite, TextTestRunner

from tests.test_function_call import TestFunctionCall
from tests.test_time_formatter import TestElapsedTime

__all__ = ('test_suite',)


def test_suite() -> TestSuite:
    suite = TestSuite()
    loader = TestLoader()
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
    runner = TextTestRunner()
    runner.run(test=test_suite())
