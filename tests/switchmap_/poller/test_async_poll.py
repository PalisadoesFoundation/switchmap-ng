#!/usr/bin/env python3
"""Test the async poller poll module."""

import os
import sys
import pytest
import asyncio
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
    async def test_devices_invalid_concurrency(self, mock_config_setup):
        """Test devices() with invalid concurrency values."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_setup
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                mock_device.return_value = True

                # Test negative concurrency
                await devices(max_concurrent_devices=-1)
                # Should still call device functions with default concurrency
                assert mock_device.call_count == 2

    @pytest.mark.asyncio
    async def test_devices_empty_zones(self):
        """Test devices() with zones containing no hostnames."""
        mock_config_instance = MagicMock()
        mock_zone = MagicMock()
        mock_zone.name = "empty_zone"
        mock_zone.hostnames = []  # Empty hostnames
        mock_config_instance.zones.return_value = [mock_zone]
        mock_config_instance.agent_subprocesses.return_value = 2

        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_instance
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                await devices()
                # Should not call device when no hostnames
                assert mock_device.call_count == 0

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
                    mock_semaphore = asyncio.Semaphore(1)
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
        mock_semaphore = asyncio.Semaphore(1)
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

                    mock_semaphore = asyncio.Semaphore(1)
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

                    mock_semaphore = asyncio.Semaphore(1)
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

    @pytest.mark.asyncio
    async def test_devices_with_exceptions(self, mock_config_setup):
        """Test devices() when asyncio.gather returns exceptions."""
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_setup
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                # Make one device return an exception
                mock_device.side_effect = [True, Exception("Test error")]

                with patch(
                    "switchmap.poller.poll.log.log2warning"
                ) as mock_log_warning:
                    await devices()

                    # Should log the exception error
                    mock_log_warning.assert_called()
                    # Check that the warning was called with the correct
                    # message pattern
                    call_args = mock_log_warning.call_args[0]
                    assert "Device device2 polling error:" in call_args[1]

    @pytest.mark.asyncio
    async def test_device_http_post_success(self, mock_poll_meta):
        """Test device() HTTP POST success scenario (lines 163-191)."""
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

                    mock_semaphore = asyncio.Semaphore(1)
                    mock_session = MagicMock()
                    mock_response = AsyncMock()
                    mock_response.status = 200

                    # Properly mock the async context manager
                    mock_session.post.return_value.__aenter__ = AsyncMock(
                        return_value=mock_response
                    )
                    mock_session.post.return_value.__aexit__ = AsyncMock(
                        return_value=None
                    )

                    with patch(
                        "switchmap.poller.poll.udevice.Device"
                    ) as mock_device_class:
                        mock_device_instance = MagicMock()
                        mock_device_instance.process.return_value = {
                            "misc": {},
                            "test": "data",
                        }
                        mock_device_class.return_value = mock_device_instance

                        with patch(
                            "switchmap.poller.poll.log.log2debug"
                        ) as mock_log_debug:
                            result = await device(
                                mock_poll_meta,
                                mock_semaphore,
                                mock_session,
                                post=True,
                            )

                            # Should return True for successful POST
                            assert result is True
                            # Should log successful posting
                            mock_log_debug.assert_called()

    @pytest.mark.asyncio
    async def test_device_http_post_failure_status(self, mock_poll_meta):
        """Test device() function handles HTTP POST failures gracefully.

        This test verifies that when an HTTP POST request to the polling API
        fails with a bad status code (e.g., 500 Internal Server Error), the
        device() function returns False and logs an appropriate warning message
        instead of crashing or throwing an exception.

        Args:
            mock_poll_meta: Mock containing device metadata and polling
                configuration used for the test.
        """
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

                    mock_semaphore = asyncio.Semaphore(1)
                    mock_session = MagicMock()
                    mock_response = AsyncMock()
                    mock_response.status = 500

                    # Properly mock the async context manager
                    mock_session.post.return_value.__aenter__ = AsyncMock(
                        return_value=mock_response
                    )
                    mock_session.post.return_value.__aexit__ = AsyncMock(
                        return_value=None
                    )

                    with patch(
                        "switchmap.poller.poll.udevice.Device"
                    ) as mock_device_class:
                        mock_device_instance = MagicMock()
                        mock_device_instance.process.return_value = {
                            "misc": {},
                            "test": "data",
                        }
                        mock_device_class.return_value = mock_device_instance

                        with patch(
                            "switchmap.poller.poll.log.log2warning"
                        ) as mock_log_warning:
                            result = await device(
                                mock_poll_meta,
                                mock_semaphore,
                                mock_session,
                                post=True,
                            )

                            # Should return False for failed POST
                            assert result is False
                            # Should log failure warning
                            mock_log_warning.assert_called()

    @pytest.mark.asyncio
    async def test_device_http_post_client_error(self, mock_poll_meta):
        """Test device() HTTP POST with aiohttp.ClientError (lines 163-191)."""
        import aiohttp

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

                    mock_semaphore = asyncio.Semaphore(1)
                    mock_session = MagicMock()
                    mock_session.post.side_effect = aiohttp.ClientError(
                        "Connection failed"
                    )

                    with patch(
                        "switchmap.poller.poll.udevice.Device"
                    ) as mock_device_class:
                        mock_device_instance = MagicMock()
                        mock_device_instance.process.return_value = {
                            "misc": {},
                            "test": "data",
                        }
                        mock_device_class.return_value = mock_device_instance

                        with patch(
                            "switchmap.poller.poll.log.log2warning"
                        ) as mock_log_warning:
                            result = await device(
                                mock_poll_meta,
                                mock_semaphore,
                                mock_session,
                                post=True,
                            )

                            # Should return False for client error
                            assert result is False
                            # Should log client error warning
                            mock_log_warning.assert_called()

    @pytest.mark.asyncio
    async def test_device_no_snmp_data(self, mock_poll_meta):
        """Test device() when SNMP returns no data (lines 198-208)."""
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
                    mock_poll_instance.query.return_value = {}  # Empty data
                    mock_poll_cls.return_value = mock_poll_instance

                    mock_semaphore = asyncio.Semaphore(1)
                    mock_session = MagicMock()

                    with patch(
                        "switchmap.poller.poll.log.log2debug"
                    ) as mock_log_debug:
                        result = await device(
                            mock_poll_meta, mock_semaphore, mock_session
                        )

                        # Should return False for no data
                        assert result is False
                        # Should log no data message
                        mock_log_debug.assert_called()

    @pytest.mark.asyncio
    async def test_device_timeout_error(self, mock_poll_meta):
        """Test device() with TimeoutError exception (lines 198-208)."""
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
                    mock_poll_instance.query.side_effect = asyncio.TimeoutError(
                        "Timeout"
                    )
                    mock_poll_cls.return_value = mock_poll_instance

                    mock_semaphore = asyncio.Semaphore(1)
                    mock_session = MagicMock()

                    with patch(
                        "switchmap.poller.poll.log.log2warning"
                    ) as mock_log_warning:
                        result = await device(
                            mock_poll_meta, mock_semaphore, mock_session
                        )

                        # Should return False for timeout
                        assert result is False
                        # Should log timeout warning
                        mock_log_warning.assert_called()

    @pytest.mark.asyncio
    async def test_device_key_error(self, mock_poll_meta):
        """Test device() with KeyError exception (lines 198-208)."""
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
                    mock_poll_instance.query.side_effect = KeyError(
                        "Missing key"
                    )
                    mock_poll_cls.return_value = mock_poll_instance

                    mock_semaphore = asyncio.Semaphore(1)
                    mock_session = MagicMock()

                    with patch(
                        "switchmap.poller.poll.log.log2warning"
                    ) as mock_log_warning:
                        result = await device(
                            mock_poll_meta, mock_semaphore, mock_session
                        )

                        # Should return False for key error
                        assert result is False
                        # Should log key error warning
                        mock_log_warning.assert_called()

    @pytest.mark.asyncio
    async def test_devices_empty_zones_continue(self):
        """Test devices() with zones that have empty hostnames (line 236)."""
        mock_config_instance = MagicMock()
        mock_zone1 = MagicMock()
        mock_zone1.name = "empty_zone"
        mock_zone1.hostnames = []  # Empty hostnames - should continue
        mock_zone2 = MagicMock()
        mock_zone2.name = "filled_zone"
        mock_zone2.hostnames = ["device1"]
        mock_config_instance.zones.return_value = [mock_zone1, mock_zone2]
        mock_config_instance.agent_subprocesses.return_value = 2

        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_instance
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                mock_device.return_value = True
                await devices()
                # Should only call device once (for filled_zone)
                assert mock_device.call_count == 1

    @pytest.mark.asyncio
    async def test_cli_device_all_zones_fail(self):
        """Test cli_device when all zone attempts fail (lines 267-268)."""
        mock_config_instance = MagicMock()
        mock_zone = MagicMock()
        mock_zone.name = "zone1"
        mock_zone.hostnames = ["device1"]
        mock_config_instance.zones.return_value = [mock_zone]

        with patch("switchmap.poller.poll.ConfigPoller") as mock_config:
            mock_config.return_value = mock_config_instance
            with patch(
                "switchmap.poller.poll.device", new_callable=AsyncMock
            ) as mock_device:
                mock_device.return_value = False

                with patch(
                    "switchmap.poller.poll.log.log2warning"
                ) as mock_log_warning:
                    await cli_device("device1")

                    # Should log failure warning when all zones
                    # fail
                    mock_log_warning.assert_called()
                    call_args = mock_log_warning.call_args[0]
                    assert (
                        "Failed to poll device1 from any configured zone"
                        in call_args[1]
                    )

    def test_run_devices_with_none_concurrency(self):
        """Test run_devices() when max_concurrent_devices is None.

        When max_concurrent_devices is None, run_devices() should
        use the
        configured agent_subprocesses value from ConfigPoller
        instead of
        the None value. This test verifies that asyncio.run is called and
        the configuration is properly consulted.
        """
        with patch("switchmap.poller.poll.ConfigPoller") as mock_config_cls:
            mock_config_instance = MagicMock()
            mock_config_instance.agent_subprocesses.return_value = 5
            mock_config_cls.return_value = mock_config_instance

            with patch("switchmap.poller.poll.asyncio.run") as mock_asyncio_run:
                from switchmap.poller.poll import run_devices

                run_devices(max_concurrent_devices=None)

                # Should call asyncio.run with devices function
                mock_asyncio_run.assert_called_once()
                # Should use config's agent_subprocesses value (5)
                mock_config_cls.assert_called_once()

    def test_run_cli_device(self):
        """Test run_cli_device() function (line 302)."""
        with patch("switchmap.poller.poll.asyncio.run") as mock_asyncio_run:
            from switchmap.poller.poll import run_cli_device

            run_cli_device("test_hostname")

            # Should call asyncio.run with cli_device function
            mock_asyncio_run.assert_called_once()
