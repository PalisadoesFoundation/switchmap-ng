#!/usr/bin/env python3
"""Test the mib_ipv6 module."""

import unittest
import os
import sys

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
from unittest.mock import MagicMock, patch, AsyncMock
from switchmap.poller.snmp.mib.generic import mib_ipv6 as test_module


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


class TestMibIpv6Functions(unittest.TestCase):
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
        # Test that get_query returns the Ipv6Query class
        result = test_module.get_query()
        self.assertEqual(result, test_module.Ipv6Query)

    def test_init_query(self):
        """Testing function init_query."""
        # Test that init_query returns a Ipv6Query instance
        mock_snmp_object = MagicMock()
        result = test_module.init_query(mock_snmp_object)
        self.assertIsInstance(result, test_module.Ipv6Query)
        self.assertEqual(result.snmp_object, mock_snmp_object)


class TestMibIpv6(unittest.TestCase):
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
            "switchmap.poller.snmp.mib.generic.mib_ipv6.Query.__init__"
        ) as mock_super_init:
            query = test_module.Ipv6Query(mock_snmp_object)

            # Check that snmp_object is assigned
            self.assertEqual(query.snmp_object, mock_snmp_object)

            # Check that super().__init__ was called with correct parameters
            mock_super_init.assert_called_once_with(
                mock_snmp_object, ".1.3.6.1.2.1.55.1.1", tags=["layer3"]
            )

    @patch("switchmap.poller.snmp.mib.generic.mib_ipv6.defaultdict")
    def test_layer3(self, mock_defaultdict):
        """Testing function layer3."""
        # Test layer3 method
        mock_snmp_object = MagicMock()
        mock_final = MagicMock()
        mock_defaultdict.return_value = mock_final

        with patch("switchmap.poller.snmp.mib.generic.mib_ipv6.Query.__init__"):
            query = test_module.Ipv6Query(mock_snmp_object)

            # Mock the ipv6nettomediaphysaddress method
            mock_values = {"::1": "aa:bb:cc:dd:ee:ff"}
            query.ipv6nettomediaphysaddress = AsyncMock(
                return_value=mock_values
            )

            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(query.layer3())

                # Verify the method calls
                query.ipv6nettomediaphysaddress.assert_called_once()
                self.assertEqual(result, mock_final)

            finally:
                loop.close()

    def test_ipv6nettomediaphysaddress(self):
        """Testing function ipv6nettomediaphysaddress."""
        # Test ipv6nettomediaphysaddress method
        mock_snmp_object = MagicMock()

        # Mock the swalk response
        mock_swalk_data = {
            ".1.3.6.1.2.1.55.1.12.1.2.1.4.32.1.13.224.0.0.251.1.6.0.0.0.0.0.0."
            "0.0": b"\x00\x1b!\x3c\x9c\x7f",
        }
        mock_snmp_object.swalk = AsyncMock(return_value=mock_swalk_data)

        with patch(
            "switchmap.poller.snmp.mib.generic.mib_ipv6.Query.__init__"
        ), patch(
            "switchmap.poller.snmp.mib.generic.mib_ipv6.general."
            "octetstr_2_string"
        ) as mock_octet_convert:

            mock_octet_convert.return_value = "00:1b:21:3c:9c:7f"

            query = test_module.Ipv6Query(mock_snmp_object)

            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                result = loop.run_until_complete(
                    query.ipv6nettomediaphysaddress()
                )

                # Verify swalk was called with correct OID
                mock_snmp_object.swalk.assert_called_once_with(
                    ".1.3.6.1.2.1.55.1.12.1.2", normalized=False
                )

                # Verify octetstr_2_string conversion was called
                mock_octet_convert.assert_called_once()

                # Result should be a dictionary with IPv6 addresses as keys
                self.assertIsInstance(result, dict)

            finally:
                loop.close()


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
