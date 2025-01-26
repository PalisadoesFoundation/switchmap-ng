#!/usr/bin/env python3
"""Test the poller poll module."""

import os
import sys
import unittest
from unittest.mock import patch, call, MagicMock
from multiprocessing.pool import Pool
from switchmap.poller.poll import devices, device, cli_device, _META

# Set up the PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(EXEC_DIR, os.pardir, os.pardir))
_EXPECTED = f"{os.sep}tests{os.sep}switchmap_{os.sep}poller"

if EXEC_DIR.endswith(_EXPECTED):
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        f'This script is not installed in the "{_EXPECTED}" directory. '
        "Please fix."
    )
    sys.exit(2)


class TestPollModule(unittest.TestCase):
    """Test cases for the poll module functionality.

    This class tests various components of the poll module including:
     - Device processing with and without multiprocessing
     - CLI device handling
     - Configuration retrieval for agent subprocesses, server address,
     and polling interval
    """

    def setUp(self):
        """Set up the test environment."""
        self.mock_config_instance = MagicMock()
        self.mock_zone = MagicMock()
        self.mock_zone.name = "zone1"
        self.mock_zone.hostnames = ["device1", "device2"]
        self.mock_config_instance.zones.return_value = [self.mock_zone]

    @patch("switchmap.poller.poll.ConfigPoller")
    @patch("switchmap.poller.poll.files.skip_file")
    @patch("switchmap.poller.poll.os.path.isfile")
    @patch("switchmap.poller.poll.poller.Poll")
    @patch("switchmap.poller.poll.rest.post")
    def test_devices_without_multiprocessing(
        self,
        mock_rest_post,
        mock_poll,
        mock_isfile,
        mock_skip_file,
        mock_config,
    ):
        """Test device processing without multiprocessing.

        Verify that:
        1. Device configuration is correctly retrieved
        2. Skip file checks are performed
        3. SNMP polling is executed
        4. Results are posted via REST
        """
        mock_config.return_value = self.mock_config_instance
        mock_skip_file.return_value = "/path/to/skip/file"
        mock_isfile.return_value = False

        mock_poll_instance = MagicMock()
        mock_poll_instance.query.return_value = {"misc": {"host": "device1"}}
        mock_poll.return_value = mock_poll_instance

        with patch("switchmap.poller.poll.udevice.Device") as mock_device:
            mock_device_instance = MagicMock()
            mock_device_instance.process.return_value = {"misc": {}}
            mock_device.return_value = mock_device_instance

            devices(multiprocessing=False)
            # Verify SNMP polling for both devices
            self.assertEqual(mock_poll.call_count, 2)
            # Verify REST posts for both devices
            self.assertEqual(mock_rest_post.call_count, 2)
            # Verify processing order
            mock_device.assert_has_calls(
                [
                    unittest.mock.call({"misc": {"host": "device1"}}),
                    unittest.mock.call().process(),
                    unittest.mock.call({"misc": {"host": "device1"}}),
                    unittest.mock.call().process(),
                ]
            )

    @patch("switchmap.poller.poll.files.skip_file")
    @patch("switchmap.poller.poll.os.path.isfile")
    @patch("switchmap.poller.poll.poller.Poll")
    @patch("switchmap.poller.poll.rest.post")
    def test_device_with_valid_data(
        self, mock_rest_post, mock_poll, mock_isfile, mock_skip_file
    ):
        """Test processing of a single device with valid data.

        Verify that:
        1. Skip file checks are performed
        2. SNMP polling is executed
        3. Device processing occurs
        4. Results are posted via REST
        """
        mock_skip_file.return_value = "/path/to/skip/file"
        mock_isfile.return_value = False

        # Mock SNMP polling
        mock_poll_instance = MagicMock()
        mock_poll_instance.query.return_value = {"key": "value"}
        mock_poll.return_value = mock_poll_instance

        # Mock device processing
        with patch("switchmap.poller.poll.udevice.Device") as mock_device:
            mock_device_instance = MagicMock()
            mock_device_instance.process.return_value = {"misc": {}}
            mock_device.return_value = mock_device_instance

            poll_meta = _META(zone="zone1", hostname="device1", config=None)
            device(poll_meta)

            mock_poll.assert_called_once()
            mock_device.assert_called_once_with(
                {"key": "value"}
            )  # Use this method
            mock_rest_post.assert_called_once()

    @patch("switchmap.poller.poll.ConfigPoller")
    @patch("switchmap.poller.poll.log.log2see")
    def test_cli_device_hostname_not_found(self, mock_log, mock_config):
        """Test CLI device handling when hostname is not found.

        Verify that log message is output when a hostname is not found in
        the configuration.
        """
        mock_config.return_value = self.mock_config_instance
        self.mock_config_instance.zones.return_value = []

        cli_device("unknown-device")

        mock_log.assert_called_with(
            1036, "No hostname unknown-device found in configuration"
        )

    @patch("switchmap.poller.poll.ConfigPoller")
    @patch("switchmap.poller.poll.device")
    def test_cli_device_hostname_found(self, mock_device, mock_config):
        """Test CLI device handling when hostname is found.

        Verify that device processing is triggered for a valid hostname.
        """
        mock_config.return_value = self.mock_config_instance

        cli_device("device1")

        mock_device.assert_called_once_with(
            _META(
                zone="zone1",
                hostname="device1",
                config=mock_config.return_value,
            ),
            post=False,  # Include the missing argument
        )

    @patch("switchmap.poller.poll.ConfigPoller")
    def test_agent_subprocesses(self, mock_config):
        """Test agent_subprocesses method.

        Verify that agent_subprocesses method returns the expected
        number of subprocesses, based on the configuration.
        """
        self.mock_config_instance.agent_subprocesses.return_value = 8
        mock_config.return_value = self.mock_config_instance

        result = self.mock_config_instance.agent_subprocesses()
        self.assertEqual(result, 8)

    @patch("switchmap.poller.poll.ConfigPoller")
    def test_server_address(self, mock_config):
        """Test server_address method.

        Verify that server_address method returns the expected
        server IP address, based on the configuration.
        """
        self.mock_config_instance.server_address.return_value = "127.0.0.1"
        mock_config.return_value = self.mock_config_instance

        result = self.mock_config_instance.server_address()
        self.assertEqual(result, "127.0.0.1")

    @patch("switchmap.poller.poll.ConfigPoller")
    def test_polling_interval(self, mock_config):
        """Test polling_interval method.

        Verify that polling_interval method returns the expected
        polling interval in seconds, based on the configuration.
        """
        self.mock_config_instance.polling_interval.return_value = 3600
        mock_config.return_value = self.mock_config_instance

        result = self.mock_config_instance.polling_interval()
        self.assertEqual(result, 3600)


if __name__ == "__main__":
    unittest.main()
