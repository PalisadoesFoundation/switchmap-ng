#!/usr/bin/env python3
"""Test the macport module."""

import os
import sys
import unittest
from operator import attrgetter

# import random
# import time
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

# from switchmap.server.db.table import macport
# from switchmap.server.db.table import oui
# from switchmap.server.db.table import mac
# from switchmap.server.db.table import zone
# from switchmap.server.db.table import event
# from switchmap.server.db.table import macip
# from switchmap.server.db.table import l1interface
# from switchmap.server.db.table import IMacPort
# from switchmap.server.db.table import IMac
# from switchmap.server.db.table import IOui
# from switchmap.server.db.table import IL1Interface
# from switchmap.server.db.table import IMacIp
from switchmap.server.db import models

# from switchmap.core import general

from tests.testlib_ import db
from tests.testlib_ import data

# from tests.testlib_ import data

from switchmap.server.db.misc import search as testimport

SearchTerms = namedtuple("SearchTerms", "ouis macs ips ifaliases hostnames")

LOOP_MAX = 30


class TestSearch(unittest.TestCase):
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
        cls.search_terms = db.populate()

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

    def test_find(self):
        """Testing function find."""
        # Initialize key variables
        terms = self.search_terms
        expecteds = [
            sorted(terms.ipports, key=attrgetter("idx_l1interface")),
            sorted(terms.ipports, key=attrgetter("idx_l1interface")),
            sorted(terms.ipports, key=attrgetter("idx_l1interface")),
            sorted(terms.ipports, key=attrgetter("idx_l1interface")),
        ]
        all_inputs = [
            [_.mac for _ in terms.macs],
            [_.address for _ in terms.ips],
            [_.ifalias for _ in terms.interfaces],
            [_.address for _ in terms.ips],
        ]

        for key_expected, inputs in enumerate(all_inputs):
            # Initialize loop variables
            results = []
            controls = []
            expected = expecteds[key_expected]

            # Get results
            for value in inputs:
                search_ = testimport.Search(terms.idx_event, value)
                found = search_.find()
                results.extend(found)

            # Test
            for key, result in enumerate(
                sorted(results, key=attrgetter("idx_l1interface"))
            ):
                self.assertEqual(
                    result.idx_l1interface, expected[key].idx_l1interface
                )
            self.assertEqual(len(results), len(expected))

            # Create control values
            for value in range(self.iterations * 10):
                new = "TEST_FIND_{}".format(data.random_string())
                if new not in inputs:
                    controls.append(new)
                if len(controls) >= self.iterations:
                    break

            # Test
            for control in controls:
                search_ = testimport.Search(terms.idx_event, control)
                self.assertFalse(search_.find())

    def test_macaddress(self):
        """Testing function macaddress."""
        # Initialize key variables
        terms = self.search_terms
        expected = sorted(terms.ipports, key=attrgetter("idx_l1interface"))
        inputs = [_.mac for _ in terms.macs]
        results = []
        controls = []

        # Get results
        for value in inputs:
            search_ = testimport.Search(terms.idx_event, value)
            found = search_.macaddress()
            results.extend(found)

        # Test
        for key, result in enumerate(
            sorted(results, key=attrgetter("idx_l1interface"))
        ):
            self.assertEqual(
                result.idx_l1interface, expected[key].idx_l1interface
            )
        self.assertEqual(len(results), len(expected))

        # Create control values
        for value in range(self.iterations * 10):
            new = "TEST_MAC_{}".format(data.random_string())
            if new not in inputs:
                controls.append(new)
            if len(controls) >= self.iterations:
                break

        # Test
        for control in controls:
            search_ = testimport.Search(terms.idx_event, control)
            self.assertFalse(search_.macaddress())

    def test_ipaddress(self):
        """Testing function ipaddress."""
        # Initialize key variables
        terms = self.search_terms
        expected = sorted(terms.ipports, key=attrgetter("idx_l1interface"))
        inputs = [_.address for _ in terms.ips]
        results = []
        controls = []

        # Get results
        for value in inputs:
            search_ = testimport.Search(terms.idx_event, value)
            found = search_.ipaddress()
            results.extend(found)

        # Test
        for key, result in enumerate(
            sorted(results, key=attrgetter("idx_l1interface"))
        ):
            self.assertEqual(
                result.idx_l1interface, expected[key].idx_l1interface
            )
        self.assertEqual(len(results), len(expected))

        # Create control values
        for value in range(self.iterations * 10):
            new = data.ip_().address
            if new not in inputs:
                controls.append(new)
            if len(controls) >= self.iterations:
                break

        # Test
        for control in controls:
            search_ = testimport.Search(terms.idx_event, control)
            self.assertFalse(search_.ipaddress())

    def test_ifalias(self):
        """Testing function ifalias."""
        # Initialize key variables
        terms = self.search_terms
        expected = sorted(terms.ipports, key=attrgetter("idx_l1interface"))
        inputs = [_.ifalias for _ in terms.interfaces]
        results = []
        controls = []

        # Get results
        for value in inputs:
            search_ = testimport.Search(terms.idx_event, value)
            found = search_.ifalias()
            results.extend(found)

        # Test
        for key, result in enumerate(
            sorted(results, key=attrgetter("idx_l1interface"))
        ):
            self.assertEqual(
                result.idx_l1interface, expected[key].idx_l1interface
            )
        self.assertEqual(len(results), len(expected))

        # Create control values
        for value in range(self.iterations * 10):
            new = data.random_string()
            if new not in inputs:
                controls.append(new)
            if len(controls) >= self.iterations:
                break

        # Test
        for control in controls:
            search_ = testimport.Search(terms.idx_event, control)
            self.assertFalse(search_.ifalias())

    def test_hostname(self):
        """Testing function hostname."""
        # Initialize key variables
        terms = self.search_terms
        expected = sorted(terms.ipports, key=attrgetter("idx_l1interface"))
        inputs = [_.hostname for _ in terms.ips]
        results = []
        controls = []

        # Get results
        for value in inputs:
            search_ = testimport.Search(terms.idx_event, value)
            found = search_.hostname()
            results.extend(found)

        # Test
        for key, result in enumerate(
            sorted(results, key=attrgetter("idx_l1interface"))
        ):
            self.assertEqual(
                result.idx_l1interface, expected[key].idx_l1interface
            )
        self.assertEqual(len(results), len(expected))

        # Create control values
        for value in range(self.iterations * 10):
            new = "TEST_HOST_{}".format(data.random_string())
            if new not in inputs:
                controls.append(new)
            if len(controls) >= self.iterations:
                break

        # Test
        for control in controls:
            search_ = testimport.Search(terms.idx_event, control)
            self.assertFalse(search_.hostname())


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
