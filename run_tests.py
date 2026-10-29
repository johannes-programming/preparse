"""Test the package."""

from __future__ import annotations

__all__: list[str] = ["main", "run"]

import sys
import unittest
from typing import Never


def main() -> Never:
    """Exit with the test-suite status."""
    sys.exit(not run().wasSuccessful())


def run() -> unittest.TextTestResult:
    """Run the discovered unit tests."""
    loader: unittest.TestLoader
    runner: unittest.TextTestRunner
    suite: unittest.TestSuite
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    main()
