"""Async Switchmap-NG poll module."""

import asyncio
from collections import namedtuple
from pprint import pprint
import os
import time 

# Import app libraries 
from switchmap import API_POLLER_POST_URI
from switchmap.poller.snmp import async_poller
from switchmap.poller.update import device as udevice
from switchmap.poller.configuration import ConfigPoller
from switchmap.core import log,rest,files 
from switchmap import AGENT_POLLER

_META = namedtuple("_META", "zone hostname config")


async def devices(max_concurrent_devices=10):
    """Poll all devices asynchronously.

    Args:
        max_concurrent_devices: Maximum number of devices to poll concurrently

    Returns:
        None
    """

    # Initialize key variables 
    arguments = [] 

    # Get configuration 
    config = ConfigPoller() 

    # Create a list of polling objects 
    zones = sorted(config.zones())

    for zone in zones:
        arguments.extend(
            _META(zone=zone.name, hostname=_, config=config) for _ in zone.hostnames
        )
    
    if not arguments:
        log_message = "No devices found in configuration"
        log.log2info(1400, log_message)
        return
    
    log_message = f"Starting async polling of {len(arguments)} devices with max concurrency: {max_concurrent_devices}"
    log.log2info(1401, log_message)

    # Semaphore to limit concurrent devices 
    device_semaphore = asyncio.Semaphore(max_concurrent_devices)

    tasks = [
        device(argument, device_semaphore, post=True) for argument in arguments
    ]

    # Execute all devices concurrently 
    start_time = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end_time = time.time()

    # Process results and log summary
    success_count = sum(1 for r in results if r is True)
    error_count = sum(1 for r in results if isinstance(r, Exception))
    failed_count = len(results) - success_count - error_count
    
    log_message = f"Polling completed in {end_time - start_time:.2f}s: {success_count} succeeded, {failed_count} failed, {error_count} errors"
    log.log2info(1402, log_message)

    # Log specific errors 
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            hostname = arguments[i].hostname
            log_message = f"Device {hostname} polling error: {result}"
            log.log2warning(1403, log_message)
    

async def device(poll_meta, device_semaphore, post=True):
    """Poll each device asynchoronously.

    Args:
        poll_meta: _META object containing zone, hostname, config 
        device_semaphore: Semaphore to limit concurrent devices 
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
            log_message = f"Skip file {skip_file} found. Aborting poll for {hostname} in zone '{zone}'"
            log.log2debug(1404, log_message)
            return False
        
        # Poll data for obviously valid hostname
        if not hostname or not isinstance(hostname, str) or hostname.lower() == "none":
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
                
                #! do a little research on aiohttp
                if post:
                    rest.post(API_POLLER_POST_URI, data, config)
                    log_message = f"Successfully polled and posted data for {hostname}"
                    log.log2debug(1407, log_message)
                else:
                    pprint(data)
                
                return True 
            else:
                log_message = f"Device {hostname} returns no data. Check connectivity/SNMP configuration"
                log.log2debug(1408, log_message)
                return False
        
        except Exception as e:
            log_message = f"Unexpected error polling device {hostname}: {e}"
            log.log2exception(1409, log_message)
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
    zones = sorted(config.zones())
    
    # Create a list of arguments
    for zone in zones:
        for next_hostname in zone.hostnames:
            if next_hostname == hostname:
                arguments.append(
                    _META(zone=zone.name, hostname=hostname, config=config)
                )
    
    if arguments:
        log_message = f"Found {hostname} in {len(arguments)} zone(s), starting async poll"
        log.log2info(1410, log_message)
        
        # Poll each zone occurrence
        tasks = [device(argument,asyncio.Semaphore(1) ,post=False) for argument in arguments]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Check results
        success_count = sum(1 for r in results if r is True)
        if success_count > 0:
            log_message = f"Successfully polled {hostname} from {success_count}/{len(results)} zone(s)"
            log.log2info(1411, log_message)
        else:
            log_message = f"Failed to poll {hostname} from any configured zone"
            log.log2warning(1412, log_message)
    
    else:
        log_message = f"No hostname {hostname} found in configuration"
        log.log2see(1413, log_message)

def run_devices(max_concurrent_devices=10):
    """Run device polling - main entry point."""
    asyncio.run(devices(max_concurrent_devices))

def run_cli_device(hostname):
    """Run CLI device polling - main entry point."""
    asyncio.run(cli_device(hostname))
    
