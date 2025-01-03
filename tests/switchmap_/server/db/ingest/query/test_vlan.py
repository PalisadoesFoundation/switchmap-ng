#!/usr/bin/env python3
"""Test the macport module."""

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
                        os.path.abspath(
                            os.path.join(
                                os.path.abspath(
                                    os.path.join(
                                        os.path.abspath(
                                            os.path.join(EXEC_DIR, os.pardir)
                                        ),
                                        os.pardir,
                                    )
                                ),
                                os.pardir,
                            )
                        ),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}ingest{0}query""".format(
    os.sep
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

from switchmap.server.db.table import vlan
from switchmap.server.db import models

from tests.testlib_ import db

from switchmap.server.db.ingest.query import vlan as testimport


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################
    prerequisites = None

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting each test."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

        # Create database tables
        models.create_all_tables()

        # Pollinate db with prerequisites
        cls.prerequisites = db.populate()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps after each tests is completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_by_idx_l1interface(self):
        """Testing function by_idx_l1interface."""
        # Initialize key variables
        lookup = {}

        # Prepare data for testing
        for (
            idx_l1interface,
            idx_vlans,
        ) in self.prerequisites.idx_l1interface.items():
            for idx_vlan in idx_vlans:
                detail = vlan.idx_exists(idx_vlan)
                found = lookup.get(idx_l1interface)
                if bool(found) is True:
                    lookup[idx_l1interface].append(detail)
                else:
                    lookup[idx_l1interface] = [detail]

        # Test
        for idx_l1interface, expected in lookup.items():
            result = testimport.by_idx_l1interface(idx_l1interface)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
