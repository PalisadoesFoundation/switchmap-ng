#!/usr/bin/env python3
"""Test the mib_entity module."""

import unittest
import os
import sys
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

from switchmap.poller.snmp.mib.generic import mib_entity as testimport


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


class TestMibEntityFunctions(unittest.IsolatedAsyncioTestCase):
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
        self.assertEqual(result, testimport.EntityQuery)

    def test_init_query(self):
        """Testing function init_query."""
        mock_snmp = Mock(spec=Query)
        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.EntityQuery)
        self.assertEqual(result.snmp_object, mock_snmp)


class TestMibEntity(unittest.IsolatedAsyncioTestCase):
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
        entity = testimport.EntityQuery(mock_snmp)
        self.assertEqual(entity.snmp_object, mock_snmp)

    async def test_system(self):
        """Testing function system."""
        mock_snmp = Mock(spec=Query)
        entity = testimport.EntityQuery(mock_snmp)

        # Mock all the entity methods
        entity.entphysicalhardwarerev = AsyncMock(return_value={1: "1.0", 2: ""})
        entity.entphysicalfirmwarerev = AsyncMock(return_value={1: "2.0", 2: ""})
        entity.entphysicalsoftwarerev = AsyncMock(return_value={1: "3.0", 2: ""})
        entity.entphysicalname = AsyncMock(return_value={1: "Chassis", 2: ""})
        entity.entphysicalmodelname = AsyncMock(return_value={1: "Model-X", 2: ""})
        entity.entphysicalserialnum = AsyncMock(return_value={1: "SN123", 2: ""})
        entity.entphysicalclass = AsyncMock(return_value={1: 3, 2: 0})
        entity.entphysicaldescr = AsyncMock(return_value={1: "Chassis", 2: ""})

        result = await entity.system()

        self.assertIn("ENTITY-MIB", result)
        data = result["ENTITY-MIB"]
        self.assertIn("entPhysicalSerialNum", data)
        self.assertEqual(data["entPhysicalSerialNum"][0], "SN123")
        self.assertEqual(data["entPhysicalName"][0], "Chassis")

    async def test_system_no_serial(self):
        """Testing function system with no serial numbers."""
        mock_snmp = Mock(spec=Query)
        entity = testimport.EntityQuery(mock_snmp)

        # Mock all methods with empty serial numbers
        entity.entphysicalhardwarerev = AsyncMock(return_value={1: ""})
        entity.entphysicalfirmwarerev = AsyncMock(return_value={1: ""})
        entity.entphysicalsoftwarerev = AsyncMock(return_value={1: ""})
        entity.entphysicalname = AsyncMock(return_value={1: ""})
        entity.entphysicalmodelname = AsyncMock(return_value={1: ""})
        entity.entphysicalserialnum = AsyncMock(return_value={1: ""})
        entity.entphysicalclass = AsyncMock(return_value={1: 0})
        entity.entphysicaldescr = AsyncMock(return_value={1: ""})

        result = await entity.system()

        self.assertIn("ENTITY-MIB", result)
        self.assertEqual(len(result["ENTITY-MIB"]), 0)

    async def test_entphysicaldescr(self):
        """Testing function entphysicaldescr."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            return_value={1: b"Chassis", 2: b"Module 1"}
        )

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicaldescr()

        self.assertEqual(result[1], "Chassis")
        self.assertEqual(result[2], "Module 1")

    async def test_entphysicalclass(self):
        """Testing function entphysicalclass."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: 3, 2: 9})

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalclass()

        self.assertEqual(result[1], 3)
        self.assertEqual(result[2], 9)

    async def test_entphysicalsoftwarerev(self):
        """Testing function entphysicalsoftwarerev."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: b"1.0.0", 2: b"2.1.0"})

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalsoftwarerev()

        self.assertEqual(result[1], "1.0.0")
        self.assertEqual(result[2], "2.1.0")

    async def test_entphysicalserialnum(self):
        """Testing function entphysicalserialnum."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: b"ABC123", 2: b"DEF456"})

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalserialnum()

        self.assertEqual(result[1], "ABC123")
        self.assertEqual(result[2], "DEF456")

    async def test_entphysicalmodelname(self):
        """Testing function entphysicalmodelname."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: b"Model-A", 2: b"Model-B"})

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalmodelname()

        self.assertEqual(result[1], "Model-A")
        self.assertEqual(result[2], "Model-B")

    async def test_entphysicalname(self):
        """Testing function entphysicalname."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(
            return_value={1: b"Chassis 1", 2: b"PSU 1"}
        )

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalname()

        self.assertEqual(result[1], "Chassis 1")
        self.assertEqual(result[2], "PSU 1")

    async def test_entphysicalhardwarerev(self):
        """Testing function entphysicalhardwarerev."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: b"1.0", 2: b"2.0"})

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalhardwarerev()

        self.assertEqual(result[1], "1.0")
        self.assertEqual(result[2], "2.0")

    async def test_entphysicalfirmwarerev(self):
        """Testing function entphysicalfirmwarerev."""
        mock_snmp = Mock(spec=Query)
        mock_snmp.swalk = AsyncMock(return_value={1: b"FW1.0", 2: b"FW2.0"})

        entity = testimport.EntityQuery(mock_snmp)
        result = await entity.entphysicalfirmwarerev()

        self.assertEqual(result[1], "FW1.0")
        self.assertEqual(result[2], "FW2.0")


if __name__ == "__main__":
    unittest.main()
