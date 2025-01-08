#!/usr/bin/env python3
"""Test the mib_ip module."""

import os
import sys
import unittest
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
from switchmap.poller.snmp.mib.generic import mib_ip as testimport


class Query:
    """Class for snmp_manager.Query mock.

    A detailed tutorial about Python mocks can be found here:
    http://www.drdobbs.com/testing/using-mocks-in-python/240168251

    """

    def query(self):
        """Do an SNMP query."""
        pass

    def oid_exists(self):
        """Determine existence of OID on device."""
        pass

    def swalk(self):
        """Do a failsafe SNMPwalk."""
        pass

    def walk(self):
        """Do a failable SNMPwalk."""
        pass


class TestMibIpFunctions(unittest.TestCase):
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


class TestMibIp(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Normalized walk returning binary data
    walk_results_ipv4_binary = {
        ".1.3.6.1.2.1.4.22.1.2.0.10.10.10.10": b"\x00\x16\xc2\x9c\x15P\x00",
        ".1.3.6.1.2.1.4.22.1.2.0"
        ".200.200.200.200": b"\xc2\x98\xc3\xae\xc3\x8bV%\xc2\xb6",
    }

    # OID with IPv6 appended in decimal format
    walk_results_ipv6_binary = {
        ".1.3.6.1.2.1.4.35.1.4.3.2.16.254.128.0.0.0.0.0.0"
        ".53.111.109.168.125."
        "42.84.88": b"\xc3\x94\xc2\x85d\xc2\x9f\xc3\x9c\x7f",
        ".1.3.6.1.2.1.4.35.1.4.3.2.16.254.128.0.0.0.0.0.0"
        ".2.30.201.255.254.172."
        "62.123": b"\xc3\x80|\xc3\x91\xc2\xa0\xc3\x82\xc2\x85",
    }

    # Set the stage for SNMPwalk for binary results
    snmpobj_ipv4_binary = Mock(spec=Query)
    mock_spec_ipv4_binary = {
        "swalk.return_value": walk_results_ipv4_binary,
        "walk.return_value": walk_results_ipv4_binary,
    }
    snmpobj_ipv4_binary.configure_mock(**mock_spec_ipv4_binary)

    snmpobj_ipv6_binary = Mock(spec=Query)
    mock_spec_ipv6_binary = {
        "swalk.return_value": walk_results_ipv6_binary,
        "walk.return_value": walk_results_ipv6_binary,
    }
    snmpobj_ipv6_binary.configure_mock(**mock_spec_ipv6_binary)

    # Initialize expected results
    ipv4_expected_dict = {
        "10.10.10.10": "00169c155000",
        "200.200.200.200": "98eecb5625b6",
    }

    ipv6_expected_dict = {
        "fe80:0000:0000:0000:356f:6da8:7d2a:5458": "d485649fdc7f",
        "fe80:0000:0000:0000:021e:c9ff:feac:3e7b": "c07cd1a0c285",
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

    def test_get_query(self):
        """Testing method / function get_query."""
        # Initializing key variables
        pass

    def test_init_query(self):
        """Testing method / function init_query."""
        # Initializing key variables
        pass

    def test_supported(self):
        """Testing method / function supported."""
        # Initializing key variables
        pass

    def test_layer3(self):
        """Testing method / function layer3."""
        # Initializing key variables
        pass

    def test_ipnettomediatable(self):
        """Testing method / function ipnettomediatable."""
        # Initialize key variables
        oid = ".1.3.6.1.2.1.4.22.1.2"

        # Get results
        testobj = testimport.init_query(self.snmpobj_ipv4_binary)
        results = testobj.ipnettomediatable()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, str), True)
            self.assertEqual(value, self.ipv4_expected_dict[key])

        # Test that we are getting the correct OID
        results = testobj.ipnettomediatable(oidonly=True)
        self.assertEqual(results, oid)

    def test_ipnettophysicalphysaddress(self):
        """Testing method / function ipnettophysicalphysaddress."""
        # Initialize key variables
        oid = ".1.3.6.1.2.1.4.35.1.4"

        # Get results
        testobj = testimport.init_query(self.snmpobj_ipv6_binary)
        results = testobj.ipnettophysicalphysaddress()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, str), True)
            self.assertEqual(value, self.ipv6_expected_dict[key])

        # Test that we are getting the correct OID
        results = testobj.ipnettophysicalphysaddress(oidonly=True)
        self.assertEqual(results, oid)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
