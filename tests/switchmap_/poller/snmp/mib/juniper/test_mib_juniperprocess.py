#!/usr/bin/env python3
"""Test the mib_juniperprocess module."""

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
from switchmap.poller.snmp.mib.juniper import mib_juniperprocess as testimport


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


class TestMibJuniperProcessFunctions(unittest.TestCase):
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
        # Cleanup the configuration
        CONFIG.cleanup()

    def test_get_query(self):
        """Testing function get_query."""
        # Test that get_query returns the JuniperProcessQuery class
        result = testimport.get_query()
        self.assertEqual(result, testimport.JuniperProcessQuery)

    def test_init_query(self):
        """Testing function init_query."""
        # Create a mock SNMP object
        mock_snmp = Mock(spec=Query)

        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.JuniperProcessQuery)
        self.assertEqual(result.snmp_object, mock_snmp)


class TestMibJuniperProcess(unittest.IsolatedAsyncioTestCase):
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

        # Initialize JuniperProcessQuery
        juniper = testimport.JuniperProcessQuery(mock_snmp)

        self.assertEqual(juniper.snmp_object, mock_snmp)

    async def test_system_success(self):
        """Testing function system with successful data retrieval."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock()

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)

        # Mock the individual methods
        juniper.operatingcpu = AsyncMock(return_value={1: 25, 2: 30})
        juniper.operatingmemoryused = AsyncMock(return_value=8192)
        juniper.operatingmemoryfree = AsyncMock(return_value=2048)

        result = await juniper.system()

        self.assertIn("JUNIPER-MIB", result)
        self.assertIn("jnxOperatingCPU", result["JUNIPER-MIB"])
        self.assertIn("jnxOperatingMemoryUsed", result["JUNIPER-MIB"])
        self.assertIn("jnxOperatingMemoryFree", result["JUNIPER-MIB"])

        self.assertEqual(
            result["JUNIPER-MIB"]["jnxOperatingCPU"], {1: 25, 2: 30}
        )
        self.assertEqual(result["JUNIPER-MIB"]["jnxOperatingMemoryUsed"], 8192)
        self.assertEqual(result["JUNIPER-MIB"]["jnxOperatingMemoryFree"], 2048)

    async def test_system_with_none_values(self):
        """Testing function system when methods return None."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)

        # Mock methods to return None
        juniper.operatingcpu = AsyncMock(return_value=None)
        juniper.operatingmemoryused = AsyncMock(return_value=None)
        juniper.operatingmemoryfree = AsyncMock(return_value=None)

        result = await juniper.system()
        # Empty defaultdict when all methods return None
        self.assertEqual(len(result), 0)

    async def test_system_with_exceptions(self):
        """Testing function system when methods raise exceptions."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)

        # Mock methods to raise exceptions
        juniper.operatingcpu = AsyncMock(side_effect=Exception("CPU error"))
        juniper.operatingmemoryused = AsyncMock(return_value=8192)
        juniper.operatingmemoryfree = AsyncMock(return_value=2048)

        result = await juniper.system()

        self.assertIn("JUNIPER-MIB", result)
        self.assertNotIn("jnxOperatingCPU", result["JUNIPER-MIB"])
        self.assertIn("jnxOperatingMemoryUsed", result["JUNIPER-MIB"])
        self.assertIn("jnxOperatingMemoryFree", result["JUNIPER-MIB"])

    async def test_system_with_outer_exception(self):
        """Testing function system when asyncio.gather itself fails."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)

        # Mock asyncio.gather to raise an exception
        juniper_path = "switchmap.poller.snmp.mib.juniper.mib_juniperprocess"
        with patch(
            f"{juniper_path}.asyncio.gather",
            side_effect=Exception("Gather failed"),
        ):
            result = await juniper.system()

            self.assertEqual(len(result), 0)

    async def test_operatingcpu(self):
        """Testing function operatingcpu."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 25, 2: 30, 3: 15})

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)

        result = await juniper.operatingcpu()

        self.assertEqual(result[1], 25)
        self.assertEqual(result[2], 30)
        self.assertEqual(result[3], 15)

    async def test_operatingcpu_oidonly(self):
        """Testing function operatingcpu with oidonly=True."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)
        result = await juniper.operatingcpu(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.4.1.2636.3.1.13.1.8")

    async def test_operatingmemoryused(self):
        """Testing function operatingmemoryused."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 4096, 2: 2048, 3: 2048})

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)
        result = await juniper.operatingmemoryused()

        self.assertEqual(result, 8192)

    async def test_operatingmemoryused_oidonly(self):
        """Testing function operatingmemoryused with oidonly=True."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)
        result = await juniper.operatingmemoryused(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.4.1.2636.3.1.13.1.11")

    async def test_operatingmemoryfree(self):
        """Testing function operatingmemoryfree."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 512, 2: 768, 3: 768})

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)
        result = await juniper.operatingmemoryfree()

        self.assertEqual(result, 2048)

    async def test_operatingmemoryfree_oidonly(self):
        """Testing function operatingmemoryfree with oidonly=True."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)
        result = await juniper.operatingmemoryfree(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.4.1.2636.3.1.13.1.12")

    async def test_operatingmemoryfree_empty_results(self):
        """Testing function operatingmemoryfree with empty results."""
        # Create mock SNMP object
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={})

        # Create JuniperProcessQuery instance
        juniper = testimport.JuniperProcessQuery(mock_snmp)
        result = await juniper.operatingmemoryfree()

        self.assertEqual(result, 0)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
