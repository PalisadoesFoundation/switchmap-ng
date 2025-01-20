#!/usr/bin/env python3
"""Test the macport module."""

import os
import sys
import unittest
from operator import attrgetter

from collections import namedtuple

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
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}db{0}misc""".format(
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

from switchmap.server.db import models
from tests.testlib_ import db
from tests.testlib_ import data
from switchmap.server.db.misc import interface as testimport

InterfaceTerms = namedtuple(
    "InterfaceTerms", "interfaces devices zones ipports"
)

LOOP_MAX = 30


class TestInterface(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    iterations = 20

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

        # Drop tables
        database = db.Database()
        database.drop()

        # Create database tables
        models.create_all_tables()

        # Pollinate db with prerequisites
        cls.interface_terms = db.populate()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps after each tests is completed."""
        # Drop tables
        database = db.Database()
        database.drop()

        # Cleanup the configuration
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_get_interface(self):
        """Testing function get_interface."""
        # Initialize key variables
        terms = self.interface_terms
        expected = sorted(terms.interfaces, key=attrgetter("idx_device"))
        results = []
        controls = []

        # Get results
        for interface in terms.interfaces:
            test_interface = testimport.Interface(terms.idx_event, interface.id)
            found = test_interface.get_interface()
            if found:
                results.append(found)

        # Test
        for key, result in enumerate(
            sorted(results, key=attrgetter("idx_device"))
        ):
            self.assertEqual(result.idx_device, expected[key].idx_device)
            self.assertEqual(result.name, expected[key].name)
            self.assertEqual(result.description, expected[key].description)
        self.assertEqual(len(results), len(expected))

        # Create control values
        for value in range(self.iterations * 10):
            new = data.random_integer()
            if new not in [_.id for _ in terms.interfaces]:
                controls.append(new)
            if len(controls) >= self.iterations:
                break

        # Test invalid interface IDs
        for control in controls:
            test_interface = testimport.Interface(terms.idx_event, control)
            self.assertFalse(test_interface.get_interface())

    def test_get_ipports(self):
        """Testing function get_ipports."""
        # Initialize key variables
        terms = self.interface_terms
        expected = sorted(terms.ipports, key=attrgetter("idx_l1interface"))
        results = []
        controls = []

        # Get results
        for interface in terms.interfaces:
            test_interface = testimport.Interface(terms.idx_event, interface.id)
            found = test_interface.get_ipports()
            results.extend(found)

        # Test
        for key, result in enumerate(
            sorted(results, key=attrgetter("idx_l1interface"))
        ):
            self.assertEqual(
                result.idx_l1interface, expected[key].idx_l1interface
            )
            self.assertEqual(result.ip_address, expected[key].ip_address)
            self.assertEqual(result.port, expected[key].port)
        self.assertEqual(len(results), len(expected))

        # Create control values
        for value in range(self.iterations * 10):
            new = data.random_integer()
            if new not in [_.id for _ in terms.interfaces]:
                controls.append(new)
            if len(controls) >= self.iterations:
                break

        # Test invalid interface IDs
        for control in controls:
            test_interface = testimport.Interface(terms.idx_event, control)
            self.assertFalse(test_interface.get_ipports())


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
