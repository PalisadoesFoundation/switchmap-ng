"""Module for updating the database with topology data."""

import time
from switchmap.core import log
from switchmap.db.table import device as _device
from switchmap.db.table import l1interface as _l1interface
from switchmap.db.table import (IDevice, IL1Interface)


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


def l1interface(data):
    """Update the l1interface DB table.

    Args:
        data: L1Interface data

    Returns:
        None

    """
    # Initialize key variables
    exists = False
    hostname = data['misc']['host']
    interfaces = data['layer1']

    # Log
    log_message = (
        'Updating L1Interface table for host {}'.format(hostname))
    log.log2debug(1028, log_message)

    # Get device data
    device_ = _device.exists(hostname)

    if bool(device_) is True:

        # Process each interface
        for ifindex, interface in interfaces.items():
            exists = _l1interface.exists(device_.idx_device, ifindex)

            # Update the database
            if bool(exists) is True:
                # Calculate the ts_idle time
                ifadminstatus = interface.get('ifAdminStatus')
                ifoperstatus = interface.get('ifOperStatus')
                if ifadminstatus == 1 and ifoperstatus == 1:
                    # Port enabled with link
                    ts_idle = 0
                elif ifadminstatus == 2:
                    # Port disabled
                    ts_idle = 0
                else:
                    # Port enabled no link
                    if bool(exists.ts_idle) is True:
                        # Do nothing if already idle
                        ts_idle = exists.ts_idle
                    else:
                        # Otherwise create an idle time entry
                        ts_idle = int(time.time())

                # Add new row to the database table
                row = IL1Interface(
                    idx_device=device_.idx_device,
                    ifindex=ifindex,
                    duplex=interface.get('jm_duplex'),
                    ethernet=int(bool(interface.get('jm_ethernet'))),
                    nativevlan=interface.get('jm_nativevlan'),
                    trunk=int(bool(interface.get('jm_trunk'))),
                    ifspeed=interface.get('ifSpeed'),
                    ifalias=interface.get('ifAlias'),
                    ifdescr=interface.get('ifDescr'),
                    ifadminstatus=interface.get('ifAdminStatus'),
                    ifoperstatus=interface.get('ifOperStatus'),
                    cdpcachedeviceid=interface.get('cdpCacheDeviceId'),
                    cdpcachedeviceport=interface.get('cdpCacheDevicePort'),
                    cdpcacheplatform=interface.get('cdpCachePlatform'),
                    lldpremportdesc=interface.get('lldpRemPortDesc'),
                    lldpremsyscapenabled=interface.get(
                        'lldpRemSysCapEnabled'),
                    lldpremsysdesc=interface.get('lldpRemSysDesc'),
                    lldpremsysname=interface.get('lldpRemSysName'),
                    ts_idle=ts_idle,
                    enabled=int(bool(exists.enabled))
                )

                _l1interface.update_row(exists.idx_l1interface, row)
            else:
                # Add new row to the database table
                row = IL1Interface(
                    idx_device=device_.idx_device,
                    ifindex=ifindex,
                    duplex=interface.get('jm_duplex'),
                    ethernet=int(bool(interface.get('jm_ethernet'))),
                    nativevlan=interface.get('jm_nativevlan'),
                    trunk=int(bool(interface.get('jm_trunk'))),
                    ifspeed=interface.get('ifSpeed'),
                    ifalias=interface.get('ifAlias'),
                    ifdescr=interface.get('ifDescr'),
                    ifadminstatus=interface.get('ifAdminStatus'),
                    ifoperstatus=interface.get('ifOperStatus'),
                    cdpcachedeviceid=interface.get('cdpCacheDeviceId'),
                    cdpcachedeviceport=interface.get('cdpCacheDevicePort'),
                    cdpcacheplatform=interface.get('cdpCachePlatform'),
                    lldpremportdesc=interface.get('lldpRemPortDesc'),
                    lldpremsyscapenabled=interface.get(
                        'lldpRemSysCapEnabled'),
                    lldpremsysdesc=interface.get('lldpRemSysDesc'),
                    lldpremsysname=interface.get('lldpRemSysName'),
                    ts_idle=0,
                    enabled=1
                )

                _l1interface.insert_row(row)

        # Log
        log_message = (
            'Updated L1Interface table for host {}'.format(hostname))
        log.log2debug(1029, log_message)

    else:

        # Log
        log_message = (
            'No interfaces detected for for host {}'.format(hostname))
        log.log2debug(1029, log_message)
