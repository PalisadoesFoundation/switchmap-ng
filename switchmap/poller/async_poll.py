"""Async Switchmap-NG poll module."""

import asyncio
from collections import namedtuple
from pprint import pprint
import os
import time
import aiohttp

# Import app libraries
from switchmap import API_POLLER_POST_URI, API_PREFIX
from switchmap.poller.snmp import async_poller
from switchmap.poller.update import device as udevice
from switchmap.poller.configuration import ConfigPoller
from switchmap.core import log, rest, files
from switchmap import AGENT_POLLER

_META = namedtuple("_META", "zone hostname config")


async def devices(max_concurrent_devices=None):
    """Poll all devices asynchronously.

    Args:
        max_concurrent_devices: Maximum number of devices to poll concurrently.
                               If None, uses config.agent_subprocesses()

    Returns:
        None
    """
    # Initialize key variables
    arguments = []

    # Get configuration
    config = ConfigPoller()

    # Use config value if not provided
    if max_concurrent_devices is None:
        max_concurrent_devices = config.agent_subprocesses()
    elif (
        not isinstance(max_concurrent_devices, int)
        or max_concurrent_devices < 1
    ):
        log.log2warning(
            1401,
            f"Invalid concurrency={max_concurrent_devices}; defaulting to 1",
        )
        max_concurrent_devices = 1

    # Create a list of polling objects
    zones = sorted(config.zones(), key=lambda z: z.name)

    for zone in zones:
        if not zone.hostnames:
            continue
        arguments.extend(
            _META(zone=zone.name, hostname=_, config=config)
            for _ in zone.hostnames
        )

    if not arguments:
        log_message = "No devices found in configuration"
        log.log2info(1400, log_message)
        return

    log_message = (
        f"Starting async polling of {len(arguments)} devices "
        f"with max concurrency: {max_concurrent_devices}"
    )
    log.log2info(1401, log_message)

    # Semaphore to limit concurrent devices
    device_semaphore = asyncio.Semaphore(max_concurrent_devices)

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            device(argument, device_semaphore, session, post=True)
            for argument in arguments
        ]
        # Execute all devices concurrently
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()

    # Process results and log summary
    success_count = sum(1 for r in results if r is True)
    error_count = sum(1 for r in results if isinstance(r, Exception))
    failed_count = len(results) - success_count - error_count

    log_message = (
        f"Polling completed in {end_time - start_time:.2f}s: "
        f"{success_count} succeeded, {failed_count} failed, "
        f"{error_count} errors"
    )
    log.log2info(1402, log_message)
    # Log specific errors
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            hostname = arguments[i].hostname
            log_message = f"Device {hostname} polling error: {result}"
            log.log2warning(1403, log_message)


