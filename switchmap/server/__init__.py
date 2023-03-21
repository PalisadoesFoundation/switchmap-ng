from collections import namedtuple

# Important tuples
ZoneData = namedtuple("ZoneData", "idx_zone data")
ZoneObjects = namedtuple("ZoneObjects", "ips macs")
ZoneDevice = namedtuple("ZoneDevice", "idx_zone, data, filepath, config")
EventObjects = namedtuple("EventObjects", "zones event")
