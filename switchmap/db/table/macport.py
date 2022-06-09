"""Module for querying the MacPort table."""

from sqlalchemy import select, update, and_, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import MacPort
from switchmap.db.table import RMacPort


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
    statement = select(
        MacPort.idx_macport).where(MacPort.idx_macport == idx)
    rows = db.db_select(1099, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


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
            MacPort.idx_l1interface == idx_l1interface
        )
    )
    rows = db.db_select_row(1109, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
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
                enabled=row.enabled
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
    statement = update(MacPort).where(
        MacPort.idx_macport == idx).values(
            {
                'idx_l1interface': row.idx_l1interface,
                'idx_mac': row.idx_mac,
                'idx_macport': row.idx_macport,
                'enabled': row.enabled
            }
        )
    db.db_update(1117, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: MacPort row

    Returns:
        result: RMacPort tuple

    """
    # Initialize key variables
    result = RMacPort(
        idx_macport=row.idx_macport,
        idx_l1interface=row.idx_l1interface,
        idx_mac=row.idx_mac,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
