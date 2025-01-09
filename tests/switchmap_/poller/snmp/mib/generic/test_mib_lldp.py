#!/usr/bin/env python3
"""Test the mib_lldp module."""

import unittest
import os
import sys
from mock import Mock


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
{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp{0}mib{0}generic\
""".format(
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

# Import other required libraries
from switchmap.poller.snmp.mib.generic import mib_lldp as testimport


class Query:
    """Class for snmp_manager.Query mock.

    A detailed tutorial about Python mocks can be found here:
    http://www.drdobbs.com/testing/using-mocks-in-python/240168251

    """

    def query(self):
        """Do an SNMP query.

        Args:
            None

        Returns:
            None
        """
        pass

    def oid_exists(self):
        """Determine existence of OID on device.

        Args:
            None

        Returns:
            None
        """
        pass

    def swalk(self):
        """Do a failsafe SNMPwalk.

        Args:
            None

        Returns:
            None
        """
        pass

    def walk(self):
        """Do a SNMPwalk.

        Args:
            None

        Returns:
            None
        """
        pass


class TestMibTestMibLldp(unittest.TestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

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

    def test_get_query(self):
        """Testing function get_query."""
        pass

    def test_init_query(self):
        """Testing function init_query."""
        pass


class TestMibLldp(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Regular walk returning byte strings
    _walk_results = {
        "lldpremsysname": {
            ".1.0.8802.1.1.2.1.4.1.1.9.0.45.1": b"device01.example.org",
            ".1.0.8802.1.1.2.1.4.1.1.9.0.47.2": b"device02.example.org",
            ".1.0.8802.1.1.2.1.4.1.1.9.0.48.3": b"device03.example.org",
        },
        "dot1dtpfdbport": {
            ".1.3.6.1.2.1.17.4.3.1.2.0.0.94.0.1.10": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.0.5.115.160.0.1": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.0.20.27.78.180.0": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.0.22.156.21.80.0": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.0.34.85.56.84.63": 0,
            ".1.3.6.1.2.1.17.4.3.1.2.0.224.134.12.31.113": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.88.243.156.162.185.64": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.100.246.157.172.214.64": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.136.67.225.9.68.127": 45,
            ".1.3.6.1.2.1.17.4.3.1.2.172.242.197.177.180.64": 47,
            ".1.3.6.1.2.1.17.4.3.1.2.248.11.203.164.174.64": 47,
        },
        "dot1dbaseport_2_ifindex": {
            ".1.3.6.1.2.1.17.1.4.1.2.45": 46,
            ".1.3.6.1.2.1.17.1.4.1.2.47": 48,
            ".1.3.6.1.2.1.17.1.4.1.2.48": 49,
        },
        "ifindex": {
            ".1.3.6.1.2.1.2.2.1.1.1": 1,
            ".1.3.6.1.2.1.2.2.1.1.2": 2,
            ".1.3.6.1.2.1.2.2.1.1.3": 3,
            ".1.3.6.1.2.1.2.2.1.1.4": 4,
            ".1.3.6.1.2.1.2.2.1.1.5": 5,
            ".1.3.6.1.2.1.2.2.1.1.6": 6,
            ".1.3.6.1.2.1.2.2.1.1.7": 7,
            ".1.3.6.1.2.1.2.2.1.1.8": 8,
            ".1.3.6.1.2.1.2.2.1.1.9": 9,
            ".1.3.6.1.2.1.2.2.1.1.10": 10,
            ".1.3.6.1.2.1.2.2.1.1.11": 11,
            ".1.3.6.1.2.1.2.2.1.1.12": 12,
            ".1.3.6.1.2.1.2.2.1.1.13": 13,
            ".1.3.6.1.2.1.2.2.1.1.14": 14,
            ".1.3.6.1.2.1.2.2.1.1.15": 15,
            ".1.3.6.1.2.1.2.2.1.1.16": 16,
            ".1.3.6.1.2.1.2.2.1.1.17": 17,
            ".1.3.6.1.2.1.2.2.1.1.18": 18,
            ".1.3.6.1.2.1.2.2.1.1.19": 19,
            ".1.3.6.1.2.1.2.2.1.1.20": 20,
            ".1.3.6.1.2.1.2.2.1.1.21": 21,
            ".1.3.6.1.2.1.2.2.1.1.22": 22,
            ".1.3.6.1.2.1.2.2.1.1.23": 23,
            ".1.3.6.1.2.1.2.2.1.1.24": 24,
            ".1.3.6.1.2.1.2.2.1.1.25": 25,
            ".1.3.6.1.2.1.2.2.1.1.26": 26,
            ".1.3.6.1.2.1.2.2.1.1.27": 27,
            ".1.3.6.1.2.1.2.2.1.1.28": 28,
            ".1.3.6.1.2.1.2.2.1.1.29": 29,
            ".1.3.6.1.2.1.2.2.1.1.30": 30,
            ".1.3.6.1.2.1.2.2.1.1.31": 31,
            ".1.3.6.1.2.1.2.2.1.1.32": 32,
            ".1.3.6.1.2.1.2.2.1.1.33": 33,
            ".1.3.6.1.2.1.2.2.1.1.34": 34,
            ".1.3.6.1.2.1.2.2.1.1.35": 35,
            ".1.3.6.1.2.1.2.2.1.1.36": 36,
            ".1.3.6.1.2.1.2.2.1.1.37": 37,
            ".1.3.6.1.2.1.2.2.1.1.38": 38,
            ".1.3.6.1.2.1.2.2.1.1.39": 39,
            ".1.3.6.1.2.1.2.2.1.1.40": 40,
            ".1.3.6.1.2.1.2.2.1.1.41": 41,
            ".1.3.6.1.2.1.2.2.1.1.42": 42,
            ".1.3.6.1.2.1.2.2.1.1.43": 43,
            ".1.3.6.1.2.1.2.2.1.1.44": 44,
            ".1.3.6.1.2.1.2.2.1.1.45": 45,
            ".1.3.6.1.2.1.2.2.1.1.46": 46,
            ".1.3.6.1.2.1.2.2.1.1.47": 47,
            ".1.3.6.1.2.1.2.2.1.1.48": 48,
            ".1.3.6.1.2.1.2.2.1.1.49": 49,
            ".1.3.6.1.2.1.2.2.1.1.50": 50,
            ".1.3.6.1.2.1.2.2.1.1.51": 51,
            ".1.3.6.1.2.1.2.2.1.1.52": 52,
            ".1.3.6.1.2.1.2.2.1.1.53": 53,
            ".1.3.6.1.2.1.2.2.1.1.54": 54,
            ".1.3.6.1.2.1.2.2.1.1.55": 55,
            ".1.3.6.1.2.1.2.2.1.1.56": 56,
            ".1.3.6.1.2.1.2.2.1.1.61": 61,
            ".1.3.6.1.2.1.2.2.1.1.78": 78,
            ".1.3.6.1.2.1.2.2.1.1.171": 171,
            ".1.3.6.1.2.1.2.2.1.1.172": 172,
            ".1.3.6.1.2.1.2.2.1.1.173": 173,
            ".1.3.6.1.2.1.2.2.1.1.174": 174,
            ".1.3.6.1.2.1.2.2.1.1.175": 175,
            ".1.3.6.1.2.1.2.2.1.1.176": 176,
            ".1.3.6.1.2.1.2.2.1.1.177": 177,
            ".1.3.6.1.2.1.2.2.1.1.178": 178,
            ".1.3.6.1.2.1.2.2.1.1.179": 179,
            ".1.3.6.1.2.1.2.2.1.1.180": 180,
            ".1.3.6.1.2.1.2.2.1.1.181": 181,
            ".1.3.6.1.2.1.2.2.1.1.253": 253,
            ".1.3.6.1.2.1.2.2.1.1.254": 254,
            ".1.3.6.1.2.1.2.2.1.1.255": 255,
            ".1.3.6.1.2.1.2.2.1.1.256": 256,
        },
    }

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

    def test_supported(self):
        """Testing method / function supported."""
        # Don't know how to test this.
        return

    def test_layer1(self):
        """Testing method / function layer1."""
        # Don't know how to test this.
        return

    def test_lldpremsysname(self):
        """Testing method / function lldpremsysname."""
        # Don't know how to test this.
        return

    def test_lldpremsyscapenabled(self):
        """Testing method / function lldpremsyscapenabled."""
        # Don't know how to test this.
        return

    def test_lldpremsysdesc(self):
        """Testing method / function lldpremsysdesc."""
        # Don't know how to test this.
        return

    def test_lldpremportdesc(self):
        """Testing method / function lldpremportdesc."""
        # Set the stage for SNMPwalk
        # Don't know how to test this.
        return

    def test__penultimate_node(self):
        """Testing method / function _penultimate_node."""
        # Initializing key variables
        oid = ".1.2.3.4.5.6.7.8.9.10"

        # Do test. Should return penultimate OID node.
        result = testimport._penultimate_node(oid)
        self.assertEqual(result, 9)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
