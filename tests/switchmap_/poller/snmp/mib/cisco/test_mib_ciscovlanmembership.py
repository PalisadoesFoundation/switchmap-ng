#!/usr/bin/env python3
"""Test the mib_ciscovlanmembership module."""

import os
import sys
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
from switchmap.poller.snmp.mib.cisco import (
    mib_ciscovlanmembership as testimport,
)


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


class TestMibCiscoVlanMemberFunctions(unittest.IsolatedAsyncioTestCase):
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


class TestMibCiscoVlanMember(unittest.IsolatedAsyncioTestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Normalized walk returning integers
    nwalk_results_integer = {100: 1234, 200: 4567}

    # Set the stage for SNMPwalk for integer results
    snmpobj_integer = Mock(spec=Query)
    snmpobj_integer.swalk = AsyncMock(return_value=nwalk_results_integer)
    snmpobj_integer.walk = AsyncMock(return_value=nwalk_results_integer)

    # Initializing key variables
    expected_dict = {
        100: {"vmPortStatus": 1234, "vmVlan": 1234},
        200: {"vmPortStatus": 4567, "vmVlan": 4567},
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

    async def test_supported(self):
        """Testing method / function supported."""
        # Set the stage for oid_exists returning True
        snmpobj = Mock(spec=Query)
        snmpobj.oid_exists = AsyncMock(return_value=True)

        # Test supported
        testobj = testimport.init_query(snmpobj)
        self.assertEqual(await testobj.supported(), True)

        # Set the stage for oid_exists returning False
        snmpobj.oid_exists = AsyncMock(return_value=False)

        # Test unsupported
        testobj = testimport.init_query(snmpobj)
        self.assertEqual(await testobj.supported(), False)

    async def test_layer1(self):
        """Testing function layer1."""
        # Initializing key variables
        expected_dict = {
            100: {"vmPortStatus": 1234, "vmVlan": 1234},
            200: {"vmPortStatus": 4567, "vmVlan": 4567},
        }

        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        snmpobj.swalk = AsyncMock(return_value=self.nwalk_results_integer)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = await testobj.layer1()

        # Basic testing of results
        for primary in results.keys():
            for secondary in results[primary].keys():
                self.assertEqual(
                    results[primary][secondary],
                    expected_dict[primary][secondary],
                )

    async def test_vmvlan(self):
        """Testing function vmvlan."""
        oid_key = "vmVlan"
        oid = ".1.3.6.1.4.1.9.9.68.1.2.2.1.2"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vmvlan()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vmvlan(oidonly=True)
        self.assertEqual(results, oid)

    async def test_vmportstatus(self):
        """Testing function vmportstatus."""
        # Initialize key variables
        oid_key = "vmPortStatus"
        oid = ".1.3.6.1.4.1.9.9.68.1.2.2.1.3"

        # Get results
        testobj = testimport.init_query(self.snmpobj_integer)
        results = await testobj.vmportstatus()

        # Basic testing of results
        for key, value in results.items():
            self.assertEqual(isinstance(key, int), True)
            self.assertEqual(value, self.expected_dict[key][oid_key])

        # Test that we are getting the correct OID
        results = await testobj.vmportstatus(oidonly=True)
        self.assertEqual(results, oid)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
