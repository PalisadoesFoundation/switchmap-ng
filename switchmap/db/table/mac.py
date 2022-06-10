"""Module for querying the Mac table."""

from sqlalchemy import select, update, and_, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Mac
from switchmap.db.table import RMac


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_mac

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(
        Mac.idx_mac).where(Mac.idx_mac == idx)
    rows = db.db_select(1097, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def exists(mac):
    """Determine whether idx_event exists in the Mac table.

    Args:
        mac: Mac address

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(Mac).where(Mac.mac == mac.encode())
    rows = db.db_select_row(1202, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a Mac table entry.

    Args:
        rows: IMac objects

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
            Mac(
                idx_oui=row.idx_oui,
                idx_event=row.idx_event,
                mac=(
                    null() if bool(row.mac) is False else
                    row.mac.encode()),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1087, inserts)


def update_row(idx, row):
    """Upadate a Mac table entry.

    Args:
        idx: idx_mac value
        row: IMac object

    Returns:
        None

    """
    # Update
    statement = update(Mac).where(
        Mac.idx_mac == idx).values(
            {
                'idx_oui': row.idx_oui,
                'idx_event': row.idx_event,
                'mac': (
                    null() if bool(row.mac) is False else
                    row.mac.encode()),
                'enabled': row.enabled
            }
        )
    db.db_update(1114, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Mac row

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = RMac(
        idx_mac=row.idx_mac,
        idx_oui=row.idx_oui,
        idx_event=row.idx_event,
        mac=(
            None if bool(row.mac) is False else row.mac.decode()),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
