#!/usr/bin/env python3
"""Test the mib_ciscoietfip module."""

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
from switchmap.poller.snmp.mib.cisco import mib_ciscoietfip as testimport


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


class TestCiscoIetfIpQueryFunctions(unittest.IsolatedAsyncioTestCase):
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
        result = testimport.get_query()
        self.assertEqual(result, testimport.CiscoIetfIpQuery)

    def test_init_query(self):
        """Testing function init_query."""
        mock_snmp = Mock(spec=Query)
        result = testimport.init_query(mock_snmp)
        self.assertIsInstance(result, testimport.CiscoIetfIpQuery)
        self.assertEqual(result.snmp_object, mock_snmp)


class TestCiscoIetfIpQuery(unittest.IsolatedAsyncioTestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # SNMPwalk results used by Mocks.

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
        mock_snmp = Mock(spec=Query)
        cisco_ietf_ip = testimport.CiscoIetfIpQuery(mock_snmp)
        self.assertEqual(cisco_ietf_ip.snmp_object, mock_snmp)

    async def test_layer3(self):
        """Testing function layer3."""
        mock_snmp = Mock(spec=Query)
        cisco_ietf_ip = testimport.CiscoIetfIpQuery(mock_snmp)

        cisco_ietf_ip.cinetnettomediaphysaddress = AsyncMock(
            return_value={
                "2001:0db8:85a3:0000:0000:8a2e:0370:7334": "aabbccddeeff00",
                "2001:0db8:85a3:0000:0000:8a2e:0370:7335": "112233445566",
            }
        )

        result = await cisco_ietf_ip.layer3()

        self.assertIn("cInetNetToMediaPhysAddress", result)
        # MAC should be truncated to 12 chars
        mac1 = result["cInetNetToMediaPhysAddress"][
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        ]
        self.assertEqual(mac1, "aabbccddeeff")
        mac2 = result["cInetNetToMediaPhysAddress"][
            "2001:0db8:85a3:0000:0000:8a2e:0370:7335"
        ]
        self.assertEqual(mac2, "112233445566")

    async def test_cinetnettomediaphysaddress(self):
        """Testing function cinetnettomediaphysaddress."""
        mock_snmp = Mock(spec=Query)

        # IPv6 in decimal: 2001:0db8::1 = 32.1.13.184.0.0...0.1
        oid_suffix = ".2.16.32.1.13.184.0.0.0.0.0.0.0.0.0.0.0.1"
        full_oid = f".1.3.6.1.4.1.9.10.86.1.1.3.1.3{oid_suffix}"
        mock_snmp.swalk = AsyncMock(
            return_value={full_oid: b"\xaa\xbb\xcc\xdd\xee\xff"}
        )

        cisco_ietf_ip = testimport.CiscoIetfIpQuery(mock_snmp)

        patch_path = "switchmap.poller.snmp.mib.cisco.mib_ciscoietfip.general"
        with patch(f"{patch_path}.octetstr_2_string") as mock_convert:
            mock_convert.return_value = "aabbccddeeff"
            result = await cisco_ietf_ip.cinetnettomediaphysaddress()

            ipv6 = "20:01:0d:b8:00:00:00:00:00:00:00:00:00:00:00:01"
            self.assertIn(ipv6, result)
            self.assertEqual(result[ipv6], "aabbccddeeff")


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
