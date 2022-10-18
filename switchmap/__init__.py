#!/usr/bin/env python3
"""Switchmap-NG setup.

Manages parameters required by all classes in the module.

"""

# Standard imports
from collections import namedtuple

# Do library imports
from .core import log
from .poll.update import TrunkInterface
from .core.configuration import Config, ConfigSNMP

# Create global variables for the API
SITE_PREFIX = "/switchmap-ng"
API_PREFIX = "{}/api/v1".format(SITE_PREFIX)
API_STATIC_FOLDER = "static/default"
API_TEMPLATE_FOLDER = "templates/default"
AGENT_API_CHILD = "switchmap-ng-gunicorn"
AGENT_POLLER = "Poller"
AGENT_API = "API"

# Important tuples
Found = namedtuple("Found", "idx_l1interface")
IP = namedtuple("IP", "address version")
MacDetail = namedtuple(
    "MacDetail", "hostname mac ip_ organization idx_l1interface idx_mac"
)
InterfaceDetail = namedtuple(
    "InterfaceDetail", "RL1Interface MacDetails RVlans"
)
DeviceDetail = namedtuple(
    'DeviceDetail', 'RDevice InterfaceDetails'
)


def main():
    """Process data.

    Args:
        None

    Returns:
        None

    """
    # Check the environment
    log.check_environment()


if __name__ == "switchmap":
    main()
