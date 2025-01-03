#!/usr/bin/env python3
"""Test the configuration module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}dashboard".format(os.sep)
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


from switchmap.dashboard import graphql_filters as test_module


class TestFunctions(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_or_operator(self):
        """Testing function or_operator."""
        # Initialize key variables
        key = "Switchmap"
        items = list(range(5))
        expected = """\
{or: [{or: [{Switchmap: {eq: 0}}, {Switchmap: {eq: 1}}, {Switchmap: {eq: 2}}, \
{Switchmap: {eq: 3}}, {Switchmap: {eq: 4}}]}]}"""

        # Test
        result = test_module.or_operator(key, items)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
