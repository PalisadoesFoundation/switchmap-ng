#!/usr/bin/env python3
"""Test the mib_bridge module."""

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
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)

from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.poller.snmp.mib.generic import mib_bridge as testimport


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


class TestMibBridgeFunctions(unittest.IsolatedAsyncioTestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        CONFIG.cleanup()

    def test_get_query(self):
        """Testing function get_query."""
        result = testimport.get_query()
        self.assertEqual(result, testimport.BridgeQuery)

    def test_init_query(self):
        """Testing function init_query."""
        mock_snmp = Mock(spec=Query)
        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.BridgeQuery)
        self.assertEqual(result.snmp_object, mock_snmp)

    def test__cisco_vlan_context(self):
        """Testing function _cisco_vlan_context."""
        # Test older style
        result = testimport._cisco_vlan_context(10, 0)
        self.assertEqual(result, "10")

        # Test newer style
        result = testimport._cisco_vlan_context(20, 1)
        self.assertEqual(result, "vlan-20")

    def test__snmp_octetstr_2_string(self):
        """Testing function _snmp_octetstr_2_string."""
        # Test with UTF-8 encoded bytes
        binary_value = b"test"
        result = testimport._snmp_octetstr_2_string(binary_value)
        self.assertEqual(result, "74657374")


class TestMibBridge(unittest.IsolatedAsyncioTestCase):
    """Checks all methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        CONFIG.cleanup()

    def test___init__(self):
        """Testing function __init__."""
        mock_snmp = Mock(spec=Query)
        bridge = testimport.BridgeQuery(mock_snmp)
        self.assertEqual(bridge.snmp_object, mock_snmp)
        self.assertIsNone(bridge._ifindex)

    async def test_layer1(self):
        """Testing function layer1."""
        mock_snmp = Mock(spec=Query)
        bridge = testimport.BridgeQuery(mock_snmp)

        # Mock _macaddresstable
        bridge._macaddresstable = AsyncMock(
            return_value={1: {"l1_macs": ["aabbccddeeff"]}}
        )

        result = await bridge.layer1()
        self.assertEqual(result, {1: {"l1_macs": ["aabbccddeeff"]}})

    async def test__macaddresstable_cisco(self):
        """Testing function _macaddresstable for Cisco."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(side_effect=[True, False])

        bridge = testimport.BridgeQuery(mock_snmp)
        bridge._macaddresstable_cisco = AsyncMock(
            return_value={1: {"l1_macs": ["001122334455"]}}
        )

        result = await bridge._macaddresstable()

        self.assertEqual(result, {1: {"l1_macs": ["001122334455"]}})
        bridge._macaddresstable_cisco.assert_called_once()

    async def test__macaddresstable_juniper(self):
        """Testing function _macaddresstable for Juniper."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(side_effect=[False, True])

        bridge = testimport.BridgeQuery(mock_snmp)
        bridge._macaddresstable_juniper = AsyncMock(
            return_value={1: {"l1_macs": ["665544332211"]}}
        )

        result = await bridge._macaddresstable()

        self.assertEqual(result, {1: {"l1_macs": ["665544332211"]}})
        bridge._macaddresstable_juniper.assert_called_once()

    async def test__macaddresstable_cisco_full(self):
        """Testing full Cisco MAC address table."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(return_value=True)
        mock_snmp.swalk = AsyncMock(
            side_effect=[
                {1: 1, 10: 1},
                {1: 1, 10: 1},
            ]
        )

        bridge = testimport.BridgeQuery(mock_snmp)

        # Mock the helper methods
        bridge._cisco_context_style = AsyncMock(return_value=0)
        bridge._dot1dtpfdbaddress = AsyncMock(
            return_value={
                ".1.2.3.4.5.6": "010203040506",
                ".7.8.9.10.11.12": "0708090a0b0c",
                ".13.14.15.16.17.18": "0d0e0f101112",
                ".19.20.21.22.23.24": "131415161718",
            }
        )
        bridge._dot1dtpfdbport = AsyncMock(
            return_value={
                ".1.2.3.4.5.6": 1,
                ".7.8.9.10.11.12": 1,
                ".13.14.15.16.17.18": 2,
                ".19.20.21.22.23.24": 0,
            }
        )
        bridge.dot1dbaseport_2_ifindex = AsyncMock(return_value={1: 10, 2: 0})

        result = await bridge._macaddresstable_cisco()

        self.assertIn(10, result)
        self.assertIn("l1_macs", result[10])
        # Two MACs should be on port 10
        self.assertEqual(len(result[10]["l1_macs"]), 2)

    async def test__macaddresstable_juniper_full(self):
        """Testing full Juniper MAC address table."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(return_value=True)
        mock_snmp.swalk = AsyncMock(return_value={1: b"vlan1"})

        bridge = testimport.BridgeQuery(mock_snmp)

        bridge._dot1qtpfdbport = AsyncMock(
            return_value={
                ".1.0.1.2.3.4.5.6": 1,
                ".1.0.7.8.9.10.11.12": 1,
            }
        )
        bridge.dot1dbaseport_2_ifindex = AsyncMock(return_value={1: 10})

        result = await bridge._macaddresstable_juniper()

        self.assertIn(10, result)
        self.assertIn("l1_macs", result[10])
        # Two MACs should be on port 10
        self.assertEqual(len(result[10]["l1_macs"]), 2)

    async def test__dot1dtpfdbport(self):
        """Testing function _dot1dtpfdbport."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            return_value={".1.3.6.1.2.1.17.4.3.1.2.1.2.3.4.5.6": 5}
        )

        bridge = testimport.BridgeQuery(mock_snmp)
        result = await bridge._dot1dtpfdbport()

        self.assertIn(".1.2.3.4.5.6", result)
        self.assertEqual(result[".1.2.3.4.5.6"], 5)

    async def test__dot1dtpfdbport_with_contexts(self):
        """Testing function _dot1dtpfdbport with context names."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            return_value={".1.3.6.1.2.1.17.4.3.1.2.1.2.3.4.5.6": 3}
        )

        bridge = testimport.BridgeQuery(mock_snmp)
        result = await bridge._dot1dtpfdbport(context_names=["vlan-10"])

        self.assertIn(".1.2.3.4.5.6", result)

    async def test__dot1qtpfdbport(self):
        """Testing function _dot1qtpfdbport."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(return_value=True)
        mock_snmp.swalk = AsyncMock(
            side_effect=[
                {1: b"default"},
                {".1.3.6.1.2.1.17.7.1.2.2.1.2.1.10.20.30.40.50.60": 2},
            ]
        )

        bridge = testimport.BridgeQuery(mock_snmp)
        result = await bridge._dot1qtpfdbport()

        self.assertIn(".1.10.20.30.40.50.60", result)

    async def test__dot1qtpfdbport_no_oid(self):
        """Testing function _dot1qtpfdbport when OID doesn't exist."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.oid_exists = AsyncMock(return_value=False)

        bridge = testimport.BridgeQuery(mock_snmp)
        result = await bridge._dot1qtpfdbport()

        self.assertEqual(len(result), 0)

    async def test__dot1dtpfdbaddress(self):
        """Testing function _dot1dtpfdbaddress."""
        mock_snmp = Mock(spec=Query)
        oid_key = ".1.3.6.1.2.1.17.4.3.1.1.1.2.3.4.5.6"
        mock_snmp.swalk = AsyncMock(
            return_value={oid_key: b"\x01\x02\x03\x04\x05\x06"}
        )

        bridge = testimport.BridgeQuery(mock_snmp)

        patch_path = "switchmap.poller.snmp.mib.generic.mib_bridge.general"
        with patch(f"{patch_path}.octetstr_2_string") as mock_convert:
            mock_convert.return_value = "010203040506"
            result = await bridge._dot1dtpfdbaddress()

            self.assertIn(".1.2.3.4.5.6", result)
            self.assertEqual(result[".1.2.3.4.5.6"], "010203040506")

    async def test__dot1dtpfdbaddress_with_contexts(self):
        """Testing function _dot1dtpfdbaddress with contexts."""
        mock_snmp = Mock(spec=Query)
        oid_key = ".1.3.6.1.2.1.17.4.3.1.1.6.5.4.3.2.1"
        mock_snmp.swalk = AsyncMock(
            return_value={oid_key: b"\x06\x05\x04\x03\x02\x01"}
        )

        bridge = testimport.BridgeQuery(mock_snmp)

        patch_path = "switchmap.poller.snmp.mib.generic.mib_bridge.general"
        with patch(f"{patch_path}.octetstr_2_string") as mock_convert:
            mock_convert.return_value = "060504030201"
            result = await bridge._dot1dtpfdbaddress(context_names=["10"])

            self.assertIn(".6.5.4.3.2.1", result)

    async def test_dot1dbaseport_2_ifindex(self):
        """Testing function dot1dbaseport_2_ifindex."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            side_effect=[
                {1: 1, 2: 2, 3: 3},
                {1: 1},
            ]
        )

        bridge = testimport.BridgeQuery(mock_snmp)
        result = await bridge.dot1dbaseport_2_ifindex()

        # offset = 1 - 1 = 0, so bridge_port = ifindex - 0
        self.assertEqual(result[1], 1)
        self.assertEqual(result[2], 2)
        self.assertEqual(result[3], 3)

    async def test_dot1dbaseport_2_ifindex_with_contexts(self):
        """Testing function dot1dbaseport_2_ifindex with contexts."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            side_effect=[
                {1: 1, 2: 2},
                {1: 1},
            ]
        )

        bridge = testimport.BridgeQuery(mock_snmp)
        result = await bridge.dot1dbaseport_2_ifindex(context_names=["vlan-10"])

        self.assertIn(1, result)

    async def test__cisco_context_style(self):
        """Testing function _cisco_context_style."""
        mock_snmp = Mock(spec=Query)
        bridge = testimport.BridgeQuery(mock_snmp)

        # Mock _dot1dtpfdbaddress to return data on first style
        bridge._dot1dtpfdbaddress = AsyncMock(
            side_effect=[{".1.2.3": "mac"}, {}]
        )

        result = await bridge._cisco_context_style(10)

        self.assertEqual(result, 0)

    async def test__cisco_context_style_second(self):
        """Testing function _cisco_context_style finding second style."""
        mock_snmp = Mock(spec=Query)
        bridge = testimport.BridgeQuery(mock_snmp)

        # Return empty first, then data
        bridge._dot1dtpfdbaddress = AsyncMock(
            side_effect=[{}, {".1.2.3": "mac"}]
        )

        result = await bridge._cisco_context_style(10)

        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
