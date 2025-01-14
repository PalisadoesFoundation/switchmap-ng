"""Define the switchmap.poller.update package.

Args:
    None

Returns:
    None

"""

from collections import namedtuple

TrunkInterface = namedtuple("TrunkInterface", "vlan nativevlan trunk ")
