"""Module for querying the VlanPort table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import VlanPort
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_vlanport

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(VlanPort).where(VlanPort.idx_vlanport == idx)
    rows = db.db_select_row(1192, statement)

    # Return
    for row in rows:
        result = _rows.vlanport(row)
        break
    return result


def exists(idx_l1interface, idx_vlan):
    """Determine whether entry exists in the VlanPort table.

    Args:
        idx_l1interface: Device.idx_l1interface
        idx_vlan: Vlan.idx_vlan

    Returns:
        result: RVlanPort tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(VlanPort).where(
        and_(
            VlanPort.idx_vlan == idx_vlan,
            VlanPort.idx_l1interface == idx_l1interface,
        )
    )
    rows = db.db_select_row(1026, statement)

    # Return
    for row in rows:
        result = _rows.vlanport(row)
        break
    return result


def find_idx_vlan(idx_vlan):
    """Find all ports on which MAC address has been found.

    Args:
        idx_vlan: Vlan.idx_vlan

    Returns:
        result: RVlanPort tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from dataase
    statement = select(VlanPort).where(VlanPort.idx_vlan == idx_vlan)
    rows = db.db_select_row(1189, statement)

    # Return
    for row in rows:
        result.append(_rows.vlanport(row))
    return result


def insert_row(rows):
    """Create a VlanPort table entry.

    Args:
        rows: IVlanPort objects

    Returns:
        None

    """
    # Initialize key variables
    inserts = []

    # Create list
    if isinstance(rows, list) is False:
        rows = [rows]

    # Remove any duplicates
    rows = list(set(rows))

    # Create objects
    for row in rows:
        inserts.append(
            VlanPort(
                idx_l1interface=row.idx_l1interface,
                idx_vlan=row.idx_vlan,
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1185, inserts)


def update_row(idx, row):
    """Upadate a VlanPort table entry.

    Args:
        idx: idx_vlanport value
        row: IVlanPort object

    Returns:
        None

    """
    # Update
    statement = (
        update(VlanPort)
        .where(VlanPort.idx_vlanport == idx)
        .values(
            {
                "idx_l1interface": row.idx_l1interface,
                "idx_vlan": row.idx_vlan,
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1187, statement)
