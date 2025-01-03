#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}"
    "dashboard{0}table".format(os.sep)
)
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


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.dashboard.table import index as testimport
from switchmap.dashboard import DeviceMeta


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_rows(self):
        """Testing function rows."""
        # Initialize key variables
        original_rows = [
            {
                "hostname": "device02.site02.example.net",
                "idxDevice": 97,
            },
            {
                "hostname": "device01.site02.example.net",
                "idxDevice": 98,
            },
        ]
        rows = [
            DeviceMeta(
                hostname=_.get("hostname"), idx_device=_.get("idxDevice")
            )
            for _ in original_rows
        ]

        # Test
        result = testimport.rows(rows)[0]
        self.assertEqual(
            result.col0,
            '<a href="/switchmap/devices/97">device02.site02.example.net'
            "</a>",
        )
        self.assertEqual(
            result.col1,
            '<a href="/switchmap/devices/98">device01.site02.example.net'
            "</a>",
        )


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
