#!/usr/bin/env python3
"""Test the poller poll module."""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
from multiprocessing import TimeoutError
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
        f'This script is not installed in the "{_EXPECTED}" directory. '
        "Please fix."
    )
    sys.exit(2)


class TestPollModule(unittest.TestCase):
    """Test cases for the poll module functionality."""

    def setUp(self):
        """Set up the test environment."""
        self.mock_config_instance = MagicMock()
        self.mock_zone = MagicMock()
        self.mock_zone.name = "zone1"
        self.mock_zone.hostnames = ["device1", "device2"]
        self.mock_config_instance.zones.return_value = [self.mock_zone]
        self.mock_config_instance.agent_subprocesses.return_value = 2

    def test_devices_without_multiprocessing(self):
        """Test device processing without multiprocessing."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = self.mock_config_instance
            with patch("switchmap.poller.poll.device") as mock_device:
                devices(multiprocessing=False)
                expected_calls = [
                    call(
                        _META(
                            zone="zone1",
                            hostname="device1",
                            config=self.mock_config_instance,
                        )
                    ),
                    call(
                        _META(
                            zone="zone1",
                            hostname="device2",
                            config=self.mock_config_instance,
                        )
                    ),
                ]
                mock_device.assert_has_calls(expected_calls)

    def test_devices_with_multiprocessing(self):
        """Test device processing with multiprocessing."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = self.mock_config_instance
            with patch("switchmap.poller.poll.Pool") as mock_pool:
                mock_pool_instance = MagicMock()
                mock_pool.return_value.__enter__.return_value = (
                    mock_pool_instance
                )

                devices(multiprocessing=True)

                mock_pool.assert_called_once_with(processes=2)
                expected_args = [
                    _META(
                        zone="zone1",
                        hostname="device1",
                        config=self.mock_config_instance,
                    ),
                    _META(
                        zone="zone1",
                        hostname="device2",
                        config=self.mock_config_instance,
                    ),
                ]
                mock_pool_instance.map.assert_called_once_with(
                    device, expected_args
                )

    def test_devices_with_multiprocessing_pool_error(self):
        """Test error handling when pool creation fails."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = self.mock_config_instance
            with patch("switchmap.poller.poll.Pool") as mock_pool:
                mock_pool.side_effect = OSError("Failed to create pool")
                with self.assertRaises(OSError):
                    devices(multiprocessing=True)

    def test_devices_with_multiprocessing_worker_error(self):
        """Test error handling when a worker process fails."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = self.mock_config_instance
            with patch("switchmap.poller.poll.Pool") as mock_pool:
                mock_pool_instance = MagicMock()
                mock_pool.return_value.__enter__.return_value = (
                    mock_pool_instance
                )
                mock_pool_instance.map.side_effect = Exception(
                    "Worker process failed"
                )

                with self.assertRaises(Exception):
                    devices(multiprocessing=True)

    @patch("switchmap.poller.poll.files.skip_file")
    @patch("switchmap.poller.poll.os.path.isfile")
    @patch("switchmap.poller.poll.poller.Poll")
    @patch("switchmap.poller.poll.rest.post")
    def test_device_with_skip_file(
        self, mock_rest_post, mock_poll, mock_isfile, mock_skip_file
    ):
        """Test device processing when skip file exists."""
        mock_skip_file.return_value = "/path/to/skip/file"
        mock_isfile.return_value = True

        with patch("switchmap.poller.poll.log.log2debug") as mock_log:
            poll_meta = _META(zone="zone1", hostname="device1", config=None)
            device(poll_meta)
            mock_log.assert_called_once_with(1041, unittest.mock.ANY)
            mock_poll.assert_not_called()
            mock_rest_post.assert_not_called()

    @patch("switchmap.poller.poll.files.skip_file")
    @patch("switchmap.poller.poll.os.path.isfile")
    @patch("switchmap.poller.poll.poller.Poll")
    @patch("switchmap.poller.poll.rest.post")
    def test_device_with_invalid_snmp_data(
        self, mock_rest_post, mock_poll, mock_isfile, mock_skip_file
    ):
        """Test device processing with invalid SNMP data."""
        mock_skip_file.return_value = "/path/to/skip/file"
        mock_isfile.return_value = False
        mock_poll_instance = MagicMock()
        mock_poll_instance.query.return_value = None
        mock_poll.return_value = mock_poll_instance

        with patch("switchmap.poller.poll.log.log2debug") as mock_log:
            poll_meta = _META(zone="zone1", hostname="device1", config=None)
            device(poll_meta)
            mock_log.assert_called_once_with(1025, unittest.mock.ANY)
            mock_rest_post.assert_not_called()

    def test_cli_device_not_found(self):
        """Test CLI device handling when device not found."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = self.mock_config_instance
            with patch("switchmap.poller.poll.log.log2see") as mock_log:
                cli_device("unknown-device")
                mock_log.assert_called_once_with(
                    1036, "No hostname unknown-device found in configuration"
                )

    def test_cli_device_found(self):
        """Test CLI device handling when device is found."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = self.mock_config_instance
            with patch("switchmap.poller.poll.device") as mock_device:
                cli_device("device1")
                expected_meta = _META(
                    zone="zone1",
                    hostname="device1",
                    config=self.mock_config_instance,
                )
                mock_device.assert_called_once_with(expected_meta, post=False)


if __name__ == "__main__":
    unittest.main()
