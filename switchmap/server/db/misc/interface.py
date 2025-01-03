"""Switchmap Interface library."""

# Module imports
from switchmap.server.db.table import zone
from switchmap.server.db.table import event
from switchmap.server.db.table import device

# from switchmap.server.db.table import device
from switchmap.server.db.table import l1interface


def interfaces(rdevice):
    """Get an Rl1interface list for the device during the previous event.

    Args:
        rdevice: RDevice object

    Returns:
        result: List of matching Rl1interface objects

    """
    # Initialize key variables
    result = []

    # Determine whether the zone exists
    zone_exists = zone.idx_exists(rdevice.idx_zone)

    if bool(zone_exists) is True:
        # Determine whether there was a previous event
        idx_event = zone_exists.idx_event - 1
        event_exists = event.idx_exists(idx_event)

        # Find the device from the previous event
        if bool(event_exists) is True:
            zones = zone.zones(idx_event)
            for item in zones:
                device_exists = device.exists(item.idx_zone, rdevice.hostname)

                # Device found. Now get the interfaces
                if bool(device_exists) is True:
                    result = l1interface.ifindexes(device_exists.idx_device)
                    break

    return result
