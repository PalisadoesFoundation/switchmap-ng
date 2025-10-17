#!/usr/bin/env python3
"""Test the mib_ciscocdp module."""

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
from switchmap.poller.snmp.mib.cisco import mib_ciscocdp as testimport


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


class TestCiscoCDPFunctions(unittest.IsolatedAsyncioTestCase):
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


class TestCiscoCDP(unittest.IsolatedAsyncioTestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

    # Regular walk returning byte strings
    walk_results_string = {
        ".0.1.2.3.4.5.6.7.8.199.100": b"byte_string_1",
        ".0.1.2.3.4.5.6.7.8.299.200": b"byte_string_2",
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
        """Testing method / function layer1."""
        # Initializing key variables
        expected_dict = {
            199: {
                "cdpCacheDeviceId": "byte_string_1",
                "cdpCachePlatform": "byte_string_1",
                "cdpCacheDevicePort": "byte_string_1",
            },
            299: {
                "cdpCacheDeviceId": "byte_string_2",
                "cdpCachePlatform": "byte_string_2",
                "cdpCacheDevicePort": "byte_string_2",
            },
        }

        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        snmpobj.swalk = AsyncMock(return_value=self.walk_results_string)

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

    async def test_cdpcachedeviceid(self):
        """Testing method / function cdpcachedeviceid."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        snmpobj.swalk = AsyncMock(return_value=self.walk_results_string)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = await testobj.cdpcachedeviceid()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = await testobj.cdpcachedeviceid(oidonly=True)
        self.assertEqual(results, ".1.3.6.1.4.1.9.9.23.1.2.1.1.6")

    async def test_cdpcacheplatform(self):
        """Testing method / function cdpcacheplatform."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        snmpobj.swalk = AsyncMock(return_value=self.walk_results_string)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = await testobj.cdpcacheplatform()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = await testobj.cdpcacheplatform(oidonly=True)
        self.assertEqual(results, ".1.3.6.1.4.1.9.9.23.1.2.1.1.8")

    async def test_cdpcachedeviceport(self):
        """Testing method / function cdpcachedeviceport."""
        # Set the stage for SNMPwalk
        snmpobj = Mock(spec=Query)
        snmpobj.swalk = AsyncMock(return_value=self.walk_results_string)

        # Get results
        testobj = testimport.init_query(snmpobj)
        results = await testobj.cdpcachedeviceport()

        # Basic testing of results
        for key in results.keys():
            self.assertEqual(isinstance(key, int), True)

        # Test that we are getting the correct OID
        results = await testobj.cdpcachedeviceport(oidonly=True)
        self.assertEqual(results, ".1.3.6.1.4.1.9.9.23.1.2.1.1.7")

    def test__ifindex(self):
        """Testing method / function _ifindex."""
        # Initializing key variables
        oid = ".1.2.3.4.5.6.7.8.9.10"

        # Do test. Should return penultimate OID node.
        result = testimport._ifindex(oid)
        self.assertEqual(result, 9)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
