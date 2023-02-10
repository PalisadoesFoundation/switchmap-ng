#!/usr/bin/env python3
"""Test the mib_if module."""

import os
import sys
import binascii
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
from switchmap.poll.snmp.mib.generic import mib_if as testimport


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


class TestMibIfFunctions(unittest.TestCase):
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


class TestMibIf(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Normalized walk returning integers
    nwalk_results_integer = {100: 1234, 200: 5678}

    # Set the stage for SNMPwalk for integer results
    snmpobj_integer = Mock(spec=Query)
    mock_spec_integer = {
        "swalk.return_value": nwalk_results_integer,
        "walk.return_value": nwalk_results_integer,
    }
    snmpobj_integer.configure_mock(**mock_spec_integer)

    # Normalized walk returning integers for the ifIndex
    nwalk_results_ifindex = {100: 100, 200: 200}

    # Set the stage for SNMPwalk for integer results for the ifIndex
    snmpobj_ifindex = Mock(spec=Query)
    mock_spec_ifindex = {
        "swalk.return_value": nwalk_results_ifindex,
        "walk.return_value": nwalk_results_ifindex,
    }
    snmpobj_ifindex.configure_mock(**mock_spec_ifindex)

    # Normalized walk returning strings
    nwalk_results_bytes = {100: b"1234", 200: b"5678"}

    # Set the stage for SNMPwalk for string results
    snmpobj_bytes = Mock(spec=Query)
    mock_spec_bytes = {
        "swalk.return_value": nwalk_results_bytes,
        "walk.return_value": nwalk_results_bytes,
    }
    snmpobj_bytes.configure_mock(**mock_spec_bytes)

    # Normalized walk returning binary data
    nwalk_results_binary = {
        100: binascii.unhexlify("1234"),
        200: binascii.unhexlify("5678"),
    }

    # Set the stage for SNMPwalk for binary results
    snmpobj_binary = Mock(spec=Query)
    mock_spec_binary = {
        "swalk.return_value": nwalk_results_binary,
        "walk.return_value": nwalk_results_binary,
    }
    snmpobj_binary.configure_mock(**mock_spec_binary)

    # Initializing key variables
    expected_dict = {
        100: {
            "ifAlias": "1234",
            "ifSpeed": 1234,
            "ifOperStatus": 1234,
            "ifAdminStatus": 1234,
            "ifType": 1234,
            "ifName": "1234",
            "ifIndex": 100,
            "ifPhysAddress": "1234",
            "ifInOctets": 1234,
            "ifOutOctets": 1234,
            "ifInBroadcastPkts": 1234,
            "ifOutBroadcastPkts": 1234,
            "ifInMulticastPkts": 1234,
            "ifOutMulticastPkts": 1234,
            "ifLastChange": 1234,
            "ifDescr": "1234",
        },
        200: {
            "ifAlias": "5678",
            "ifSpeed": 5678,
            "ifOperStatus": 5678,
            "ifAdminStatus": 5678,
            "ifType": 5678,
            "ifName": "5678",
            "ifIndex": 200,
            "ifPhysAddress": "5678",
            "ifInOctets": 5678,
            "ifOutOctets": 5678,
            "ifInBroadcastPkts": 5678,
            "ifOutBroadcastPkts": 5678,
            "ifInMulticastPkts": 5678,
            "ifOutMulticastPkts": 5678,
            "ifLastChange": 5678,
            "ifDescr": "5678",
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

    def test_get_query(self):
        """Testing function get_query."""
        pass

    def test_init_query(self):
        """Testing function init_query."""
        pass

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_system(self):
        """Testing function system."""
        pass

    def test_layer1(self):
        """Testing function layer1."""
        # Layer 1 testing only seems to work when all the methods return
        # the same type of results (eg. int, string, hex)
        pass

    def test_iflastchange(self):
        """Testing function iflastchange."""
        # Initialize key variables
        oid_key = "ifLastChange"
        oid = ".1.3.6.1.2.1.2.2.1.9"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.iflastchange()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.iflastchange(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifinoctets(self):
        """Testing function ifinoctets."""
        # Initialize key variables
        oid_key = "ifInOctets"
        oid = ".1.3.6.1.2.1.2.2.1.10"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifinoctets()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifinoctets(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifoutoctets(self):
        """Testing function ifoutoctets."""
        # Initialize key variables
        oid_key = "ifOutOctets"
        oid = ".1.3.6.1.2.1.2.2.1.16"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifoutoctets()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifoutoctets(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifdescr(self):
        """Testing function ifdescr."""
        # Initialize key variables
        oid_key = "ifDescr"
        oid = ".1.3.6.1.2.1.2.2.1.2"

        # Get results
        testobj = testimport.init_query(self.snmpobj_bytes)
        results = testobj.ifdescr()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifdescr(oidonly=True)
        self.assertEqual(results, oid)

    def test_iftype(self):
        """Testing function iftype."""
        # Initialize key variables
        oid_key = "ifType"
        oid = ".1.3.6.1.2.1.2.2.1.3"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.iftype()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.iftype(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifspeed(self):
        """Testing function ifspeed."""
        # Initialize key variables
        oid_key = "ifSpeed"
        oid = ".1.3.6.1.2.1.2.2.1.5"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifspeed()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifspeed(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifadminstatus(self):
        """Testing function ifadminstatus."""
        # Initialize key variables
        oid_key = "ifAdminStatus"
        oid = ".1.3.6.1.2.1.2.2.1.7"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifadminstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifadminstatus(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifoperstatus(self):
        """Testing function ifoperstatus."""
        # Initialize key variables
        oid_key = "ifOperStatus"
        oid = ".1.3.6.1.2.1.2.2.1.8"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifoperstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifoperstatus(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifalias(self):
        """Testing function ifalias."""
        # Initialize key variables
        oid_key = "ifAlias"
        oid = ".1.3.6.1.2.1.31.1.1.1.18"

        # Get results
        testobj = testimport.init_query(self.snmpobj_bytes)
        results = testobj.ifalias()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifalias(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifname(self):
        """Testing function ifname."""
        # Initialize key variables
        oid_key = "ifName"
        oid = ".1.3.6.1.2.1.31.1.1.1.1"

        # Get results
        testobj = testimport.init_query(self.snmpobj_bytes)
        results = testobj.ifname()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifname(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifindex(self):
        """Testing function ifindex."""
        # Initialize key variables
        oid_key = "ifIndex"
        oid = ".1.3.6.1.2.1.2.2.1.1"

        # Get results
        testobj = testimport.init_query(self.snmpobj_ifindex)
        results = testobj.ifindex()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

            # The ifIndex value must match that of the key.
            # We are keying off of the ifIndex so this must be true.
            self.assertEqual(key, value)

        # Test that we are getting the correct OID
        results = testobj.ifindex(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifphysaddress(self):
        """Testing function ifphysaddress."""
        # Initialize key variables
        oid_key = "ifPhysAddress"
        oid = ".1.3.6.1.2.1.2.2.1.6"

        # Get results
        testobj = testimport.init_query(self.snmpobj_binary)
        results = testobj.ifphysaddress()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifphysaddress(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifinmulticastpkts(self):
        """Testing function ifinmulticastpkts."""
        # Initialize key variables
        oid_key = "ifInMulticastPkts"
        oid = ".1.3.6.1.2.1.31.1.1.1.2"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifinmulticastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifinmulticastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifoutmulticastpkts(self):
        """Testing function ifoutmulticastpkts."""
        # Initialize key variables
        oid_key = "ifOutMulticastPkts"
        oid = ".1.3.6.1.2.1.31.1.1.1.4"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifoutmulticastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifoutmulticastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifinbroadcastpkts(self):
        """Testing function ifinbroadcastpkts."""
        # Initialize key variables
        oid_key = "ifInBroadcastPkts"
        oid = ".1.3.6.1.2.1.31.1.1.1.3"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifinbroadcastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifinbroadcastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifoutbroadcastpkts(self):
        """Testing function ifoutbroadcastpkts."""
        # Initialize key variables
        oid_key = "ifOutBroadcastPkts"
        oid = ".1.3.6.1.2.1.31.1.1.1.5"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = testobj.ifoutbroadcastpkts()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = testobj.ifoutbroadcastpkts(oidonly=True)
        self.assertEqual(results, oid)

    def test_ifstackstatus(self):
        """Testing function ifstackstatus."""
        pass

    def test__get_data(self):
        """Testing function _get_data."""
        # Tested by all other methods
        pass


if __name__ == "__main__":

    # Do the unit test
    unittest.main()
