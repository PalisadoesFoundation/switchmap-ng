#!/usr/bin/env python3
"""Class used to set test configuration used by unittests."""

# Standard imports
import sys
import os

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir)
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}bin".format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)


# Import application libraries
from tests.testlib_ import setup


def main():
    """Create test configurations."""
    # Save the config
    config = setup.config()
    config.save()


if __name__ == "__main__":
    # Do the unit test
    main()
