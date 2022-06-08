"""Module for updating the database with topology data."""

import time
from collections import namedtuple
from switchmap.core import log
from switchmap.db.table import device as _device
from switchmap.db.table import l1interface as _l1interface
from switchmap.db.table import vlan as _vlan
from switchmap.db.table import macip as _macip
from switchmap.db.table import mac as _mac
from switchmap.db.table import oui as _oui
from switchmap.db.table import (
    IDevice, IL1Interface, IVlan, IMacIp, IMac, ProcessMacIP,
    TopologyResult, TopologyUpdates)


def device(data, idx_event):
    """Update the device DB table.

    Args:
        data: Device data
        idx_event: Event idx_event

    Returns:
        None

    """
    # Initialize key variables
    exists = False
    hostname = data['misc']['host']
    row = IDevice(
        idx_location=1,
        idx_event=idx_event,
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


def vlan(data):
    """Update the vlan DB table.

    Args:
        data: Vlan data

    Returns:
        None

    """
    # Initialize key variables
    exists = False
    hostname = data['misc']['host']
    interfaces = data['layer1']
    rows = []
    unique_vlans = []

    # Log
    log_message = (
        'Updating Vlan table for host {}'.format(hostname))
    log.log2debug(1028, log_message)

    # Get device data
    device_ = _device.exists(hostname)

    if bool(device_) is True:

        # Process each interface
        for ifindex, interface in interfaces.items():
            exists = _l1interface.exists(device_.idx_device, ifindex)

            # Process each Vlan
            if bool(exists) is True:
                vlans = interface.get('jm_vlan')
                if isinstance(vlans, list) is True:
                    for next_vlan in vlans:
                        rows.append(
                            IVlan(
                                idx_device=device_.idx_device,
                                vlan=next_vlan,
                                name=None,
                                state=0,
                                enabled=1
                            )
                        )

    # Do Vlan insertions
    unique_vlans = list(set(rows))
    for item in unique_vlans:
        vlan_exists = _vlan.exists(item.idx_device, item.vlan)
        if vlan_exists is False:
            _vlan.insert_row(item)
        else:
            _vlan.update_row(vlan_exists.idx_vlan, item)

    # Log
    log_message = (
        'Updated Vlan table for host {}'.format(hostname))
    log.log2debug(1029, log_message)


def mac(data, idx_event):
    """Update the mac DB table.

    Args:
        data: Mac data
        idx_event: Event idx_event

    Returns:
        None

    """
    # Initialize key variables
    exists = False
    hostname = data['misc']['host']
    interfaces = data['layer1']
    all_macs = []
    unique_macs = []
    unique_ouis = []
    lookup = {}

    # Log
    log_message = (
        'Updating Mac table for host {}'.format(hostname))
    log.log2debug(1028, log_message)

    # Get device data
    device_ = _device.exists(hostname)

    if bool(device_) is True:
        # Process each interface
        for ifindex, interface in interfaces.items():
            exists = _l1interface.exists(device_.idx_device, ifindex)

            # Process each Mac
            if bool(exists) is True:
                these_macs = interface.get('jm_macs')
                if bool(these_macs) is True:
                    all_macs.extend(these_macs)

    # Get macs and ouis
    unique_macs = list(set(_.lower() for _ in all_macs))
    unique_ouis = list(set([_[:6].lower() for _ in unique_macs]))

    # Process ouis
    for item in unique_ouis:
        exists = _oui.exists(item)
        lookup[item] = exists.idx_oui if bool(exists) is True else 1

    # Process macs
    for item in unique_macs:
        exists = _mac.exists(item)
        row = IMac(
            idx_oui=lookup.get(item[:6], 1),
            idx_event=idx_event,
            mac=item,
            enabled=1
        )
        if bool(exists) is False:
            _mac.insert_row(row)
        else:
            _mac.update_row(exists.idx_mac, row)

    # Log
    log_message = (
        'Updated Mac table for host {}'.format(hostname))
    log.log2debug(1029, log_message)


def macip(data):
    """Update the mac DB table.

    Args:
        data: MacIp data

    Returns:
        None

    """
    # Initialize key variables
    ipv6 = None
    ipv4 = None
    hostname = data['misc']['host']
    adds = []
    updates = []

    # Log
    log_message = (
        'Updating MacIp table for host {}'.format(hostname))
    log.log2debug(1028, log_message)

    # Get device data
    device_ = _device.exists(hostname)

    # Get MacIp data
    layer3 = data.get('layer3')
    if bool(layer3) is True and bool(device_) is True:
        ipv4 = layer3.get('ipNetToMediaTable')
        ipv6 = layer3.get('ipNetToPhysicalPhysAddress')

        # Process IPv4 data
        if bool(ipv4) is True:
            result = _process_macip(
                ProcessMacIP(table=ipv4, device=device_, version=4)
            )
            adds.extend(result.adds)
            updates.extend(result.updates)

        # Process IPv6 data
        if bool(ipv6) is True:
            result = _process_macip(
                ProcessMacIP(table=ipv6, device=device_, version=6)
            )
            adds.extend(result.adds)
            updates.extend(result.updates)

    # Do the Updates
    for item in updates:
        _macip.update_row(
            item.idx_macip,
            item.row
        )
    for item in adds:
        _macip.insert_row(item)

    # Log
    log_message = (
        'Updated MacIp table for host {}'.format(hostname))
    log.log2debug(1029, log_message)


def _process_macip(info):
    """Update the mac DB table.

    Args:
        info: ProcessMacIP object

    Returns:
        result

    """
    # Initialize key variables
    adds = []
    updates = []

    # Process data
    for next_ip_addr, next_mac_addr in info.table.items():
        # Create lower case versions of these important variables
        next_ip_addr = next_ip_addr.lower()
        next_mac_addr = next_mac_addr.lower()

        # Update the database
        mac_exists = _mac.exists(next_mac_addr)
        if bool(mac_exists) is True:
            macip_exists = _macip.exists(
                info.device.idx_device, mac_exists.idx_mac, next_ip_addr)
            row = IMacIp(
                idx_device=info.device.idx_device,
                idx_mac=mac_exists.idx_mac,
                ip_=next_ip_addr,
                hostname=None,
                type=info.version,
                enabled=1
            )
            if bool(macip_exists) is True:
                updates.append(
                    TopologyUpdates(
                        idx_macip=macip_exists.idx_macip, row=row))
            else:
                adds.append(row)

    # Return
    result = TopologyResult(adds=adds, updates=updates)
    return result
