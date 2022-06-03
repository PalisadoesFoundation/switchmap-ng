"""Module for updating the database with topology data."""

from switchmap.core import log
from switchmap.db.table import device as _device
from switchmap.db.table import IDevice


def device(data):
    """Update the device DB table.

    Args:
        data: Device data

    Returns:
        None

    """
    # Initialize key variables
    exists = False
    hostname = data['misc']['host']
    row = IDevice(
        idx_location=1,
        hostname=hostname,
        sys_name=data['system']['SNMPv2-MIB']['sysName'][0],
        sys_description=data['system']['SNMPv2-MIB']['sysDescr'][0],
        sys_objectid=data['system']['SNMPv2-MIB']['sysObjectID'][0],
        sys_uptime=data['system']['SNMPv2-MIB']['sysUpTime'][0],
        last_polled=data['misc']['timestamp'],
        enabled=1
    )

    # Log
    log_message = (
        'Updating Device table for host {}'.format(hostname))
    log.log2debug(1028, log_message)

    # Update the database
    exists = _device.exists(row.hostname)
    if bool(exists) is True:
        _device.update_row(exists.idx_device, row)
    else:
        _device.insert_row(row)

    # Log
    log_message = (
        'Updated Device table for host {}'.format(hostname))
    log.log2debug(1029, log_message)
