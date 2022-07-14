"""Module for querying the Device table."""
import os

import yaml
from sqlalchemy import select, update, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Device as _Device
from switchmap.db.table import RDevice
from switchmap.core import log


class Device():
    """Process configuration file for a host.

    The aim of this class is to process the YAML file consistently
    across multiple manufacturers and present it to other classes
    consistently. That way manufacturer specific code for processing YAML
    data is in one place.

    For example, there isn’t a standard way of reporting ethernet duplex
    values with different manufacturers exposing this data to different MIBs.
    This class file attempts to determine the true duplex value of the
    device by testing the presence of one or more OID values in the data.
    It adds a ‘duplex’ data key to self._ports to act as the canonical key for
    duplex across all devices.

    """

    def __init__(self, config, hostname):
        """Initialize class.

        Args:
            config: Configuration file object
            hostname: Hostname to process

        Returns:
            data_dict: Dict of summary data

        Summary:

            IF-MIB

            A significant portion of this code relies on ifIndex
            IF-MIB::ifStackStatus information. This is stored under the
            'system' key of the device YAML files.

            According to the official IF-MIB file. ifStackStatus is a
            "table containing information on the relationships
            between the multiple sub-layers of network interfaces.  In
            particular, it contains information on which sub-layers run
            'on top of' which other sub-layers, where each sub-layer
            corresponds to a conceptual row in the ifTable.  For
            example, when the sub-layer with ifIndex value x runs over
            the sub-layer with ifIndex value y, then this table
            contains:

              ifStackStatus.x.y=active

            For each ifIndex value, I, which identifies an active
            interface, there are always at least two instantiated rows
            in this table associated with I.  For one of these rows, I
            is the value of ifStackHigherLayer; for the other, I is the
            value of ifStackLowerLayer.  (If I is not involved in
            multiplexing, then these are the only two rows associated
            with I.)

            For example, two rows exist even for an interface which has
            no others stacked on top or below it:

              ifStackStatus.0.x=active
              ifStackStatus.x.0=active"

            In the case of Juniper equipment, VLAN information is only
            visible on subinterfaces of the main interface. For example
            interface ge-0/0/0 won't have VLAN information assigned to it
            directly.

            When a VLAN is assigned to this interface, a subinterface
            ge-0/0/0.0 is automatically created with a non-Ethernet ifType.
            VLAN related OIDs are only maintained for this new subinterface
            only. This makes determining an interface's VLAN based on
            Ethernet ifType more difficult. ifStackStatus maps the ifIndex of
            the primary interface (ge-0/0/0) to the ifIndex of the secondary
            interface (ge-0/0/0.0) which manages higher level protocols and
            data structures such as VLANs and LLDP.

            The primary interface is referred to as the
            ifStackLowerLayer and the secondary subinterface is referred to
            as the ifStackHigherLayer.

            =================================================================

            Layer1 Keys

            The following Layer1 keys are presented by the ethernet_data
            method due to this instantiation:

            l1_nativevlan: A vendor agnostic Native VLAN
            l1_vlan: A list of vendor agnostic VLANs
            l1_trunk: A vendor agnostic flag of "True" if the port is a Trunk
            l1_duplex: A vendor agnostic status code for the duplex setting

        """
        # Initialize key variables
        self._ports = {}
        self._hostname = hostname
        yaml_file = config.topology_device_file(self._hostname)

        # Fail if yaml file doesn't exist
        if os.path.isfile(yaml_file) is False:
            log_message = (
                'YAML file {} for host {} doesn\'t exist! '
                'Try polling devices first.'.format(yaml_file, self._hostname))
            log.log2die(1185, log_message)

        # Read file
        with open(yaml_file, 'r') as file_handle:
            yaml_from_file = file_handle.read()
        yaml_data = yaml.safe_load(yaml_from_file)

        # Create dict for layer1 Ethernet data
        for ifindex, metadata in yaml_data['layer1'].items():
            # Skip non Ethernet ports
            if 'l1_ethernet' not in metadata:
                continue

            # Process metadata
            if bool(metadata['l1_ethernet']) is True:
                # Update ports
                self._ports[int(ifindex)] = metadata

        # Get system
        self._system = yaml_data['system']
        self._misc = yaml_data['misc']

    def system_summary(self):
        """Return system summary data.

        Args:
            None

        Returns:
            data_dict: Dict of summary data

        """
        # Initialize key variables
        data_dict = {}

        # Assign system variables
        v2mib = self._system['SNMPv2-MIB']
        for key in v2mib.keys():
            data_dict[key] = v2mib[key]['0']

        # Add the hostname to the dictionary
        data_dict['hostname'] = self._hostname
        data_dict['timestamp'] = self._misc['timestamp']

        # Return
        return data_dict

    def ethernet_data(self):
        """Return L1 data for Ethernet ports only.

        Args:
            None

        Returns:
            self._ports: L1 data for Ethernet ports

        """
        return self._ports


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_device

    Returns:
        result: RDevice object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(_Device).where(_Device.idx_device == idx)
    rows = db.db_select_row(1208, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def exists(hostname):
    """Determine whether hostname exists in the Device table.

    Args:
        hostname: Device

    Returns:
        result: RDevice tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get hostname from database
    statement = select(_Device).where(_Device.hostname == hostname.encode())
    rows = db.db_select_row(1107, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a Device table entry.

    Args:
        rows: IDevice objects

    Returns:
        None

    """
    # Initialize key variables
    inserts = []

    # Create list
    if isinstance(rows, list) is False:
        rows = [rows]

    # Create objects
    for row in rows:
        inserts.append(
            _Device(
                idx_zone=row.idx_zone,
                idx_event=row.idx_event,
                sys_name=(
                    null() if row.sys_name is None else row.sys_name.encode()),
                hostname=(
                    null() if row.hostname is None else row.hostname.encode()),
                name=(
                    null() if row.name is None else row.name.encode()),
                sys_description=(
                    null() if row.sys_description is None else
                    row.sys_description.encode()),
                sys_objectid=(
                    null() if row.sys_objectid is None else
                    row.sys_objectid.encode()),
                sys_uptime=(
                    null() if row.sys_uptime is None else row.sys_uptime),
                last_polled=(
                    0 if row.last_polled is None else row.last_polled),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1156, inserts)


def update_row(idx, row):
    """Upadate a Device table entry.

    Args:
        idx: idx_device value
        row: IDevice object

    Returns:
        None

    """
    # Update
    statement = update(_Device).where(
        _Device.idx_device == idx).values(
            {
                'idx_zone': row.idx_zone,
                'idx_event': row.idx_event,
                'sys_name': (
                    null() if bool(row.sys_name) is False else
                    row.sys_name.encode()),
                'hostname': (
                    null() if bool(row.hostname) is False else
                    row.hostname.encode()),
                'name': (
                    null() if bool(row.name) is False else
                    row.name.encode()),
                'sys_description': (
                    null() if bool(row.sys_description) is False else
                    row.sys_description.encode()),
                'sys_objectid': (
                    null() if bool(row.sys_objectid) is False else
                    row.sys_objectid.encode()),
                'sys_uptime': (
                    null() if bool(row.sys_uptime) is False else
                    row.sys_uptime),
                'last_polled': (
                    0 if bool(row.last_polled) is False else
                    row.last_polled),
                'enabled': row.enabled
            }
        )
    db.db_update(1110, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Device row

    Returns:
        result: RDevice tuple

    """
    # Initialize key variables
    result = RDevice(
        idx_device=row.idx_device,
        idx_zone=row.idx_zone,
        idx_event=row.idx_event,
        sys_name=(
            None if bool(row.sys_name) is False else row.sys_name.decode()),
        hostname=(
            None if bool(row.hostname) is False else row.hostname.decode()),
        name=(
            None if bool(row.name) is False else row.name.decode()),
        sys_description=(
            None if bool(row.sys_description) is False else
            row.sys_description.decode()),
        sys_objectid=(
            None if bool(row.sys_objectid) is False else
            row.sys_objectid.decode()),
        sys_uptime=row.sys_uptime,
        last_polled=row.last_polled,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
