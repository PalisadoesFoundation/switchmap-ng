"""Define the switchmap.poller package.

Args:
    None

Returns:
    None

"""

from collections import namedtuple

SNMP = namedtuple(
    "SNMP",
    "enabled group authpassword authprotocol community "
    "port privpassword privprotocol secname version",
)
POLLING_OPTIONS = namedtuple(
    "POLL",
    "hostname authorizations",
)
POLL = namedtuple(
    "POLL",
    "hostname authorization",
)

ZONE = namedtuple("ZONE", "name hostnames")
