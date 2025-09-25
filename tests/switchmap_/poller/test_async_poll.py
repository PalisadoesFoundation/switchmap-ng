#!/usr/bin/env python3
"""Test the async poller poll module."""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from switchmap.poller.poll import devices, device, cli_device, _META

# Create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(EXEC_DIR, os.pardir)  # Move up to 'poller'
        ),
        os.pardir,  # Move up to 'switchmap_'
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}poller".format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        f'This script is not installed in the "{_EXPECTED}" directory. '
        "Please fix."
    )
    sys.exit(2)


@pytest.fixture
def mock_config_setup():
    """Set up mock configuration for tests.

    Args:
        None

    Returns:
        MagicMock: Mock configuration instance with zones and subprocesses.
    """
    mock_config_instance = MagicMock()
    mock_zone = MagicMock()
    mock_zone.name = "zone1"
    mock_zone.hostnames = ["device1", "device2"]
    mock_config_instance.zones.return_value = [mock_zone]
    mock_config_instance.agent_subprocesses.return_value = 2
    return mock_config_instance


@pytest.fixture
def mock_poll_meta():
    """Create a mock poll meta object.

    Args:
        None

    Returns:
        _META: Mock poll meta object with zone, hostname, and config.
    """
    return _META(zone="zone1", hostname="device1", config=MagicMock())


class TestAsyncPoll:
    """Test cases for the async poll module functionality."""

    @pytest.mark.asyncio
    async def test_devices_basic_functionality(self, mock_config_setup):
        """Test basic device polling functionality."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_setup
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                mock_device.return_value = True

                await devices()

                # Verify device was called for each hostname
                assert mock_device.call_count == 2

                # Check that the calls were made with correct hostnames
                call_args_list = mock_device.call_args_list
                hostnames_called = [
                    call[0][0].hostname for call in call_args_list
                ]
                assert "device1" in hostnames_called
                assert "device2" in hostnames_called

    @pytest.mark.asyncio
    async def test_devices_with_custom_concurrency(self, mock_config_setup):
        """Test device polling with custom concurrency limit."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_setup
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                mock_device.return_value = True

                await devices(max_concurrent_devices=1)

                # Should still call device for both hostnames
                assert mock_device.call_count == 2

    @pytest.mark.asyncio
    async def test_cli_device_found(self, mock_config_setup):
        """Test CLI device polling when hostname is found."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_setup
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                mock_device.return_value = True

                await cli_device("device1")

                # Should call device once for the found hostname
                assert mock_device.call_count == 1
                assert mock_device.call_args[0][0].hostname == "device1"

    @pytest.mark.asyncio
    async def test_cli_device_not_found(self, mock_config_setup):
        """Test CLI device polling when hostname is not found."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_setup
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:

                await cli_device("nonexistent_device")

                # Should not call device for non-existent hostname
                assert mock_device.call_count == 0

    @pytest.mark.asyncio
    async def test_device_with_skip_file(self, mock_poll_meta):
        """Test device processing when skip file exists."""
        with patch("switchmap.poller.poll.files.skip_file") as mock_skip_file:
            mock_skip_file.return_value = "/path/to/skip/file"
            with patch("switchmap.poller.poll.os.path.isfile") as mock_isfile:
                mock_isfile.return_value = True
                with patch("switchmap.poller.poll.log.log2debug") as mock_log:
                    # Create mock semaphore and session
                    mock_semaphore = AsyncMock()
                    mock_session = MagicMock()

                    result = await device(
                        mock_poll_meta, mock_semaphore, mock_session
                    )

                    # Should return False when skip file exists
                    assert result is False
                    mock_log.assert_called()

    @pytest.mark.asyncio
    async def test_device_invalid_hostname(self):
        """Test device processing with invalid hostname."""
        mock_semaphore = AsyncMock()
        mock_session = MagicMock()

        # Test with None hostname
        poll_meta = _META(zone="zone1", hostname=None, config=MagicMock())
        result = await device(poll_meta, mock_semaphore, mock_session)
        assert result is False

        # Test with "none" hostname
        poll_meta = _META(zone="zone1", hostname="none", config=MagicMock())
        result = await device(poll_meta, mock_semaphore, mock_session)
        assert result is False

    @pytest.mark.asyncio
    async def test_device_snmp_failure(self, mock_poll_meta):
        """Test device processing when SNMP initialization fails."""
        mock_skip_file_path = "/path/to/skip/file"
        with patch("switchmap.poller.poll.files.skip_file") as mock_skip_file:
            mock_skip_file.return_value = mock_skip_file_path
            with patch("switchmap.poller.poll.os.path.isfile") as mock_isfile:
                mock_isfile.return_value = False
                with patch(
                    "switchmap.poller.poll.poller.Poll"
                ) as mock_poll_cls:
                    mock_poll_instance = AsyncMock()
                    mock_poll_instance.initialize_snmp.return_value = False
                    mock_poll_cls.return_value = mock_poll_instance

                    mock_semaphore = AsyncMock()
                    mock_session = MagicMock()

                    result = await device(
                        mock_poll_meta, mock_semaphore, mock_session
                    )

                    # Should return False when SNMP initialization fails
                    assert result is False

    @pytest.mark.asyncio
    async def test_device_successful_poll_no_post(self, mock_poll_meta):
        """Test successful device polling without posting data."""
        mock_skip_file_path = "/path/to/skip/file"
        with patch("switchmap.poller.poll.files.skip_file") as mock_skip_file:
            mock_skip_file.return_value = mock_skip_file_path
            with patch("switchmap.poller.poll.os.path.isfile") as mock_isfile:
                mock_isfile.return_value = False
                with patch(
                    "switchmap.poller.poll.poller.Poll"
                ) as mock_poll_cls:
                    mock_poll_instance = AsyncMock()
                    mock_poll_instance.initialize_snmp.return_value = True
                    mock_poll_instance.query.return_value = {"test": "data"}
                    mock_poll_cls.return_value = mock_poll_instance

                    mock_semaphore = AsyncMock()
                    mock_session = MagicMock()

                    with patch(
                        "switchmap.poller.poll.udevice.Device"
                    ) as mock_device_class:
                        mock_device_instance = MagicMock()
                        mock_device_instance.process.return_value = {
                            "misc": {},
                            "test": "data",
                        }
                        mock_device_class.return_value = mock_device_instance

                        result = await device(
                            mock_poll_meta,
                            mock_semaphore,
                            mock_session,
                            post=False,
                        )

                        # Should return True for successful poll
                        assert result is True
                        # Should create Device instance and call process
                        mock_device_class.assert_called_once()
                        mock_device_instance.process.assert_called_once()
