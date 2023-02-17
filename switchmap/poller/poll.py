"""Switchmap-NG poll modulre.

Updates the database with device SNMP data.

"""

# Standard libraries
from multiprocessing import Pool
from collections import namedtuple

# Import app libraries
from switchmap import API_POLLER_POST_URI
from switchmap.poller.snmp import poller
from switchmap.poller.update import device as udevice
from switchmap.poller import rest
from switchmap.poller.configuration import ConfigPoller
from switchmap.core import log

# We have to create this named tuple outside the multiprocessing Pool
# for it to be pickled
_Poll = namedtuple("_Poll", "hostname")


def devices():
    """Poll all devices for data using subprocesses and create YAML files.

    Args:
        None

    Returns:
        None

    """
    # Get configuration
    config = ConfigPoller()

    # Get the number of threads to use in the pool
    pool_size = config.agent_subprocesses()

    # Create a list of polling objects
    hostnames = sorted(config.hostnames())

    polls = [_Poll(hostname=hostname) for hostname in hostnames]

    for poll in polls:
        device(poll)

    # Create a pool of sub process resources
    # with Pool(processes=pool_size) as pool:

    #     # Create sub processes from the pool
    #     pool.map(_poll_single_device, polls)


def device(poll):
    """Poll single device for data and create YAML files.

    Args:
        poll: _Poll object

    Returns:
        None

    """
    # Initialize key variables
    hostname = poll.hostname

    # Poll data for obviously valid hostnames (eg. "None" used in installation)
    if bool(hostname) is True:
        if isinstance(hostname, str) is True:
            if hostname.lower() != "none":
                poll = poller.Poll(hostname)
                snmp_data = poll.query()

                # Process if we get valid data
                if bool(snmp_data):
                    # Process device data
                    _device = udevice.Device(snmp_data)
                    data = _device.process()

                    # Update the database tables with polled data
                    rest.post(API_POLLER_POST_URI, data)
                else:
                    log_message = """\
Device {} returns no data. Check your connectivity and/or SNMP configuration\
""".format(
                        hostname
                    )
                    log.log2debug(1036, log_message)
