__all__: list[str] = ["test"]

import unittest


def test() -> unittest.TextTestResult:
    "This function runs all the tests."
    loader: unittest.TestLoader
    runner: unittest.TextTestRunner
    tests: unittest.TestSuite
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="preparse.tests")
    runner = unittest.TextTestRunner()
    return runner.run(tests)
