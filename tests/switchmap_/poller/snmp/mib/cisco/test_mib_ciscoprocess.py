#!/usr/bin/env python3
"""Test the mib_ciscoprocess module."""

import os
import sys
import unittest
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
{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp{0}mib{0}cisco\
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

from switchmap.poller.snmp.mib.cisco import mib_ciscoprocess as testimport


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


class TestCiscoProcessQueryFunctions(unittest.IsolatedAsyncioTestCase):
    """Checks all methods."""

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
        self.assertEqual(result, testimport.CiscoProcessQuery)

    def test_init_query(self):
        """Testing function init_query."""
        mock_snmp = Mock(spec=Query)
        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.CiscoProcessQuery)
        self.assertEqual(result.snmp_object, mock_snmp)


class TestCiscoProcessQuery(unittest.IsolatedAsyncioTestCase):
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
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        self.assertEqual(cisco_process.snmp_object, mock_snmp)

    async def test_system_success(self):
        """Testing function system with successful data."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        cisco_process.cpmcputotal5minrev = AsyncMock(return_value={1: 25})
        cisco_process.memorypoolused = AsyncMock(return_value=8192000)
        cisco_process.memorypoolfree = AsyncMock(return_value=2048000)

        result = await cisco_process.system()

        self.assertIn("CISCO-PROCESS-MIB", result)
        data = result["CISCO-PROCESS-MIB"]
        self.assertIn("cpmCPUTotal5minRev", data)
        self.assertIn("ciscoMemoryPoolUsed", data)
        self.assertIn("ciscoMemoryPoolFree", data)
        self.assertEqual(data["cpmCPUTotal5minRev"], {1: 25})
        self.assertEqual(data["ciscoMemoryPoolUsed"], 8192000)
        self.assertEqual(data["ciscoMemoryPoolFree"], 2048000)

    async def test_system_with_none_values(self):
        """Testing function system when methods return None."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        cisco_process.cpmcputotal5minrev = AsyncMock(return_value=None)
        cisco_process.memorypoolused = AsyncMock(return_value=None)
        cisco_process.memorypoolfree = AsyncMock(return_value=None)

        result = await cisco_process.system()

        self.assertEqual(len(result), 0)

    async def test_system_with_exceptions(self):
        """Testing function system when methods raise exceptions."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        cisco_process.cpmcputotal5minrev = AsyncMock(
            side_effect=Exception("CPU error")
        )
        cisco_process.memorypoolused = AsyncMock(return_value=8192000)
        cisco_process.memorypoolfree = AsyncMock(return_value=2048000)

        result = await cisco_process.system()

        self.assertIn("CISCO-PROCESS-MIB", result)
        self.assertNotIn("cpmCPUTotal5minRev", result["CISCO-PROCESS-MIB"])
        self.assertIn("ciscoMemoryPoolUsed", result["CISCO-PROCESS-MIB"])
        self.assertIn("ciscoMemoryPoolFree", result["CISCO-PROCESS-MIB"])

    async def test_system_with_outer_exception(self):
        """Testing function system with outer exception."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        cisco_path = "switchmap.poller.snmp.mib.cisco.mib_ciscoprocess"
        with patch(
            f"{cisco_path}.asyncio.gather",
            side_effect=Exception("Gather failed"),
        ):
            result = await cisco_process.system()

            self.assertEqual(len(result), 0)

    async def test_cpmcputotal5minrev(self):
        """Testing function cpmcputotal5minrev."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 10, 2: 15, 3: 20})

        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        result = await cisco_process.cpmcputotal5minrev()

        self.assertEqual(result[1], 10)
        self.assertEqual(result[2], 15)
        self.assertEqual(result[3], 20)

    async def test_cpmcputotal5minrev_oidonly(self):
        """Testing function cpmcputotal5minrev with oidonly=True."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        result = await cisco_process.cpmcputotal5minrev(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.4.1.9.9.109.1.1.1.1.8")

    async def test_cpmcputotal5minrev_with_exception(self):
        """Testing function cpmcputotal5minrev with exception."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(side_effect=Exception("SNMP error"))

        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        result = await cisco_process.cpmcputotal5minrev()

        self.assertEqual(len(result), 0)

    async def test_memorypoolused(self):
        """Testing function memorypoolused."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 4096000, 2: 4096000})

        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        result = await cisco_process.memorypoolused()

        self.assertEqual(result, 8192000)

    async def test_memorypoolused_oidonly(self):
        """Testing function memorypoolused with oidonly=True."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        result = await cisco_process.memorypoolused(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.4.1.9.9.48.1.1.1.5")

    async def test_memorypoolused_with_exception(self):
        """Testing function memorypoolused with exception."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(side_effect=Exception("SNMP error"))

        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        result = await cisco_process.memorypoolused()

        self.assertIsNone(result)

    async def test_memorypoolfree(self):
        """Testing function memorypoolfree."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 1024000, 2: 1024000})

        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        result = await cisco_process.memorypoolfree()

        self.assertEqual(result, 2048000)

    async def test_memorypoolfree_oidonly(self):
        """Testing function memorypoolfree with oidonly=True."""
        mock_snmp = Mock(spec=Query)
        cisco_process = testimport.CiscoProcessQuery(mock_snmp)

        result = await cisco_process.memorypoolfree(oidonly=True)

        self.assertEqual(result, ".1.3.6.1.4.1.9.9.48.1.1.1.6")

    async def test_memorypoolfree_with_exception(self):
        """Testing function memorypoolfree with exception."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(side_effect=Exception("SNMP error"))

        cisco_process = testimport.CiscoProcessQuery(mock_snmp)
        result = await cisco_process.memorypoolfree()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
