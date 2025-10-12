#!/usr/bin/env python3
"""Test the snmp_manager module."""

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
                        os.path.abspath(os.path.join(EXEC_DIR, os.pardir)),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}poller{0}snmp".format(
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
from unittest.mock import patch, MagicMock
from pysnmp.proto.rfc1902 import OctetString, Integer, ObjectIdentifier
import tempfile

from switchmap.poller.snmp import snmp_manager as test_module

# Import pysnmp objects for testing
from pysnmp.proto.rfc1905 import EndOfMibView, NoSuchInstance, NoSuchObject


class ExceptionObj:
    """Test class that raises an exception in __str__ method."""

    def __str__(self):
        """Raise an exception for testing purposes.

        Args:
            None

        Returns:
            None

        Raises:
            ValueError: Always raises this exception for testing purposes.
        """
        raise ValueError("Test exception")


class TestSnmpManagerFunctions(unittest.TestCase):
    """Test utility functions in snmp_manager."""

    def test__convert(self):
        """Test _convert function with various inputs."""
        # Test string input
        result = test_module._convert("test_string")
        self.assertEqual(result, b"test_string")

        # Test bytes input - returns string representation of bytes
        result = test_module._convert(b"test_bytes")
        self.assertEqual(result, b"b'test_bytes'")

        # Test None input
        result = test_module._convert(None)
        self.assertEqual(result, b"None")

        # Test integer input
        result = test_module._convert(42)
        self.assertEqual(result, b"42")

    def test__convert_special_cases(self):
        """Test _convert with pysnmp special objects and mock objects."""
        # Test NoSuchObject
        result = test_module._convert(NoSuchObject())
        self.assertIsNone(result)

        # Test NoSuchInstance
        result = test_module._convert(NoSuchInstance())
        self.assertIsNone(result)

        # Test EndOfMibView
        result = test_module._convert(EndOfMibView())
        self.assertIsNone(result)

        # Test mock object with prettyPrint method - OctetString type
        result = test_module._convert(OctetString("test_value"))
        self.assertEqual(result, b"test_value")

        # Test mock object with prettyPrint method - Integer type
        result = test_module._convert(Integer(42))
        self.assertEqual(result, 42)

        # Test mock object with prettyPrint method - ObjectIdentifier type
        result = test_module._convert(ObjectIdentifier("1.3.6.1.2.1.1.1.0"))
        self.assertEqual(result, b"1.3.6.1.2.1.1.1.0")

        # Test object with 'value' attribute
        value_obj = MagicMock()
        value_obj.value = "test_value_attr"
        # Remove prettyPrint to test fallback
        delattr(value_obj, "prettyPrint")
        result = test_module._convert(value_obj)
        self.assertEqual(result, b"test_value_attr")

    def test__convert_exception_handling(self):
        """Test _convert exception handling."""
        result = test_module._convert(ExceptionObj())
        self.assertIsNone(result)

    def test__format_results(self):
        """Test _format_results function."""
        # Test without normalization
        results = [
            (".1.3.6.1.2.1.1.1.0", "test_value"),
            (".1.3.6.1.2.1.1.2.0", "another_value"),
        ]
        formatted = test_module._format_results(results, None, normalized=False)
        expected = {
            ".1.3.6.1.2.1.1.1.0": b"test_value",
            ".1.3.6.1.2.1.1.2.0": b"another_value",
        }
        self.assertEqual(formatted, expected)

        # Test with normalization
        formatted = test_module._format_results(results, None, normalized=True)
        expected = {"0": b"another_value"}
        self.assertEqual(formatted, expected)

        # Test with mock_filter
        results = [
            (".1.3.6.1.2.1.1.1.0", "match"),
            (".1.3.6.1.9.9.9.0", "no_match"),
        ]
        formatted = test_module._format_results(
            results, ".1.3.6.1.2.1", normalized=False
        )
        expected = {".1.3.6.1.2.1.1.1.0": b"match"}
        self.assertEqual(formatted, expected)

    def test__oid_valid_format(self):
        """Test _oid_valid_format function."""
        # Valid OIDs (must start with .)
        self.assertTrue(test_module._oid_valid_format(".1.3.6.1.2.1.1.1.0"))
        self.assertTrue(test_module._oid_valid_format(".1"))

        # Invalid OIDs
        self.assertFalse(
            test_module._oid_valid_format("1.3.6.1.2.1.1.1.0")
        )  # No leading dot
        self.assertFalse(
            test_module._oid_valid_format(".1.3.6.1.2.1.1.1.0.")
        )  # Trailing dot
        self.assertFalse(
            test_module._oid_valid_format(".1.3.6.1 .2.1.1.1.0")
        )  # Embedded spaces not allowed (RFC compliant)
        self.assertFalse(
            test_module._oid_valid_format(".1.3.6.1.abc.1.1.0")
        )  # Non-numeric
        self.assertFalse(test_module._oid_valid_format(""))  # Empty string
        self.assertFalse(test_module._oid_valid_format(None))  # None
        self.assertFalse(
            test_module._oid_valid_format("..1.3.6.1")
        )  # Double dots

    def test__update_cache(self):
        """Test _update_cache function."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
            tmp_filename = tmp_file.name

        try:
            # Test writing to cache file
            test_group = "test_group_name"
            test_module._update_cache(tmp_filename, test_group)

            # Verify the content was written
            with open(tmp_filename, "r") as f:
                content = f.read().strip()
            self.assertEqual(content, test_group)

        finally:
            os.unlink(tmp_filename)


class TestSnmpManagerSession(unittest.TestCase):
    """Test Session class methods."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock POLL object
        self.mock_poll = MagicMock()
        self.mock_poll.hostname = "test_host"
        self.mock_poll.authorization = MagicMock()
        self.mock_poll.authorization.port = 161

        # Create mock engine
        self.mock_engine = MagicMock()

    def test___init__(self):
        """Test Session initialization."""
        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Check assignments
        self.assertEqual(session._poll, self.mock_poll)
        self.assertEqual(session._engine, self.mock_engine)
        self.assertEqual(session.context_name, "")

        # Test with custom context_name
        session = test_module.Session(
            self.mock_poll, self.mock_engine, "custom_context"
        )
        self.assertEqual(session.context_name, "custom_context")

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.CommunityData")
    def test__session_v1(self, mock_community_data, mock_udp_transport):
        """Test _session method with SNMPv1."""
        # Setup v1 authorization
        self.mock_poll.authorization.version = 1
        self.mock_poll.authorization.community = "public"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify UdpTransportTarget was called
            mock_udp_transport.assert_called_once()
            # Verify CommunityData was called for v1
            mock_community_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.CommunityData")
    def test__session_v2c(self, mock_community_data, mock_udp_transport):
        """Test _session method with SNMPv2c."""
        # Setup v2c authorization
        self.mock_poll.authorization.version = 2
        self.mock_poll.authorization.community = "public"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify UdpTransportTarget was called
            mock_udp_transport.assert_called_once()
            # Verify CommunityData was called for v2c
            mock_community_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    def test__session_v3_no_auth(self, mock_usm_user_data, mock_udp_transport):
        """Test _session method with SNMPv3 no authentication."""
        # Setup v3 authorization without auth
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = None
        self.mock_poll.authorization.privprotocol = None

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify UdpTransportTarget was called
            mock_udp_transport.assert_called_once()
            # Verify UsmUserData was called for v3
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    @patch(
        "switchmap.poller.snmp.snmp_manager.usmHMACMD5AuthProtocol",
        new=MagicMock(),
    )
    def test__session_v3_with_md5_auth(
        self, mock_usm_user_data, mock_udp_transport
    ):
        """Test _session method with SNMPv3 MD5 authentication."""
        # Setup v3 authorization with MD5
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = "md5"
        self.mock_poll.authorization.authpassword = "authpass"
        self.mock_poll.authorization.privprotocol = None

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify calls were made
            mock_udp_transport.assert_called_once()
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    @patch(
        "switchmap.poller.snmp.snmp_manager.usmHMACSHAAuthProtocol",
        new=MagicMock(),
    )
    @patch(
        "switchmap.poller.snmp.snmp_manager.usmDESPrivProtocol", new=MagicMock()
    )
    def test__session_v3_with_sha_and_des(
        self, mock_usm_user_data, mock_udp_transport
    ):
        """Test _session method with SNMPv3 SHA auth and DES privacy."""
        # Setup v3 authorization with SHA and DES
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = "sha"
        self.mock_poll.authorization.authpassword = "authpass"
        self.mock_poll.authorization.privprotocol = "des"
        self.mock_poll.authorization.privpassword = "privpass"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify calls were made
            mock_udp_transport.assert_called_once()
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    @patch(
        "switchmap.poller.snmp.snmp_manager.usmAesCfb128Protocol",
        new=MagicMock(),
    )
    def test__session_v3_with_aes(self, mock_usm_user_data, mock_udp_transport):
        """Test _session method with SNMPv3 and AES privacy."""
        # Setup v3 authorization with AES
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = "sha"
        self.mock_poll.authorization.authpassword = "authpass"
        self.mock_poll.authorization.privprotocol = "aes128"
        self.mock_poll.authorization.privpassword = "privpass"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify calls were made
            mock_udp_transport.assert_called_once()
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    @patch(
        "switchmap.poller.snmp.snmp_manager.usmAesCfb192Protocol",
        new=MagicMock(),
    )
    def test__session_v3_with_aes192(
        self, mock_usm_user_data, mock_udp_transport
    ):
        """Test _session method with SNMPv3 and AES192 privacy."""
        # Setup v3 authorization with AES192
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = "sha"
        self.mock_poll.authorization.authpassword = "authpass"
        self.mock_poll.authorization.privprotocol = "aes192"
        self.mock_poll.authorization.privpassword = "privpass"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify calls were made
            mock_udp_transport.assert_called_once()
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    @patch(
        "switchmap.poller.snmp.snmp_manager.usmAesCfb256Protocol",
        new=MagicMock(),
    )
    def test__session_v3_with_aes256(
        self, mock_usm_user_data, mock_udp_transport
    ):
        """Test _session method with SNMPv3 and AES256 privacy."""
        # Setup v3 authorization with AES256
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = "sha"
        self.mock_poll.authorization.authpassword = "authpass"
        self.mock_poll.authorization.privprotocol = "aes256"
        self.mock_poll.authorization.privpassword = "privpass"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify calls were made
            mock_udp_transport.assert_called_once()
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    def test__session_walk_operation_timeouts(self, mock_udp_transport):
        """Test _session method timeout behavior with walk operations.

        This test verifies that when walk_operation=True is passed to the
        _session method, it uses shorter timeout values (5 seconds) compared
        to the default timeout, optimizing for SNMP walk operations which
        typically require less time per request.

        Args:
            mock_udp_transport: Mock for UdpTransportTarget to verify timeout
                parameters are set correctly.
        """
        # Setup basic authorization
        self.mock_poll.authorization.version = 2
        self.mock_poll.authorization.community = "public"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Test with walk_operation=True (should use shorter timeout)
            result = loop.run_until_complete(
                session._session(walk_operation=True)
            )

            # Verify UdpTransportTarget was called with shorter timeout
            call_args = mock_udp_transport.call_args
            self.assertEqual(call_args[1]["timeout"], 5)
            self.assertEqual(call_args[1]["retries"], 2)

            self.assertIsNotNone(result)

        finally:
            loop.close()

    @patch("switchmap.poller.snmp.snmp_manager.log")
    @patch("switchmap.poller.snmp.snmp_manager.UdpTransportTarget")
    @patch("switchmap.poller.snmp.snmp_manager.UsmUserData")
    def test__session_v3_unknown_protocols(
        self, mock_usm_user_data, mock_udp_transport, mock_log
    ):
        """Test _session method handles unknown SNMPv3 protocols gracefully.

        This test verifies that when SNMPv3 authentication or privacy protocols
        are set to unknown/unsupported values, the system logs appropriate
        warnings but continues to function rather than crashing.

        Args:
            mock_usm_user_data: Mock for UsmUserData to verify SNMPv3 setup
            mock_udp_transport: Mock for UdpTransportTarget to verify connection
            mock_log: Mock for logging to verify warning messages are logged
        """
        # Setup v3 authorization with unknown protocols
        self.mock_poll.authorization.version = 3
        self.mock_poll.authorization.secname = "testuser"
        self.mock_poll.authorization.authprotocol = "unknown_auth"
        self.mock_poll.authorization.authpassword = "authpass"
        self.mock_poll.authorization.privprotocol = "unknown_priv"
        self.mock_poll.authorization.privpassword = "privpass"

        session = test_module.Session(self.mock_poll, self.mock_engine)

        # Mock the async call
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(session._session())

            # Verify warnings were logged
            self.assertTrue(mock_log.log2warning.called)

            # Verify calls were made
            mock_udp_transport.assert_called_once()
            mock_usm_user_data.assert_called_once()

            self.assertIsNotNone(result)

        finally:
            loop.close()


