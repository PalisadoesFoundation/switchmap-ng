"""Module for querying the MacTable table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.db import db
from switchmap.db.models import MacTable
from switchmap.db.table import RMacTable


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_mactable

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(
        MacTable.idx_mactable).where(MacTable.idx_mactable == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def insert_row(rows):
    """Create a MacTable table entry.

    Args:
        rows: IMacTable objects

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
            MacTable(
                idx_device=row.idx_device,
                idx_oui=row.idx_oui,
                ip_=row.ip_.encode(),
                mac=row.mac.encode(),
                hostname=row.hostname.encode(),
                type=row.type,
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a MacTable table entry.

    Args:
        idx: idx_mactable value
        row: IMacTable object

    Returns:
        None

    """
    # Update
    statement = update(MacTable).where(
        MacTable.idx_mactable == idx).values(
            {
                'idx_device': row.idx_device,
                'idx_oui': row.idx_oui,
                'ip_': row.ip_.encode(),
                'mac': row.mac.encode(),
                'hostname': row.hostname.encode(),
                'enabled': row.enabled
            }
        )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: MacTable row

    Returns:
        result: RMacTable tuple

    """
    # Initialize key variables
    result = RMacTable(
        idx_mactable=row.idx_mactable,
        idx_device=row.idx_device,
        idx_oui=row.idx_oui,
        ip_=row.ip_.decode(),
        mac=row.mac.decode(),
        hostname=row.hostname.decode(),
        type=row.type,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
