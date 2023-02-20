"""Switchmap-NG poll modulre.

Updates the database with device SNMP data.

"""

# Standard libraries
from multiprocessing import Pool
from collections import namedtuple
from pprint import pprint

# Import app libraries
from switchmap import API_POLLER_POST_URI
from switchmap.poller.snmp import poller
from switchmap.poller.update import device as udevice
from switchmap.poller import rest
from switchmap.poller.configuration import ConfigPoller
from switchmap.core import log

_META = namedtuple("_META", "zone hostname")


def devices():
    """Poll all devices for data using subprocesses and create YAML files.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    arguments = []

    # Get configuration
    config = ConfigPoller()

    # Get the number of threads to use in the pool
    pool_size = config.agent_subprocesses()

    # Create a list of polling objects
    zones = sorted(config.zones())

    # Create a list of arguments
    for zone in zones:
        arguments.extend(
            _META(zone=zone.name, hostname=_) for _ in zone.hostnames
        )

    for argument in arguments:
        device(argument)

    # Create a pool of sub process resources
    # with Pool(processes=pool_size) as pool:

    #     # Create sub processes from the pool
    #     pool.map(device, arguments)


def device(poll, post=True):
    """Poll single device for data and create YAML files.

    Args:
        poll: _META object
        post: Post the data if True, else just print it.

    Returns:
        None

    """
    # Initialize key variables
    hostname = poll.hostname
    zone = poll.zone

    # Poll data for obviously valid hostnames (eg. "None" used in installation)
    if bool(hostname) is True:
        if isinstance(hostname, str) is True:
            if hostname.lower() != "none":
                poll = poller.Poll(hostname)
                snmp_data = poll.query()

                # Process if we get valid data
                if bool(snmp_data) and isinstance(snmp_data, dict):
                    # Process device data
                    _device = udevice.Device(snmp_data)
                    data = _device.process()
                    data["misc"]["zone"] = zone

                    if bool(post) is True:
                        # Update the database tables with polled data
                        rest.post(API_POLLER_POST_URI, data)
                    else:
                        pprint(data)
                else:
                    log_message = """\
Device {} returns no data. Check your connectivity and/or SNMP configuration\
""".format(
                        hostname
                    )
                    log.log2debug(1025, log_message)


def cli_device(hostname):
    """Poll single device for data and create YAML files.

    Args:
        Hostname: Host to poll

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
                arguments.append(_META(zone=zone.name, hostname=hostname))

    if bool(arguments) is True:
        for argument in arguments:
            device(argument, post=False)
    else:
        log_message = "No hostname {} found in configuration".format(hostname)
        log.log2see(1036, log_message)
