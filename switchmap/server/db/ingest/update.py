"""Module for updating the database with topology data."""

import time
import socket
from collections import namedtuple
from copy import deepcopy
from operator import attrgetter

# Application imports
from switchmap.core import log
from switchmap.core import general
from switchmap.server.db.ingest.query import device as _misc_device
from switchmap.server.db.table import device as _device
from switchmap.server.db.table import l1interface as _l1interface
from switchmap.server.db.table import vlan as _vlan
from switchmap.server.db.table import macip as _macip
from switchmap.server.db.table import macport as _macport
from switchmap.server.db.table import vlanport as _vlanport
from switchmap.server.db.table import ip as _ip
from switchmap.server.db.table import ipport as _ipport
from switchmap.server.db.table import mac as _mac
from switchmap.server.db.table import oui as _oui
from switchmap.server.db.table import (
    IIp,
    IIpPort,
    IMac,
    IVlan,
    IMacIp,
    IDevice,
    IMacPort,
    IVlanPort,
    IL1Interface,
    TopologyResult,
)


def process(data, idx_zone, dns=True):
    """Process data received from a device.

    Args:
        data: Device data (dict)
        idx_zone: Zone index to which the data belongs
        dns: Do DNS lookups if True

    Returns:
        None

    """
    # Process the device
    meta = device(idx_zone, data)
    _topology = Topology(meta, data, dns=dns)
    _topology.process()


def device(idx_zone, data):
    """Update the Device DB table.

    Args:
        idx_zone: Zone index to which the data belongs
        data: Device data (dict)

    Returns:
        None

    """
    # Initialize key variables
    exists = False
    hostname = data["misc"]["host"]
    row = IDevice(
        idx_zone=idx_zone,
        hostname=hostname,
        name=hostname,
        sys_name=data["system"]["SNMPv2-MIB"]["sysName"][0],
        sys_description=data["system"]["SNMPv2-MIB"]["sysDescr"][0],
        sys_objectid=data["system"]["SNMPv2-MIB"]["sysObjectID"][0],
        sys_uptime=data["system"]["SNMPv2-MIB"]["sysUpTime"][0],
        last_polled=data["misc"]["timestamp"],
        enabled=1,
    )

    # Log
    log_message = "Updating Device table for host {}".format(hostname)
    log.log2debug(1080, log_message)

    # Update the database
    exists = _device.exists(row.idx_zone, row.hostname)
    if bool(exists) is True:
        _device.update_row(exists.idx_device, row)
    else:
        _device.insert_row(row)
        exists = _device.exists(row.idx_zone, row.hostname)

    # Log
    log_message = "Updated Device table for host {}".format(hostname)
    log.log2debug(1137, log_message)

    # Return
    return exists


def _lookup(idx_device):
    """Create in memory lookup data for the device.

    Args:
        idx_device: device index

    Returns:
        result: Lookup object

    """
    # Initialize key variables
    Lookup = namedtuple("Lookup", "ifindexes vlans")

    # Return
    result = Lookup(
        ifindexes=_l1interface.ifindexes(idx_device),
        vlans=_vlan.vlans(idx_device),
    )
    return result


class Status:
    """Tracks the status of various Topology methods."""

    def __init__(self):
        """Instantiate the class."""
        self._vlan = False
        self._vlanport = False
        self._mac = False
        self._macport = False
        self._ip = False
        self._macip = False
        self._ipport = False
        self._l1interface = False

    @property
    def ip(self):
        """Provide the value of  the 'ip' property."""
        return self._ip

    @ip.setter
    def ip(self, value):
        """Set the 'ip' property."""
        self._ip = value

    @property
    def ipport(self):
        """Provide the value of  the 'ipport' property."""
        return self._ipport

    @ipport.setter
    def ipport(self, value):
        """Set the 'ipport' property."""
        self._ipport = value

    @property
    def l1interface(self):
        """Provide the value of  the 'l1interface' property."""
        return self._l1interface

    @l1interface.setter
    def l1interface(self, value):
        """Set the 'l1interface' property."""
        self._l1interface = value

    @property
    def mac(self):
        """Provide the value of  the 'mac' property."""
        return self._mac

    @mac.setter
    def mac(self, value):
        """Set the 'mac' property."""
        self._mac = value

    @property
    def macip(self):
        """Provide the value of  the 'macip' property."""
        return self._macip

    @macip.setter
    def macip(self, value):
        """Set the 'macip' property."""
        self._macip = value

    @property
    def macport(self):
        """Provide the value of  the 'macport' property."""
        return self._macport

    @macport.setter
    def macport(self, value):
        """Set the 'macport' property."""
        self._macport = value

    @property
    def vlanport(self):
        """Provide the value of  the 'vlanport' property."""
        return self._vlanport

    @vlanport.setter
    def vlanport(self, value):
        """Set the 'vlanport' property."""
        self._vlanport = value

    @property
    def vlan(self):
        """Provide the value of  the 'vlan' property."""
        return self._vlan

    @vlan.setter
    def vlan(self, value):
        """Set the 'vlan' property."""
        self._vlan = value


