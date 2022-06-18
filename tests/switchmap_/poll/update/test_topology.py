#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '''{0}switchmap-ng{0}tests{0}switchmap_{0}poll{0}update\
'''.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


# Create the necessary configuration
from tests.testlib_ import setup
CONFIG = setup.config()
CONFIG.save()

from switchmap.poll.update import topology as testimport
from switchmap.db.models import Oui
from switchmap.db.table import ROui
from switchmap.db.table import IOui
from switchmap.db import models

from tests.testlib_ import db
from tests.testlib_ import data


class TestSuite(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Steps to execute when before tests start."""
        # Do nothing
        pass

    @classmethod
    def tearDownClass(cls):
        """Steps to execute when all tests are completed."""
        # Cleanup the config
        CONFIG.cleanup()

    def test_process(self):
        """Testing function process."""
        pass

    def test_device(self):
        """Testing function device."""
        pass

    def test_l1interface(self):
        """Testing function l1interface."""
        pass

    def test_vlan(self):
        """Testing function vlan."""
        pass

    def test_mac(self):
        """Testing function mac."""
        pass

    def test_macport(self):
        """Testing function macport."""
        pass

    def test_macip(self):
        """Testing function macip."""
        pass

    def test__process_macip(self):
        """Testing function _process_macip."""
        pass


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
