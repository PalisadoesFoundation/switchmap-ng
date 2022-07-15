"""Module for querying the VlanPort table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.db import db
from switchmap.db.models import VlanPort
from switchmap.db.table import RVlanPort


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
    rows = db.db_select_row(1099, statement)

    # Return
    for row in rows:
        result = _row(row)
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
            VlanPort.idx_l1interface == idx_l1interface
        )
    )
    rows = db.db_select_row(1109, statement)

    # Return
    for row in rows:
        result = _row(row)
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
    rows = db.db_select_row(1180, statement)

    # Return
    for row in rows:
        result.append(_row(row))
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

    # Create objects
    for row in rows:
        inserts.append(
            VlanPort(
                idx_l1interface=row.idx_l1interface,
                idx_vlan=row.idx_vlan,
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1092, inserts)


def update_row(idx, row):
    """Upadate a VlanPort table entry.

    Args:
        idx: idx_vlanport value
        row: IVlanPort object

    Returns:
        None

    """
    # Update
    statement = update(VlanPort).where(
        VlanPort.idx_vlanport == idx).values(
            {
                'idx_l1interface': row.idx_l1interface,
                'idx_vlan': row.idx_vlan,
                'enabled': row.enabled
            }
        )
    db.db_update(1117, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: VlanPort row

    Returns:
        result: RVlanPort tuple

    """
    # Initialize key variables
    result = RVlanPort(
        idx_vlanport=row.idx_vlanport,
        idx_l1interface=row.idx_l1interface,
        idx_vlan=row.idx_vlan,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
