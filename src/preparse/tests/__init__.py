import unittest

__all__ = ["test"]


def test() -> unittest.TextTestResult:
    "This function runs all the tests."
    loader: unittest.TestLoader
    tests: unittest.TestSuite
    runner: unittest.TextTestRunner
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="preparse.tests")
    runner = unittest.TextTestRunner()
    return runner.run(tests)
