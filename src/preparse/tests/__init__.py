import unittest

__all__ = ["test"]


def test() -> unittest.TextTestResult:
    "This function runs all the tests."
    loader: unittest.TestLoader
    tests: unittest.TestSuite
    runner: unittest.TextTestRunner
    result: unittest.TextTestResult
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="preparse.tests")
    runner = unittest.TextTestRunner()
    result = runner.run(tests)
    return result