class Topology:
    """Update Device data in the database."""

    def __init__(self, exists, data, dns=True):
        """Initialize class.

        Args:
            exists: RDevice object
            data: Dict of device data

        Returns:
            None

        """
        # Initialize key variables
        self._data = deepcopy(data)
        self._device = exists
        self._dns = dns
        self._valid = False not in [
            bool(_device.idx_exists(exists.idx_device)),
            bool(data),
            isinstance(data, dict),
        ]
        self._status = Status()
        self._start = int(time.time())

    def process(self):
        """Process data received from a device.

        Args:
            None

        Returns:
            None

        """
        self.l1interface()
        self.vlan()
        self.vlanport()
        self.mac()
        self.macport()
        self.ip()
        self.macip()

    def l1interface(self):
        """Update the L1interface DB table.

        Args:
            None

        Returns:
            None

        """
        # Test validity
        if bool(self._valid) is False:
            # Log
            log_message = "No interfaces detected for for host {}".format(
                self._device.hostname
            )
            log.log2debug(1021, log_message)
            return

        # Initialize more key variables
        data = self._data
        interfaces = data.get("layer1")
        inserts = []

        # Log
        self.log("L1Interface")

        # Get all the existing ifindexes
        all_ifindexes = {
            _.ifindex: _ for _ in _lookup(self._device.idx_device).ifindexes
        }

        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            exists = all_ifindexes.get(ifindex)

            # Update the database
            if bool(exists) is True:
                # Calculate the ts_idle time
                ifadminstatus = interface.get("ifAdminStatus")
                ifoperstatus = interface.get("ifOperStatus")
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
                    idx_device=self._device.idx_device,
                    ifindex=ifindex,
                    duplex=interface.get("l1_duplex"),
                    ethernet=int(bool(interface.get("l1_ethernet"))),
                    nativevlan=interface.get("l1_nativevlan"),
                    trunk=int(bool(interface.get("l1_trunk"))),
                    ifspeed=_ifspeed(interface),
                    iftype=interface.get("ifType"),
                    ifalias=interface.get("ifAlias"),
                    ifname=interface.get("ifName"),
                    ifdescr=interface.get("ifDescr"),
                    ifadminstatus=interface.get("ifAdminStatus"),
                    ifoperstatus=interface.get("ifOperStatus"),
                    cdpcachedeviceid=interface.get("cdpCacheDeviceId"),
                    cdpcachedeviceport=interface.get("cdpCacheDevicePort"),
                    cdpcacheplatform=interface.get("cdpCachePlatform"),
                    lldpremportdesc=interface.get("lldpRemPortDesc"),
                    lldpremsyscapenabled=interface.get("lldpRemSysCapEnabled"),
                    lldpremsysdesc=interface.get("lldpRemSysDesc"),
                    lldpremsysname=interface.get("lldpRemSysName"),
                    ts_idle=ts_idle,
                    enabled=int(bool(exists.enabled)),
                )

                _l1interface.update_row(exists.idx_l1interface, row)
            else:
                # Add new row to the database table
                inserts.append(
                    IL1Interface(
                        idx_device=self._device.idx_device,
                        ifindex=ifindex,
                        duplex=interface.get("l1_duplex"),
                        ethernet=int(bool(interface.get("l1_ethernet"))),
                        nativevlan=interface.get("l1_nativevlan"),
                        trunk=int(bool(interface.get("l1_trunk"))),
                        ifspeed=_ifspeed(interface),
                        iftype=interface.get("ifType"),
                        ifalias=interface.get("ifAlias"),
                        ifname=interface.get("ifName"),
                        ifdescr=interface.get("ifDescr"),
                        ifadminstatus=interface.get("ifAdminStatus"),
                        ifoperstatus=interface.get("ifOperStatus"),
                        cdpcachedeviceid=interface.get("cdpCacheDeviceId"),
                        cdpcachedeviceport=interface.get("cdpCacheDevicePort"),
                        cdpcacheplatform=interface.get("cdpCachePlatform"),
                        lldpremportdesc=interface.get("lldpRemPortDesc"),
                        lldpremsyscapenabled=interface.get(
                            "lldpRemSysCapEnabled"
                        ),
                        lldpremsysdesc=interface.get("lldpRemSysDesc"),
                        lldpremsysname=interface.get("lldpRemSysName"),
                        ts_idle=0,
                        enabled=1,
                    )
                )

        # Insert if necessary
        if bool(inserts):
            _l1interface.insert_row(inserts)

        # Log
        self.log("L1Interface", updated=True)

        # Everything is completed
        self._status.l1interface = True

    def vlan(self):
        """Update the Vlan DB table.

        Args:
            None

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.l1interface) is False:
            self.log_invalid("Vlan")
            return

        # Initialize key variables
        interfaces = self._data.get("layer1")
        rows = []
        unique_vlans = []
        inserts = []
        lookup = _lookup(self._device.idx_device)

        # Log
        self.log("Vlan")

        # Get all the existing ifindexes and VLANs.
        all_vlans = {_.vlan: _ for _ in lookup.vlans}

        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            # Process the VLANs on the interface
            vlans = interface.get("l1_vlans")
            if isinstance(vlans, list) is True:
                for next_vlan in vlans:
                    rows.append(
                        IVlan(
                            idx_device=self._device.idx_device,
                            vlan=next_vlan,
                            name=None,
                            state=0,
                            enabled=1,
                        )
                    )

        # Do VLAN insertions
        unique_vlans = list(set(rows))

        # Sort by VLAN number and idx_device
        unique_vlans.sort(key=lambda x: (x.vlan, x.idx_device))

        for item in unique_vlans:
            # vlan_exists = _vlan.exists(item.idx_device, item.vlan)
            vlan_exists = all_vlans.get(item.vlan)

            if bool(vlan_exists) is False:
                inserts.append(item)
            else:
                _vlan.update_row(vlan_exists, item)

        # Insert if required
        if bool(inserts) is True:
            _vlan.insert_row(inserts)

        # Log
        self.log("Vlan", updated=True)

        # Everything is completed
        self._status.vlan = True

    def vlanport(self):
        """Update the VlanPort DB table.

        Args:
            None

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.vlan) is False:
            self.log_invalid("VlanPort")
            return

        # Initialize key variables
        VlanInterface = namedtuple("VlanInterface", "idx_l1interface idx_vlan")
        interfaces = self._data.get("layer1")
        lookup = _lookup(self._device.idx_device)
        inserts = []

        # Log
        self.log("VlanPort")

        # Get all the existing ifindexes, VLANs and VlanPorts
        all_ifindexes = {_.ifindex: _ for _ in lookup.ifindexes}
        all_vlans = {_.vlan: _ for _ in lookup.vlans}
        all_vlan_ports = {
            VlanInterface(
                idx_l1interface=_.idx_l1interface, idx_vlan=_.idx_vlan
            ): _
            for _ in _misc_device.vlanports(self._device.idx_device)
        }
        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            l1_exists = all_ifindexes.get(ifindex)

            # Check for VLANs on the interface
            if bool(l1_exists) is True:
                _vlans = interface.get("l1_vlans")

                # Process found VLANs
                if bool(_vlans) is True:
                    for item in sorted(_vlans):
                        # Ensure the Vlan exists in the database
                        vlan_exists = all_vlans.get(item)
                        if bool(vlan_exists) is True:
                            row = IVlanPort(
                                idx_l1interface=l1_exists.idx_l1interface,
                                idx_vlan=vlan_exists.idx_vlan,
                                enabled=1,
                            )

                            # Verify that a VLAN / Port mapping exists
                            vlanport_exists = all_vlan_ports.get(
                                VlanInterface(
                                    idx_l1interface=l1_exists.idx_l1interface,
                                    idx_vlan=vlan_exists.idx_vlan,
                                )
                            )

                            # Update the VLAN / Port mapping
                            if bool(vlanport_exists) is True:
                                _vlanport.update_row(
                                    vlanport_exists.idx_vlanport, row
                                )
                            else:
                                inserts.append(row)

        # Insert if required
        if bool(inserts) is True:
            _vlanport.insert_row(inserts)

        # Log
        self.log("VlanPort", updated=True)

        # Everything is completed
        self._status.vlanport = True

    def mac(self):
        """Update the Mac DB table.

        Args:
            None

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.vlanport) is False:
            self.log_invalid("Mac")
            return

        # Initialize key variables
        exists = False
        interfaces = self._data.get("layer1")
        all_macs = []
        unique_macs = []
        unique_ouis = []
        inserts = []
        lookup = {}
        db_lookup = _lookup(self._device.idx_device)

        # Log
        self.log("Mac")

        # Get all the existing ifindexes
        all_ifindexes = [_.ifindex for _ in db_lookup.ifindexes]

        # Process each interface
        for ifindex, interface in interfaces.items():
            exists = ifindex in all_ifindexes

            # Process each Mac
            if bool(exists) is True:
                these_macs = interface.get("l1_macs")
                if bool(these_macs) is True:
                    all_macs.extend(these_macs)

        # Get macs and ouis
        unique_macs = list(set(_.lower() for _ in all_macs))
        unique_ouis = list(set([_[:6].lower() for _ in unique_macs]))

        # Process ouis
        for item in sorted(unique_ouis):
            exists = _oui.exists(item)
            lookup[item] = exists.idx_oui if bool(exists) is True else 1

        # Process macs
        for item in sorted(unique_macs):
            exists = _mac.exists(self._device.idx_zone, item)
            row = IMac(
                idx_oui=lookup.get(item[:6], 1),
                idx_zone=self._device.idx_zone,
                mac=item,
                enabled=1,
            )
            if bool(exists) is False:
                # _mac.insert_row(row)
                inserts.append(row)
            else:
                _mac.update_row(exists.idx_mac, row)

        # Insert if required
        if bool(inserts) is True:
            _mac.insert_row(inserts)

        # Log
        self.log("Mac", updated=True)

        # Everything is completed
        self._status.mac = True

    def macport(self):
        """Update the MacPort DB table.

        Args:
        None

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.mac) is False:
            self.log_invalid("MacPort")
            return

        # Initialize key variables
        interfaces = self._data.get("layer1")
        lookup = _lookup(self._device.idx_device)

        # Log
        self.log("MacPort")

        # Get all the existing ifindexes
        all_ifindexes = {_.ifindex: _ for _ in lookup.ifindexes}

        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            l1_exists = all_ifindexes.get(ifindex)

            # Process each Mac
            _macs = interface.get("l1_macs")
            if bool(_macs) is True:
                for item in sorted(_macs):
                    # Ensure the Mac exists in the database
                    mac_exists = _mac.exists(self._device.idx_zone, item)
                    if bool(mac_exists) is True:
                        row = IMacPort(
                            idx_l1interface=l1_exists.idx_l1interface,
                            idx_mac=mac_exists.idx_mac,
                            enabled=1,
                        )
                        # Update the MacPort database table
                        macport_exists = _macport.exists(
                            l1_exists.idx_l1interface,
                            mac_exists.idx_mac,
                        )
                        if bool(macport_exists) is True:
                            _macport.update_row(
                                macport_exists.idx_macport, row
                            )
                        else:
                            _macport.insert_row(row)

        # Log
        self.log("MacPort", updated=True)

        # Everything is completed
        self._status.macport = True

    def ip(self):
        """Update the Ip DB table.

        Args:
            data: Ip data

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.macport) is False:
            self.log_invalid("Ip")
            return

        # Initialize key variables
        dns = self._dns
        ipv6 = None
        ipv4 = None
        adds = []
        updates = []

        # Log
        self.log("Ip")

        # Get Ip data
        layer3 = self._data.get("layer3")
        if bool(layer3) is True:
            ipv4 = layer3.get("ipNetToMediaTable")
            ipv6 = layer3.get("ipNetToPhysicalPhysAddress")

            # Process arp table data
            for table in [ipv4, ipv6]:
                if bool(table) is True:
                    result = _process_ip(
                        self._device.idx_zone,
                        table,
                        dns=dns,
                    )
                    adds.extend(result.adds)
                    updates.extend(result.updates)

        # Do the Updates
        for item in sorted(updates):
            _ip.update_row(item.idx_ip, item.row)

        # Do the adds
        _ip.insert_row(sorted(adds))

        # Log
        self.log("Ip", updated=True)

        # Everything is completed
        self._status.ip = True

    def macip(self):
        """Update the MacIp DB table.

        Args:
            data: MacIp data

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.macport) is False:
            self.log_invalid("MacIp")
            return

        # Initialize key variables
        ipv6 = None
        ipv4 = None
        adds = []
        updates = []

        # Log
        self.log("MacIp")

        # Get MacIp data
        layer3 = self._data.get("layer3")
        if bool(layer3) is True:
            ipv4 = layer3.get("ipNetToMediaTable")
            ipv6 = layer3.get("ipNetToPhysicalPhysAddress")

            for table in [ipv4, ipv6]:
                if bool(table):
                    result = _process_macip(self._device.idx_zone, table)
                    adds.extend(result.adds)
                    updates.extend(result.updates)

        # Do the Updates
        for item in sorted(updates):
            _macip.update_row(item.idx_macip, item.row)

        # Do the adds
        _macip.insert_row(sorted(adds))

        # Log
        self.log("MacIp", updated=True)

        # Everything is completed
        self._status.macip = True

    def ipport(self):
        """Update the IpPort DB table.

        Args:
            data: IpPort data

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.macip) is False:
            self.log_invalid("IpPort")
            return

        # Initialize key variables
        ipv6 = None
        ipv4 = None
        adds = []
        updates = []

        # Log
        self.log("IpPort")

        # Get IpPort data
        layer3 = self._data.get("layer3")
        if bool(layer3) is True:
            ipv4 = layer3.get("ipNetToMediaTable")
            ipv6 = layer3.get("ipNetToPhysicalPhysAddress")

            for table in [ipv4, ipv6]:
                if bool(table):
                    result = _process_ipport(self._device.idx_zone, table)
                    adds.extend(result.adds)
                    updates.extend(result.updates)

        # Do the Updates
        for item in sorted(updates):
            _ipport.update_row(item.idx_ipport, item.row)

        # Do the adds
        _ipport.insert_row(sorted(adds))

        # Log
        self.log("IpPort", updated=True)

        # Everything is completed
        self._status.ipport = True

    def log(self, table, updated=False):
        """Create standardized log messaging.

        Args:
            table: Name of table being updated
            updated: True if the table has been updated

        Returns:
            None

        """
        # Initialize key variables
        log_message = '\
{} table update "{}" for host {}, {} seconds after starting'.format(
            "Completed" if bool(updated) else "Starting",
            table,
            self._device.hostname,
            int(time.time()) - self._start,
        )
        log.log2debug(1028, log_message)

    def log_invalid(self, table):
        """Create standardized log messaging for invalid states.

        Args:
            table: Name of table being updated
            updated: True if the table has been updated

        Returns:
            None

        """
        # Initialize key variables
        log_message = "\
Invalid update sequence for table {} when processing host {}, {} seconds\
after starting".format(
            table,
            self._device.hostname,
            int(time.time()) - self._start,
        )
        log.log2debug(1029, log_message)


def _process_ip(idx_zone, table, dns=True):
    """Update the mac DB table.

    Args:
        idx_zone: Zone index
        table: ARP table keyed by ip address
        dns: Do DNS lookup if True

    Returns:
        result

    """
    # Initialize key variables
    adds = []
    updates = []

    # Process data
    for next_ip, _ in table.items():
        # Create expanded lower case versions of the IP address
        myp = general.ipaddress(next_ip)
        if bool(myp) is False:
            continue

        # Get the status in the database
        db_row = _ip.exists(idx_zone, myp.address)

        # Get hostname for DB
        if bool(dns) is True:
            try:
                hostname = socket.gethostbyaddr(myp.address)[0]
            except:
                hostname = None
        else:
            hostname = None

        # Create a DB record
        row = IIp(
            idx_zone=idx_zone,
            address=myp.address,
            hostname=hostname,
            version=myp.version,
            enabled=1,
        )

        # Prepare for insert or update
        if bool(db_row) is True:
            if row == IIp(
                idx_zone=db_row.idx_zone,
                address=db_row.address,
                hostname=db_row.hostname,
                version=db_row.version,
                enabled=db_row.enabled,
            ):
                continue
            else:
                updates.append(row)
        else:
            adds.append(row)

    # Return
    result = TopologyResult(adds=adds, updates=updates)
    return result


def _process_macip(idx_zone, table):
    """Update the mac DB table.

    Args:
        idx_zone: Zone index
        table: ARP table keyed by ip address

    Returns:
        result

    """
    # Initialize key variables
    adds = []
    updates = []

    # Process data
    for next_ip, next_mac in table.items():
        # Create expanded lower case versions of the IP address
        myp = general.ipaddress(next_ip)
        if bool(myp) is False:
            continue

        # Create lowercase version of mac address
        next_mac = general.mac(next_mac)

        # Update the database
        mac_exists = _mac.exists(idx_zone, next_mac)
        ip_exists = _ip.exists(idx_zone, myp.address)

        # Insert
        if bool(mac_exists) and bool(ip_exists):
            macip_exists = _macip.exists(mac_exists.idx_mac, ip_exists.idx_ip)
            if bool(macip_exists) is False:
                # Create a DB record
                adds.append(
                    IMacIp(
                        idx_ip=ip_exists.idx_ip,
                        idx_mac=mac_exists.idx_mac,
                        enabled=1,
                    )
                )

    # Return
    result = TopologyResult(adds=adds, updates=updates)
    return result


def _process_ipport(idx_zone, table):
    """Update the mac DB table.

    Args:
        idx_zone: Zone index
        table: ARP table keyed by ip address

    Returns:
        result

    """
    # Initialize key variables
    adds = []
    updates = []

    # Process data
    for next_ip, next_mac in table.items():
        # Create expanded lower case versions of the IP address
        myp = general.ipaddress(next_ip)
        if bool(myp) is False:
            continue

        # Create lowercase version of mac address
        next_mac = general.mac(next_mac)

        # Verify prerequisites
        mac_exists = _mac.exists(idx_zone, next_mac)
        ip_exists = _ip.exists(idx_zone, myp.address)

        # Skip if the IP doesn't exist, or else the following logic will crash
        if bool(ip_exists) is False:
            continue

        # Iterate over existing MAC entries
        if bool(mac_exists) is True:
            # Get the ports on which the MAC address resides
            macports = _macport.find_idx_mac(mac_exists.idx_mac)

            # Iterate over the MAC assignments to interfaces
            for macport in macports:
                # Assign the IP to this port
                adds.append(
                    IIpPort(
                        idx_l1interface=macport.idx_l1interface,
                        idx_ip=ip_exists.idx_ip,
                        enabled=1,
                    )
                )

    # Sort the results for better testing
    adds = sorted(adds, key=attrgetter("idx_l1interface", "idx_ip"))

    # Return
    result = TopologyResult(adds=adds, updates=updates)
    return result


def _ifspeed(interface):
    """Get the speed of an interface.

    Args:
        interface: L1Interface dict

    Returns:
        result

    """
    result = interface.get("ifHighSpeed")
    if bool(result) is False:
        result = interface.get("ifSpeed")
        result = result / 1000000 if bool(result) else 0
    return result
