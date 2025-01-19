"""Module for updating the database with topology data."""

import time
from collections import namedtuple
from copy import deepcopy
from operator import attrgetter

# Application imports
from switchmap.core import log
from switchmap.server.db.ingest.query import device as _misc_device
from switchmap.server.db.misc import interface as _historical
from switchmap.server.db.table import device as _device
from switchmap.server.db.table import l1interface as _l1interface
from switchmap.server.db.table import vlan as _vlan
from switchmap.server.db.table import macport as _macport
from switchmap.server.db.table import vlanport as _vlanport
from switchmap.server.db.table import mac as _mac
from switchmap.server.db.table import (
    IVlan,
    IDevice,
    IMacPort,
    IVlanPort,
    IL1Interface,
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
        """Instantiate the class.

        Args:
            None

        Returns:
            None

        """
        self._vlan = False
        self._vlanport = False
        self._macport = False
        self._l1interface = False

    @property
    def l1interface(self):
        """Provide the value of  the 'l1interface' property."""
        return self._l1interface

    @l1interface.setter
    def l1interface(self, value):
        """Set the 'l1interface' property."""
        self._l1interface = value

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
            dns: Do DNS lookups if True

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
        self.macport()

    def l1interface(self, test=False):
        """Update the L1interface DB table.

        Args:
            test: Sequentially insert values into the database if True.
                Bulk inserts don't insert data with predictable primary keys.

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
        historical = {_.ifname: _ for _ in _historical.interfaces(self._device)}
        rows = []

        # Log
        self.log("L1Interface")

        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            # Get important interface characteristics
            ifadminstatus = interface.get("ifAdminStatus")
            ifoperstatus = interface.get("ifOperStatus")
            ifname = interface.get("ifName")
            previous = historical.get(ifname)

            # Calculate the ts_idle time
            if ifadminstatus == 1 and ifoperstatus == 1:
                # Port enabled with link
                ts_idle = 0
            elif ifadminstatus == 2:
                # Port disabled
                ts_idle = 0
            else:
                # Port enabled without link. Eet ts_idle to the timestamp
                # when the interface was first detected as being idle.
                ts_idle = (
                    previous.ts_idle if bool(previous) else int(time.time())
                )

            # Add new row to the database table
            rows.append(
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
                    ifname=ifname,
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
                    enabled=1,
                )
            )

        # Insert rows
        if bool(rows):
            if bool(test) is False:
                _l1interface.insert_row(rows)
            else:
                for row in sorted(rows, key=attrgetter("ifindex")):
                    _l1interface.insert_row(row)

        # Log
        self.log("L1Interface", updated=True)

        # Everything is completed
        self._status.l1interface = True

    def vlan(self, test=False):
        """Update the Vlan DB table.

        Args:
            test: Sequentially insert values into the database if True.
                Bulk inserts don't insert data with predictable primary keys.

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
        inserts = []

        # Log
        self.log("Vlan")

        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            # Process the VLANs on the interface
            vlans = interface.get("l1_vlans")
            if isinstance(vlans, list) is True:
                for next_vlan in sorted(vlans):
                    rows.append(
                        IVlan(
                            idx_device=self._device.idx_device,
                            vlan=next_vlan,
                            name=None,
                            state=0,
                            enabled=1,
                        )
                    )

        # Remove duplicates
        inserts = list(set(rows))

        # Insert if required
        if bool(inserts) is True:
            if bool(test) is False:
                _vlan.insert_row(inserts)
            else:
                for insert in sorted(
                    inserts, key=attrgetter("vlan", "idx_device")
                ):
                    _vlan.insert_row(insert)

        # Log
        self.log("Vlan", updated=True)

        # Everything is completed
        self._status.vlan = True

    def vlanport(self, test=False):
        """Update the VlanPort DB table.

        Args:
            test: Sequentially insert values into the database if True.
                Bulk inserts don't insert data with predictable primary keys.

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
        db_ifindexes = {_.ifindex: _ for _ in lookup.ifindexes}
        db_vlans = {_.vlan: _ for _ in lookup.vlans}
        db_vlanports = {
            VlanInterface(
                idx_l1interface=_.idx_l1interface, idx_vlan=_.idx_vlan
            ): _
            for _ in _misc_device.vlanports(self._device.idx_device)
        }
        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            if_exists = db_ifindexes.get(ifindex)

            # Check for VLANs on the interface
            if bool(if_exists) is True:
                # Get the vlans
                _vlans = interface.get("l1_vlans")

                # Process found VLANs
                if bool(_vlans) is True:
                    for item in sorted(_vlans):
                        # Ensure the Vlan exists in the database
                        vlan_exists = db_vlans.get(item)

                        if bool(vlan_exists) is True:
                            row = IVlanPort(
                                idx_l1interface=if_exists.idx_l1interface,
                                idx_vlan=vlan_exists.idx_vlan,
                                enabled=1,
                            )

                            # Verify that a VLAN / Port mapping exists
                            vlanport_exists = db_vlanports.get(
                                VlanInterface(
                                    idx_l1interface=if_exists.idx_l1interface,
                                    idx_vlan=vlan_exists.idx_vlan,
                                )
                            )

                            # Update the VLAN / Port mapping
                            if bool(vlanport_exists) is False:
                                inserts.append(row)

        # Insert rows
        if bool(inserts) is True:
            if bool(test) is False:
                _vlanport.insert_row(inserts)
            else:
                for insert in sorted(
                    inserts, key=attrgetter("idx_vlan", "idx_l1interface")
                ):
                    _vlanport.insert_row(insert)

        # Log
        self.log("VlanPort", updated=True)

        # Everything is completed
        self._status.vlanport = True

    def macport(self, test=False):
        """Update the MacPort DB table.

        Args:
            test: Sequentially insert values into the database if True.
                Bulk inserts don't insert data with predictable primary keys.

        Returns:
            None

        """
        # Test prerequisite
        if bool(self._status.vlanport) is False:
            self.log_invalid("MacPort")
            return

        # Initialize key variables
        interfaces = self._data.get("layer1")
        lookup = _lookup(self._device.idx_device)
        inserts = []

        # Log
        self.log("MacPort")

        # Get all the existing ifindexes
        db_ifindexes = {_.ifindex: _ for _ in lookup.ifindexes}

        # Process each interface
        for ifindex, interface in sorted(interfaces.items()):
            if_exists = db_ifindexes.get(ifindex)

            # Process each Mac
            _macs = interface.get("l1_macs")
            if bool(_macs) is True:
                # Update MAC addresses for all zones
                log_message = (
                    "Updating MAC addresses in the DB for device {}"
                    "based on SNMP MIB-BRIDGE entries".format(
                        self._device.hostname
                    )
                )
                log.log2debug(1094, log_message)

                # Iterate over the MACs found
                for item in sorted(_macs):
                    # Ensure the MAC exists in the database
                    mac_exists = _mac.exists(self._device.idx_zone, item)

                    # If True update the port to MAC address mapping
                    if bool(mac_exists) is True:
                        inserts.append(
                            IMacPort(
                                idx_l1interface=if_exists.idx_l1interface,
                                idx_mac=mac_exists.idx_mac,
                                enabled=1,
                            )
                        )

        # Insert rows
        if bool(inserts) is True:
            if bool(test) is False:
                _macport.insert_row(inserts)
            else:
                for insert in sorted(
                    inserts, key=attrgetter("idx_mac", "idx_l1interface")
                ):
                    _macport.insert_row(insert)

        # Log
        self.log("MacPort", updated=True)

        # Everything is completed
        self._status.macport = True

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


def _ifspeed(interface):
    """Get the speed of an interface.

    Args:
        interface: L1Interface dict

    Returns:
        result: Interface speed

    """
    result = interface.get("ifHighSpeed")
    if bool(result) is False:
        result = interface.get("ifSpeed")
        result = result / 1000000 if bool(result) else 0
    return result
