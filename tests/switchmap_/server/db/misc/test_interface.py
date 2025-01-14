import unittest
from unittest.mock import patch, MagicMock

# Mocking read_yaml_file and ConfigServer globally to prevent configuration initialization issues
yaml_patcher = patch("switchmap.core.files.read_yaml_file", return_value={"config_key": "value"})
yaml_patcher.start()

config_patcher = patch("switchmap.server.configuration.ConfigServer", autospec=True)
config_patcher.start()

from switchmap.server.db.misc.interface import interfaces  # Import after mocking

class TestInterfaces(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        """
        Stop global mocks after all tests.
        """
        yaml_patcher.stop()
        config_patcher.stop()

    @patch("switchmap.server.db.misc.interface.zone")
    @patch("switchmap.server.db.misc.interface.event")
    @patch("switchmap.server.db.misc.interface.device")
    @patch("switchmap.server.db.misc.interface.l1interface")
    def test_interfaces_success(self, mock_l1interface, mock_device, mock_event, mock_zone):
        """
        Test successful retrieval of interfaces when all conditions pass.
        """
        # Mock return values
        mock_zone.idx_exists.return_value = MagicMock(idx_event=2)
        mock_event.idx_exists.return_value = True
        mock_zone.zones.return_value = [MagicMock(idx_zone=1)]
        mock_device.exists.return_value = MagicMock(idx_device=5)
        mock_l1interface.ifindexes.return_value = ["interface1", "interface2"]

        # Mock rdevice input
        rdevice = MagicMock(idx_zone=1, hostname="device1")

        # Call the function
        result = interfaces(rdevice)

        # Assert the result
        self.assertEqual(result, ["interface1", "interface2"])

    @patch("switchmap.server.db.misc.interface.zone")
    def test_interfaces_no_zone(self, mock_zone):
        """
        Test when the zone does not exist.
        """
        mock_zone.idx_exists.return_value = False
        rdevice = MagicMock(idx_zone=1, hostname="device1")
        result = interfaces(rdevice)
        self.assertEqual(result, [])

    @patch("switchmap.server.db.misc.interface.zone")
    @patch("switchmap.server.db.misc.interface.event")
    def test_interfaces_no_event(self, mock_event, mock_zone):
        """
        Test when the event does not exist.
        """
        mock_zone.idx_exists.return_value = MagicMock(idx_event=2)
        mock_event.idx_exists.return_value = False
        rdevice = MagicMock(idx_zone=1, hostname="device1")
        result = interfaces(rdevice)
        self.assertEqual(result, [])

    @patch("switchmap.server.db.misc.interface.zone")
    @patch("switchmap.server.db.misc.interface.event")
    @patch("switchmap.server.db.misc.interface.device")
    def test_interfaces_no_device(self, mock_device, mock_event, mock_zone):
        """
        Test when the device does not exist.
        """
        mock_zone.idx_exists.return_value = MagicMock(idx_event=2)
        mock_event.idx_exists.return_value = True
        mock_zone.zones.return_value = [MagicMock(idx_zone=1)]
        mock_device.exists.return_value = False
        rdevice = MagicMock(idx_zone=1, hostname="device1")
        result = interfaces(rdevice)
        self.assertEqual(result, [])

    @patch("switchmap.server.db.misc.interface.zone")
    @patch("switchmap.server.db.misc.interface.event")
    @patch("switchmap.server.db.misc.interface.device")
    @patch("switchmap.server.db.misc.interface.l1interface")
    def test_interfaces_no_interfaces(self, mock_l1interface, mock_device, mock_event, mock_zone):
        """
        Test when no interfaces are returned.
        """
        mock_zone.idx_exists.return_value = MagicMock(idx_event=2)
        mock_event.idx_exists.return_value = True
        mock_zone.zones.return_value = [MagicMock(idx_zone=1)]
        mock_device.exists.return_value = MagicMock(idx_device=5)
        mock_l1interface.ifindexes.return_value = []
        rdevice = MagicMock(idx_zone=1, hostname="device1")
        result = interfaces(rdevice)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