class TestSnmpManagerValidateSimple(unittest.TestCase):
    """Test simple Validate class methods."""

    def test___init__(self):
        """Test Validate initialization."""
        mock_options = MagicMock()
        mock_options.hostname = "test_host"

        validator = test_module.Validate(mock_options)

        # Check that options are stored
        self.assertEqual(validator._options, mock_options)


class TestSnmpManagerInteractSimple(unittest.TestCase):
    """Test simple Interact class methods that don't require complex setup."""

    def test___init___success(self):
        """Test successful Interact initialization."""
        # Create mock POLL object
        mock_poll = MagicMock()
        mock_poll.hostname = "test_device.example.com"
        mock_poll.authorization = MagicMock()

        # Mock asyncio.Semaphore and SnmpEngine to test initialization
        with patch(
            "switchmap.poller.snmp.snmp_manager.asyncio.Semaphore"
        ) as mock_semaphore, patch(
            "switchmap.poller.snmp.snmp_manager.SnmpEngine"
        ) as mock_snmp_engine:

            interact = test_module.Interact(mock_poll)

            # Check that initialization worked
            self.assertEqual(interact._poll, mock_poll)
            mock_snmp_engine.assert_called_once()
            mock_semaphore.assert_called_once_with(10)

    def test_hostname(self):
        """Test hostname method returns poll hostname."""
        # Create mock POLL object
        mock_poll = MagicMock()
        mock_poll.hostname = "test_device.example.com"
        mock_poll.authorization = MagicMock()

        # Mock asyncio.Semaphore to avoid event loop issues
        with patch("switchmap.poller.snmp.snmp_manager.asyncio.Semaphore"):
            interact = test_module.Interact(mock_poll)
            result = interact.hostname()

        self.assertEqual(result, "test_device.example.com")

    @patch("switchmap.poller.snmp.snmp_manager.log")
    def test___init___no_auth_fails(self, mock_log):
        """Test Interact initialization failure when no authorization."""
        # Create mock POLL object with no authorization
        mock_poll = MagicMock()
        mock_poll.authorization = None

        # Mock asyncio.Semaphore to avoid event loop issues
        with patch("switchmap.poller.snmp.snmp_manager.asyncio.Semaphore"):
            test_module.Interact(mock_poll)

        # Verify log2die was called
        mock_log.log2die.assert_called_once_with(1045, unittest.mock.ANY)

    @patch("switchmap.poller.snmp.snmp_manager.log")
    def test_query_invalid_oid_format(self, mock_log):
        """Test query method with invalid OID format."""
        # Create mock POLL object
        mock_poll = MagicMock()
        mock_poll.hostname = "test_device.example.com"
        mock_poll.authorization = MagicMock()

        # Mock asyncio.Semaphore to avoid event loop issues
        with patch("switchmap.poller.snmp.snmp_manager.asyncio.Semaphore"):
            interact = test_module.Interact(mock_poll)

            # This should trigger log2die for invalid OID
            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Use an actually invalid OID (no leading dot)
                loop.run_until_complete(interact.query("1.3.6.1.invalid"))
            except SystemExit:
                pass  # Expected from log2die
            finally:
                loop.close()

        # Verify log2die was called for invalid OID
        self.assertTrue(mock_log.log2die.called)
        # Check that the first call was about OID format
        first_call_args = mock_log.log2die.call_args_list[0]
        self.assertEqual(first_call_args[0][0], 1057)


class TestSnmpManagerSessionErrorHandling(unittest.TestCase):
    """Test Session class error handling."""

    @patch("switchmap.poller.snmp.snmp_manager.log")
    def test___init___no_auth_fails(self, mock_log):
        """Test Session initialization failure when no authorization."""
        # Create mock POLL object with no authorization
        mock_poll = MagicMock()
        mock_poll.authorization = None
        mock_engine = MagicMock()

        # This should trigger log2die
        test_module.Session(mock_poll, mock_engine)

        # Verify log2die was called
        mock_log.log2die.assert_called_once_with(1046, unittest.mock.ANY)


if __name__ == "__main__":
    unittest.main()
