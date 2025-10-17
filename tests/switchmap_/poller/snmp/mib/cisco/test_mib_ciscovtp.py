#!/usr/bin/env python3
"""Test the mib_if module."""

import os
import sys
import binascii
import unittest
from unittest.mock import Mock, AsyncMock

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
{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp{0}mib{0}cisco\
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
from switchmap.poller.snmp.mib.cisco import mib_ciscovtp as testimport


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
        """Do a failable SNMPwalk.

        Args:
            None

        Returns:
            None
        """
        pass


class TestMibCiscoVTPFunctions(unittest.IsolatedAsyncioTestCase):
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


class TestMibCiscoVTP(unittest.IsolatedAsyncioTestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Normalized walk returning integers
    nwalk_results_integer = {100: 1234, 200: 5678}

    # Set the stage for SNMPwalk for integer results
    snmpobj_integer = Mock(spec=Query)
    snmpobj_integer.swalk = AsyncMock(return_value=nwalk_results_integer)
    snmpobj_integer.walk = AsyncMock(return_value=nwalk_results_integer)

    # Normalized walk returning integers for the ifIndex
    nwalk_results_ifindex = {100: 100, 200: 200}

    # Set the stage for SNMPwalk for integer results for the ifIndex
    snmpobj_ifindex = Mock(spec=Query)
    snmpobj_ifindex.swalk = AsyncMock(return_value=nwalk_results_ifindex)
    snmpobj_ifindex.walk = AsyncMock(return_value=nwalk_results_ifindex)

    # Normalized walk returning strings
    nwalk_results_bytes = {100: b"1234", 200: b"5678"}

    # Set the stage for SNMPwalk for string results
    snmpobj_bytes = Mock(spec=Query)
    snmpobj_bytes.swalk = AsyncMock(return_value=nwalk_results_bytes)
    snmpobj_bytes.walk = AsyncMock(return_value=nwalk_results_bytes)

    # Normalized walk returning binary data
    nwalk_results_binary = {
        100: binascii.unhexlify("1234"),
        200: binascii.unhexlify("5678"),
    }

    # Set the stage for SNMPwalk for binary results
    snmpobj_binary = Mock(spec=Query)
    snmpobj_binary.swalk = AsyncMock(return_value=nwalk_results_binary)
    snmpobj_binary.walk = AsyncMock(return_value=nwalk_results_binary)

    # Initializing key variables
    expected_dict = {
        100: {
            "vlanTrunkPortDynamicState": 1234,
            "vlanTrunkPortDynamicStatus": 1234,
            "vlanTrunkPortNativeVlan": 1234,
            "vlanTrunkPortEncapsulationType": 1234,
            "vlanTrunkPortVlansEnabled": 1234,
            "vtpVlanType": "1234",
            "vtpVlanName": "1234",
            "vtpVlanState": 1234,
        },
        200: {
            "vlanTrunkPortDynamicState": 5678,
            "vlanTrunkPortDynamicStatus": 5678,
            "vlanTrunkPortNativeVlan": 5678,
            "vlanTrunkPortEncapsulationType": 5678,
            "vlanTrunkPortVlansEnabled": 5678,
            "vtpVlanType": "5678",
            "vtpVlanName": "5678",
            "vtpVlanState": 5678,
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

    def test_layer2(self):
        """Testing function layer2."""
        # Layer 2 testing only seems to work when all the methods return
        # the same type of results (eg. int, string, hex)
        pass

    def test_layer1(self):
        """Testing function layer1."""
        # Layer 1 testing only seems to work when all the methods return
        # the same type of results (eg. int, string, hex)
        pass

    async def test_vlantrunkportencapsulationtype(self):
        """Testing function vlantrunkportencapsulationtype."""
        # Initialize key variables
        oid_key = "vlanTrunkPortEncapsulationType"
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.3"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vlantrunkportencapsulationtype()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vlantrunkportencapsulationtype(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vlantrunkportnativevlan(self):
        """Testing function vlantrunkportnativevlan."""
        # Initialize key variables
        oid_key = "vlanTrunkPortNativeVlan"
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.5"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vlantrunkportnativevlan()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vlantrunkportnativevlan(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vlantrunkportdynamicstatus(self):
        """Testing function vlantrunkportdynamicstatus."""
        # Initialize key variables
        oid_key = "vlanTrunkPortDynamicStatus"
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.14"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vlantrunkportdynamicstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vlantrunkportdynamicstatus(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vlantrunkportdynamicstate(self):
        """Testing function vlantrunkportdynamicstate."""
        # Initialize key variables
        oid_key = "vlanTrunkPortDynamicState"
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.13"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vlantrunkportdynamicstate()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vlantrunkportdynamicstate(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vtpvlanname(self):
        """Testing function vtpvlanname."""
        # Initialize key variables
        oid_key = "vtpVlanName"
        oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.4"

        # Get results
        testobj = testimport.init_query(self.snmpobj_bytes)
        results = await testobj.vtpvlanname()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vtpvlanname(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vtpvlantype(self):
        """Testing function vtpvlantype."""
        # Initialize key variables
        oid_key = "vtpVlanType"
        oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.3"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vtpvlantype()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vtpvlantype(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vtpvlanstate(self):
        """Testing function vtpvlanstate."""
        # Initialize key variables
        oid_key = "vtpVlanState"
        oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.2"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vtpvlanstate()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vtpvlanstate(oidonly=True)
        self.assertEqual(results, oid)

    def test_vlantrunkportvlansenabled(self):
        """Testing function vlantrunkportvlansenabled."""
        pass


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
