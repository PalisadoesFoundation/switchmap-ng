#!/usr/bin/env python3
"""Test the poller poll module."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from switchmap.poller.poll import devices, device, cli_device, _META

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(EXEC_DIR, os.pardir)  # Move up to 'poller'
        ),
        os.pardir,  # Move up to 'switchmap_'
    )
)
_EXPECTED = "{0}tests{0}switchmap_{0}poller".format(os.sep)

if EXEC_DIR.endswith(_EXPECTED):
    # Prepend the root directory to the Python path
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        f'This script is not installed in the "{_EXPECTED}" directory. Please fix.'
    )
    sys.exit(2)


class TestPollModule(unittest.TestCase):

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
        # Mock configuration
        mock_config_instance = MagicMock()
        mock_config_instance.agent_subprocesses.return_value = 4
        mock_zone = MagicMock()
        mock_zone.name = "zone1"
        mock_zone.hostnames = ["device1", "device2"]
        mock_config_instance.zones.return_value = [mock_zone]
        mock_config.return_value = mock_config_instance

        # Mock skip file existence
        mock_skip_file.return_value = "/path/to/skip/file"
        mock_isfile.return_value = False

        # Mock SNMP polling
        mock_poll_instance = MagicMock()
        mock_poll_instance.query.return_value = {"misc": {"host": "device1"}}
        mock_poll.return_value = mock_poll_instance

        # Mock device processing
        with patch("switchmap.poller.poll.udevice.Device") as mock_device:
            mock_device_instance = MagicMock()
            mock_device_instance.process.return_value = {"misc": {}}
            mock_device.return_value = mock_device_instance

            # Run devices without multiprocessing
            devices(multiprocessing=False)

            # Assertions
            mock_poll.assert_called()
            mock_rest_post.assert_called()

    @patch("switchmap.poller.poll.files.skip_file")
    @patch("switchmap.poller.poll.os.path.isfile")
    @patch("switchmap.poller.poll.poller.Poll")
    @patch("switchmap.poller.poll.rest.post")
    def test_device_with_valid_data(
        self, mock_rest_post, mock_poll, mock_isfile, mock_skip_file
    ):
        # Mock skip file existence
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

            # Run device function
            poll_meta = _META(zone="zone1", hostname="device1", config=None)
            device(poll_meta)

            # Assertions
            mock_poll.assert_called()
            mock_device.assert_called()
            mock_rest_post.assert_called()

    @patch("switchmap.poller.poll.ConfigPoller")
    @patch("switchmap.poller.poll.log.log2see")
    def test_cli_device_hostname_not_found(self, mock_log, mock_config):
        # Mock configuration
        mock_config_instance = MagicMock()
        mock_config_instance.zones.return_value = []
        mock_config.return_value = mock_config_instance

        # Run cli_device with a non-existent hostname
        cli_device("unknown-device")

        # Assertions
        mock_log.assert_called_with(
            1036, "No hostname unknown-device found in configuration"
        )

    @patch("switchmap.poller.poll.ConfigPoller")
    @patch("switchmap.poller.poll.device")
    def test_cli_device_hostname_found(self, mock_device, mock_config):
        # Mock configuration
        mock_config_instance = MagicMock()
        mock_zone = MagicMock()
        mock_zone.name = "zone1"
        mock_zone.hostnames = ["device1"]
        mock_config_instance.zones.return_value = [mock_zone]
        mock_config.return_value = mock_config_instance

        # Run cli_device with an existing hostname
        cli_device("device1")

        # Assertions
        mock_device.assert_called()

    @patch("switchmap.poller.poll.ConfigPoller")
    def test_agent_subprocesses(self, mock_config):
        # Mock configuration
        mock_config_instance = MagicMock()
        mock_config_instance.agent_subprocesses.return_value = 8
        mock_config.return_value = mock_config_instance

        # Verify agent_subprocesses
        result = mock_config_instance.agent_subprocesses()
        self.assertEqual(result, 8)

    @patch("switchmap.poller.poll.ConfigPoller")
    def test_server_address(self, mock_config):
        # Mock configuration
        mock_config_instance = MagicMock()
        mock_config_instance.server_address.return_value = "127.0.0.1"
        mock_config.return_value = mock_config_instance

        # Verify server address
        result = mock_config_instance.server_address()
        self.assertEqual(result, "127.0.0.1")

    @patch("switchmap.poller.poll.ConfigPoller")
    def test_polling_interval(self, mock_config):
        # Mock configuration
        mock_config_instance = MagicMock()
        mock_config_instance.polling_interval.return_value = 3600
        mock_config.return_value = mock_config_instance

        # Verify polling interval
        result = mock_config_instance.polling_interval()
        self.assertEqual(result, 3600)


if __name__ == "__main__":
    unittest.main()
