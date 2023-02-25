"""Module for querying the MacPort table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import MacPort
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_macport

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(MacPort).where(MacPort.idx_macport == idx)
    rows = db.db_select_row(1099, statement)

    # Return
    for row in rows:
        result = _rows.macport(row)
        break
    return result


def exists(idx_l1interface, idx_mac):
    """Determine whether entry exists in the MacPort table.

    Args:
        idx_l1interface: Device.idx_l1interface
        idx_mac: Mac.idx_mac

    Returns:
        result: RMacPort tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(MacPort).where(
        and_(
            MacPort.idx_mac == idx_mac,
            MacPort.idx_l1interface == idx_l1interface,
        )
    )
    rows = db.db_select_row(1109, statement)

    # Return
    for row in rows:
        result = _rows.macport(row)
        break
    return result


def find_idx_mac(idx_mac):
    """Find all ports on which MAC address has been found.

    Args:
        idx_mac: Mac.idx_mac

    Returns:
        result: RMacPort tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from dataase
    statement = select(MacPort).where(MacPort.idx_mac == idx_mac)
    rows = db.db_select_row(1180, statement)

    # Return
    for row in rows:
        result.append(_rows.macport(row))
    return result


def insert_row(rows):
    """Create a MacPort table entry.

    Args:
        rows: IMacPort objects

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
            MacPort(
                idx_l1interface=row.idx_l1interface,
                idx_mac=row.idx_mac,
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1092, inserts)


def update_row(idx, row):
    """Upadate a MacPort table entry.

    Args:
        idx: idx_macport value
        row: IMacPort object

    Returns:
        None

    """
    # Update
    statement = (
        update(MacPort)
        .where(MacPort.idx_macport == idx)
        .values(
            {
                "idx_l1interface": row.idx_l1interface,
                "idx_mac": row.idx_mac,
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1117, statement)
