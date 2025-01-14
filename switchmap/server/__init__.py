"""Define the switchmap.server package.

Args:
    None

Returns:
    None

"""

from collections import namedtuple

# Important tuples
ZoneData = namedtuple("ZoneData", "idx_zone data")
ZoneObjects = namedtuple("ZoneObjects", "ips macs pairmacips")
ZoneDevice = namedtuple("ZoneDevice", "idx_zone, data, filepath, config")
EventObjects = namedtuple("EventObjects", "zones event")
PairMacIp = namedtuple("PairMacIp", "mac ip ip_version idx_zone")
