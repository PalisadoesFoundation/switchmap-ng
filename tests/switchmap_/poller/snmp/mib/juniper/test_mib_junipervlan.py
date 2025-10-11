#!/usr/bin/env python3
"""Test the mib_if module."""

import os
import sys
import unittest

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
{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp{0}mib{0}juniper\
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
from unittest.mock import MagicMock, patch, AsyncMock
from switchmap.poller.snmp.mib.juniper import mib_junipervlan as test_module


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


class TestJuniperVlanFunctions(unittest.IsolatedAsyncioTestCase):
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
        # Test that get_query returns the JuniperVlanQuery class
        result = test_module.get_query()
        self.assertEqual(result, test_module.JuniperVlanQuery)

    def test_init_query(self):
        """Testing function init_query."""
        # Test that init_query returns a JuniperVlanQuery instance
        mock_snmp_object = MagicMock()
        result = test_module.init_query(mock_snmp_object)
        self.assertIsInstance(result, test_module.JuniperVlanQuery)
        self.assertEqual(result.snmp_object, mock_snmp_object)


class TestJuniperVlan(unittest.IsolatedAsyncioTestCase):
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
        # Test class initialization
        mock_snmp_object = MagicMock()

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ) as mock_super_init:
            query = test_module.JuniperVlanQuery(mock_snmp_object)

            # Check that snmp_object is assigned
            self.assertEqual(query.snmp_object, mock_snmp_object)

            # Check that super().__init__ was called with correct parameters
            mock_super_init.assert_called_once_with(
                mock_snmp_object,
                ".1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3",
                tags=["layer1", "layer2"],
            )

            # Check initialization of instance variables
            self.assertIsNone(query.vlan_map)
            self.assertIsNone(query.baseportifindex)

    @patch("switchmap.poller.snmp.mib.juniper.mib_junipervlan.defaultdict")
    async def test_layer1(self, mock_defaultdict):
        """Testing function layer1."""
        # Test layer1 method
        mock_snmp_object = MagicMock()
        mock_final = MagicMock()
        mock_defaultdict.return_value = mock_final

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)

            # Mock dependency methods
            query._get_vlan_map = AsyncMock()
            query._get_bridge_data = AsyncMock()
            query.jnxexvlantag = AsyncMock(return_value={1: [100, 200]})
            query.jnxexvlanportaccessmode = AsyncMock(return_value={1: 1})

            result = await query.layer1()

            # Verify dependency methods were called
            query._get_vlan_map.assert_called_once()
            query._get_bridge_data.assert_called_once()
            query.jnxexvlantag.assert_called_once()
            query.jnxexvlanportaccessmode.assert_called_once()

            self.assertEqual(result, mock_final)

    @patch("switchmap.poller.snmp.mib.juniper.mib_junipervlan.defaultdict")
    async def test_layer2(self, mock_defaultdict):
        """Testing function layer2."""
        # Test layer2 method
        mock_snmp_object = MagicMock()
        mock_final = MagicMock()
        mock_defaultdict.return_value = mock_final

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)

            # Mock dependency methods
            query._get_vlan_map = AsyncMock()
            query.jnxexvlanname = AsyncMock(return_value={100: "VLAN_100"})

            result = await query.layer2()

            # Verify methods were called
            query._get_vlan_map.assert_called_once()
            query.jnxexvlanname.assert_called_once()

            self.assertEqual(result, mock_final)

    async def test_jnxexvlanportaccessmode(self):
        """Testing function jnxexvlanportaccessmode."""
        # Test jnxexvlanportaccessmode method
        mock_snmp_object = MagicMock()
        mock_snmp_object.swalk = AsyncMock(return_value={"1": 1, "2": 2})

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)
            query.baseportifindex = {1: 10, 2: 20}

            result = await query.jnxexvlanportaccessmode()

            # Verify swalk was called with correct OID
            mock_snmp_object.swalk.assert_called_once_with(
                ".1.3.6.1.4.1.2636.3.40.1.5.1.7.1.5", normalized=True
            )

            # Check result structure
            self.assertIsInstance(result, dict)

    async def test__get_vlan_map_supported(self):
        """Testing _get_vlan_map when supported."""
        # Test _get_vlan_map method
        mock_snmp_object = MagicMock()

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)
            query.supported = AsyncMock(return_value=True)
            query._vlanid2tag = AsyncMock(return_value={1: 100, 2: 200})

            await query._get_vlan_map()

            # Verify methods were called and vlan_map was set
            query.supported.assert_called_once()
            query._vlanid2tag.assert_called_once()
            self.assertEqual(query.vlan_map, {1: 100, 2: 200})

    async def test__get_bridge_data_supported(self):
        """Testing _get_bridge_data when both MIBs are supported."""
        # Test _get_bridge_data method
        mock_snmp_object = MagicMock()

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ), patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.BridgeQuery"
        ) as mock_bridge_class:

            query = test_module.JuniperVlanQuery(mock_snmp_object)
            query.baseportifindex = None
            query.supported = AsyncMock(return_value=True)

            # Mock BridgeQuery instance
            mock_bridge_instance = AsyncMock()
            mock_bridge_instance.supported = AsyncMock(return_value=True)
            mock_bridge_instance.dot1dbaseport_2_ifindex = AsyncMock(
                return_value={1: 10, 2: 20}
            )
            mock_bridge_class.return_value = mock_bridge_instance

            await query._get_bridge_data()

            # Verify BridgeQuery was created and methods called
            mock_bridge_class.assert_called_once_with(mock_snmp_object)
            query.supported.assert_called_once()
            mock_bridge_instance.supported.assert_called_once()
            mock_bridge_instance.dot1dbaseport_2_ifindex.assert_called_once()

            # Verify baseportifindex was set
            self.assertEqual(query.baseportifindex, {1: 10, 2: 20})

    async def test__get_bridge_data_not_supported(self):
        """Testing _get_bridge_data when not supported."""
        # Test _get_bridge_data method when not supported
        mock_snmp_object = MagicMock()

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ), patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.BridgeQuery"
        ) as mock_bridge_class:

            query = test_module.JuniperVlanQuery(mock_snmp_object)
            query.baseportifindex = None
            query.supported = AsyncMock(return_value=False)

            mock_bridge_instance = AsyncMock()
            mock_bridge_class.return_value = mock_bridge_instance

            await query._get_bridge_data()

            # Verify baseportifindex was set to empty dict
            self.assertEqual(query.baseportifindex, {})

    async def test_jnxexvlantag(self):
        """Testing function jnxexvlantag."""
        # Test jnxexvlantag method
        mock_snmp_object = MagicMock()
        mock_swalk_data = {
            ".1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3.100.1": "test_value1",
            ".1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3.200.2": "test_value2",
        }
        mock_snmp_object.swalk = AsyncMock(return_value=mock_swalk_data)

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)

            # Set up required instance variables
            query.vlan_map = {100: 10, 200: 20}
            query.baseportifindex = {1: 101, 2: 102}

            result = await query.jnxexvlantag()

            # Verify swalk was called with correct OID
            mock_snmp_object.swalk.assert_called_once_with(
                ".1.3.6.1.4.1.2636.3.40.1.5.1.7.1.3", normalized=False
            )

            # Check result structure - should be dict with ifindex as key
            self.assertIsInstance(result, dict)
            # Expected: {101: [10], 102: [20]} based on the mappings
            expected_result = {101: [10], 102: [20]}
            self.assertEqual(result, expected_result)

    async def test_jnxexvlanname(self):
        """Testing function jnxexvlanname."""
        # Test jnxexvlanname method
        mock_snmp_object = MagicMock()
        mock_swalk_data = {"100": b"VLAN_100", "200": b"VLAN_200"}
        mock_snmp_object.swalk = AsyncMock(return_value=mock_swalk_data)

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)

            # Set up vlan_map
            query.vlan_map = {100: 10, 200: 20}

            result = await query.jnxexvlanname()

            # Verify swalk was called with correct OID
            mock_snmp_object.swalk.assert_called_once_with(
                ".1.3.6.1.4.1.2636.3.40.1.5.1.5.1.2", normalized=True
            )

            # Check result - should be dict with vlan_tag as key and string name as value
            self.assertIsInstance(result, dict)
            expected_result = {10: "VLAN_100", 20: "VLAN_200"}
            self.assertEqual(result, expected_result)

    async def test__vlanid2tag(self):
        """Testing function _vlanid2tag."""
        # Test _vlanid2tag method
        mock_snmp_object = MagicMock()
        mock_snmp_object.swalk = AsyncMock(return_value={"1": 100, "2": 200})

        with patch(
            "switchmap.poller.snmp.mib.juniper.mib_junipervlan.Query.__init__"
        ):
            query = test_module.JuniperVlanQuery(mock_snmp_object)

            result = await query._vlanid2tag()

            # Verify swalk was called with correct OID
            mock_snmp_object.swalk.assert_called_once_with(
                ".1.3.6.1.4.1.2636.3.40.1.5.1.5.1.5", normalized=True
            )

            # Check result - should be a dict with int keys and values
            self.assertIsInstance(result, dict)
            expected = {1: 100, 2: 200}
            self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
