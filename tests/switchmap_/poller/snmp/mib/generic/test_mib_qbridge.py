#!/usr/bin/env python3
"""Test the mib_qbridge module."""

import unittest
import os
import sys
from unittest.mock import Mock, AsyncMock, patch

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
from switchmap.poller.snmp.mib.generic import mib_qbridge as testimport


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


class TestMibQBridgeFunctions(unittest.TestCase):
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
        # Test that get_query returns the QbridgeQuery class
        result = testimport.get_query()
        self.assertEqual(result, testimport.QbridgeQuery)

    def test_init_query(self):
        """Testing function init_query."""
        # Create a mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Test that init_query returns an instance of QbridgeQuery
        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.QbridgeQuery)
        self.assertEqual(result.snmp_object, mock_snmp)


class TestMibQBridge(unittest.IsolatedAsyncioTestCase):
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

    def test___init__(self):
        """Testing function __init__."""
        # Create a mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Initialize QbridgeQuery
        qbridge = testimport.QbridgeQuery(mock_snmp)

        self.assertEqual(qbridge.snmp_object, mock_snmp)
        self.assertIsNone(qbridge.baseportifindex)

    async def test__get_bridge_data_supported(self):
        """Testing function _get_bridge_data when both MIBs are supported."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(return_value=True)

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        qbridge.supported = AsyncMock(return_value=True)
        mock_bridge = Mock()
        mock_bridge.supported = AsyncMock(return_value=True)
        mock_bridge.dot1dbaseport_2_ifindex = AsyncMock(
            return_value={1: 10, 2: 20, 3: 30}
        )

        # Patch BridgeQuery to return our mock
        with patch(
            "switchmap.poller.snmp.mib.generic.mib_qbridge.BridgeQuery",
            return_value=mock_bridge,
        ):
            await qbridge._get_bridge_data()

        self.assertEqual(qbridge.baseportifindex, {1: 10, 2: 20, 3: 30})

    async def test__get_bridge_data_not_supported(self):
        """Testing function _get_bridge_data when MIB is not supported."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(return_value=False)

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)
        qbridge.supported = AsyncMock(return_value=False)
        mock_bridge = Mock()
        mock_bridge.supported = AsyncMock(return_value=False)

        # Patch BridgeQuery to return our mock
        with patch(
            "switchmap.poller.snmp.mib.generic.mib_qbridge.BridgeQuery",
            return_value=mock_bridge,
        ):
            await qbridge._get_bridge_data()

        self.assertEqual(qbridge.baseportifindex, {})

    async def test__get_bridge_data_cached(self):
        """Testing function _get_bridge_data when data is already cached."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)
        qbridge.baseportifindex = {1: 10, 2: 20}

        qbridge.supported = AsyncMock(return_value=True)
        await qbridge._get_bridge_data()

        # Verify supported was not called (because data was cached)
        qbridge.supported.assert_not_called()

        # Verify baseportifindex remains unchanged
        self.assertEqual(qbridge.baseportifindex, {1: 10, 2: 20})

    async def test_layer1(self):
        """Testing function layer1."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 100, 2: 200})

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        # Set baseportifindex to simulate cached data
        qbridge.baseportifindex = {1: 10, 2: 20}

        # Call layer1
        result = await qbridge.layer1()

        # Verify result structure
        self.assertIn(10, result)
        self.assertIn(20, result)
        self.assertEqual(result[10]["dot1qPvid"], 100)
        self.assertEqual(result[20]["dot1qPvid"], 200)

    async def test_layer2(self):
        """Testing function layer2."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            return_value={1: b"default", 10: b"management"}
        )

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        # Call layer2
        result = await qbridge.layer2()

        # Verify result structure
        self.assertIn(1, result)
        self.assertIn(10, result)
        self.assertEqual(result[1]["dot1qVlanStaticName"], "default")
        self.assertEqual(result[10]["dot1qVlanStaticName"], "management")

    async def test_dot1qpvid(self):
        """Testing function dot1qpvid."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 100, 2: 200, 3: 300})

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        # Set baseportifindex mapping
        qbridge.baseportifindex = {1: 10, 2: 20, 3: 30}

        # Call dot1qpvid
        result = await qbridge.dot1qpvid()

        # Verify result - baseport mapped to ifindex
        self.assertEqual(result[10], 100)
        self.assertEqual(result[20], 200)
        self.assertEqual(result[30], 300)

    async def test_dot1qpvid_oidonly(self):
        """Testing function dot1qpvid with oidonly=True."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        # Call dot1qpvid with oidonly=True
        result = await qbridge.dot1qpvid(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.2.1.17.7.1.4.5.1.1")

    async def test_dot1qpvid_missing_ifindex(self):
        """Testing function dot1qpvid when ifindex mapping is missing."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 100, 2: 200, 5: 500})

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        # Set baseportifindex mapping (missing entry for key 5)
        qbridge.baseportifindex = {1: 10, 2: 20}

        result = await qbridge.dot1qpvid()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[10], 100)
        self.assertEqual(result[20], 200)
        self.assertNotIn(500, result)

    async def test_dot1qvlanstaticname(self):
        """Testing function dot1qvlanstaticname."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            return_value={1: b"default", 10: b"management", 100: b"guest"}
        )

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        result = await qbridge.dot1qvlanstaticname()

        self.assertEqual(result[1], "default")
        self.assertEqual(result[10], "management")
        self.assertEqual(result[100], "guest")

    async def test_dot1qvlanstaticname_oidonly(self):
        """Testing function dot1qvlanstaticname with oidonly=True."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create QbridgeQuery instance
        qbridge = testimport.QbridgeQuery(mock_snmp)

        result = await qbridge.dot1qvlanstaticname(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.2.1.17.7.1.4.3.1.1")


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