async def device(poll_meta, device_semaphore, session, post=True):
    """Poll each device asynchronously.

    Args:
        poll_meta: _META object containing zone, hostname, config
        device_semaphore: Semaphore to limit concurrent devices
        session: aiohttp ClientSession for HTTP requests
        post: Post the data if True, else just print it

    Returns:
        bool: True if successful, False otherwise
    """
    async with device_semaphore:
        # Initialize key variables
        hostname = poll_meta.hostname
        zone = poll_meta.zone
        config = poll_meta.config

        # Do nothing if the skip file exists
        skip_file = files.skip_file(AGENT_POLLER, config)
        if os.path.isfile(skip_file):
            log_message = (
                f"Skip file {skip_file} found. Aborting poll for "
                f"{hostname} in zone '{zone}'"
            )
            log.log2debug(1404, log_message)
            return False

        # Poll data for obviously valid hostname
        if (
            not hostname
            or not isinstance(hostname, str)
            or hostname.lower() == "none"
        ):
            log_message = f"Invalid hostname: {hostname}"
            log.log2debug(1405, log_message)
            return False

        try:
            poll = async_poller.Poll(hostname)

            # Initialize SNMP connection
            if not await poll.initialize_snmp():
                log_message = f"Failed to initialize SNMP for {hostname}"
                log.log2debug(1406, log_message)
                return False

            # Query device data asynchronously
            snmp_data = await poll.query()

            # Process if we get valid data
            if bool(snmp_data) and isinstance(snmp_data, dict):
                # Process device data
                _device = udevice.Device(snmp_data)
                data = _device.process()
                data["misc"]["zone"] = zone

                if post:
                    try:
                        # Construct full URL for posting
                        url = (
                            f"{config.server_url_root()}{API_PREFIX}"
                            f"{API_POLLER_POST_URI}"
                        )
                        log_message = f"Posting data for {hostname} to {url}"
                        log.log2debug(1416, log_message)

                        async with session.post(url, json=data) as res:
                            if res.status == 200:
                                log_message = (
                                    f"Successfully polled and posted data "
                                    f"for {hostname}"
                                )
                                log.log2debug(1407, log_message)
                            else:
                                log_message = (
                                    f"Failed to post data for {hostname}, "
                                    f"status={res.status}"
                                )
                                log.log2warning(1414, log_message)
                    except aiohttp.ClientError as e:
                        log_message = (
                            f"HTTP error posting data for {hostname}: {e}"
                        )
                        log.log2warning(1415, log_message)
                        return False

                else:
                    pprint(data)

                return True
            else:
                log_message = (
                    f"Device {hostname} returns no data. Check "
                    f"connectivity/SNMP configuration"
                )
                log.log2debug(1408, log_message)
                return False

        except (asyncio.TimeoutError, KeyError, ValueError) as e:
            log_message = f"Recoverable error polling device {hostname}: {e}"
            log.log2warning(1409, log_message)
            return False


async def cli_device(hostname):
    """Poll single device for data - CLI interface.

    Args:
        hostname: Host to poll

    Returns:
        None
    """
    # Initialize key variables
    arguments = []

    # Get configuration
    config = ConfigPoller()

    # Create a list of polling objects
    zones = sorted(config.zones(), key=lambda z: z.name)

    # Create a list of arguments
    for zone in zones:
        if not zone.hostnames:
            continue
        for next_hostname in zone.hostnames:
            if next_hostname == hostname:
                arguments.append(
                    _META(zone=zone.name, hostname=hostname, config=config)
                )

    if arguments:
        log_message = (
            f"Found {hostname} in {len(arguments)} zone(s), starting async poll"
        )
        log.log2info(1410, log_message)

        # Poll each zone occurrence
        semaphore = asyncio.Semaphore(1)
        async with aiohttp.ClientSession() as session:
            tasks = [
                device(argument, semaphore, session, post=False)
                for argument in arguments
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check results
        success_count = sum(1 for r in results if r is True)
        if success_count > 0:
            log_message = (
                f"Successfully polled {hostname} from "
                f"{success_count}/{len(results)} zone(s)"
            )
            log.log2info(1411, log_message)
        else:
            log_message = f"Failed to poll {hostname} from any configured zone"
            log.log2warning(1412, log_message)

    else:
        log_message = f"No hostname {hostname} found in configuration"
        log.log2see(1413, log_message)


def run_devices(max_concurrent_devices=None):
    """Run device polling - main entry point.

    Args:
        max_concurrent_devices (int, optional): Maximum number of devices to
            poll concurrently. If None, uses config.agent_subprocesses().

    Returns:
        None
    """
    # Use config if not specified
    if max_concurrent_devices is None:
        config = ConfigPoller()
        max_concurrent_devices = config.agent_subprocesses()

    asyncio.run(devices(max_concurrent_devices))


def run_cli_device(hostname):
    """Run CLI device polling - main entry point.

    Args:
        hostname (str): The hostname of the device to poll.

    Returns:
        None
    """
    asyncio.run(cli_device(hostname))
