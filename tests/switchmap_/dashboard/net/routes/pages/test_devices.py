#!/usr/bin/env python3
"""Test the switchmap.dashboard.net.routes.pages.devices module.

Args:
    None

Returns:
    None

"""
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

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

_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}"
    "dashboard{0}net{0}routes{0}pages".format(os.sep)
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

# Import the switchmap classes to test
from switchmap.dashboard.net.routes.pages import devices
from switchmap.dashboard import uri


class TestDevices(unittest.TestCase):
    """Checks all functions and methods."""

    def setUp(self):
        """Setup the test case.

        Args:
            None

        Returns:
            None

        """
        self.test_device_data = {
            "device": {
                "event": {
                    "roots": [{"idxRoot": 123}, {"idxRoot": 456}],
                    "tsCreated": "2025-01-18 10:00:00",
                }
            }
        }

        # Create mock device instance attributes
        self.mock_interfaces = "mock_interfaces_data"
        self.mock_system = "mock_system_data"
        self.mock_hostname = "device.example.com"

    def test_blueprint_exists(self):
        """Testing DEVICES blueprint initialization.

        Args:
            None

        Returns:
            None

        """
        # Test
        self.assertTrue(hasattr(devices, "DEVICES"))
        self.assertEqual(devices.DEVICES.name, "DEVICES")

    @patch("switchmap.dashboard.net.routes.pages.devices.Device")
    @patch("switchmap.dashboard.net.routes.pages.devices.ConfigDashboard")
    @patch("switchmap.dashboard.net.routes.pages.devices.rest")
    @patch("switchmap.dashboard.net.routes.pages.devices.render_template")
    def test_devices_route_success(
        self, mock_render, mock_rest, mock_config, mock_device
    ):
        """Testing successful devices route.

        Args:
            mock_render: Mock render_template function
            mock_rest: Mock rest module
            mock_config: Mock ConfigDashboard class
            mock_device: Mock Device class

        Returns:
            None

        """
        # Initialize key variables
        idx_device = 97

        # Create mock device instance
        mock_device_instance = MagicMock()
        mock_device_instance.interfaces.return_value = self.mock_interfaces
        mock_device_instance.system.return_value = self.mock_system
        mock_device_instance.hostname.return_value = self.mock_hostname
        mock_device.return_value = mock_device_instance

        # Set up rest mock
        mock_rest.get.return_value = self.test_device_data

        # Set up render mock
        expected_template = "device.html"
        mock_render.return_value = "Rendered HTML Content"

        # Test
        result = devices.devices(idx_device)

        # Verify rest.get call
        mock_rest.get.assert_called_once()
        call_args = mock_rest.get.call_args
        self.assertEqual(call_args[1]["server"], False)

        # Verify Device instantiation and method calls
        mock_device.assert_called_once_with(self.test_device_data)
        mock_device_instance.interfaces.assert_called_once()
        mock_device_instance.system.assert_called_once()
        mock_device_instance.hostname.assert_called_once()

        # Verify template rendering
        mock_render.assert_called_once_with(
            expected_template,
            hostname=self.mock_hostname,
            port_table=self.mock_interfaces,
            system_table=self.mock_system,
            idx_root=123,
            date="2025-01-18 10:00:00",
        )

        # Verify result
        self.assertEqual(result, "Rendered HTML Content")

    @patch("switchmap.dashboard.net.routes.pages.devices.Device")
    @patch("switchmap.dashboard.net.routes.pages.devices.ConfigDashboard")
    @patch("switchmap.dashboard.net.routes.pages.devices.rest")
    def test_devices_route_empty_roots(
        self, mock_rest, mock_config, mock_device
    ):
        """Testing devices route with empty roots list.

        Args:
            mock_rest: Mock rest module
            mock_config: Mock ConfigDashboard class
            mock_device: Mock Device class

        Returns:
            None

        """
        # Initialize key variables
        idx_device = 97
        test_data_empty_roots = {
            "device": {
                "event": {"roots": [], "tsCreated": "2025-01-18 10:00:00"}
            }
        }

        # Set up rest mock
        mock_rest.get.return_value = test_data_empty_roots

        # Create mock device instance
        mock_device_instance = MagicMock()
        mock_device.return_value = mock_device_instance

        # Test
        with self.assertRaises(ValueError):
            devices.devices(idx_device)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
