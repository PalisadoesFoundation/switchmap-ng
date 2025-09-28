"""Module for querying the SystemStat table."""

from sqlalchemy import select, update, and_, null

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import SystemStat
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.
    Args:
        idx: idx_systemstat
    Returns:
        results: SystemStat object
    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(SystemStat).where(SystemStat.idx_systemstat == idx)
    rows = db.db_select_row(1500, statement)

    # Return
    for row in rows:
        #! i think we are just finding if row exist we are ret bool
        result = _rows.systemstat(row)
        #! why breaking just after appending result for single row
        #! are we just checking if there exists a single row or not
        break
    return result


def device_exists(idx_device):
    """Determine whether SystemStat record exists for a device.
    Args:
        idx_device: Device index
    Returns:
        result: SystemStat object or False if not found
    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(SystemStat).where(SystemStat.idx_device == idx_device)
    rows = db.db_select_row(1502, statement)

    # Return the first record found
    for row in rows:
        result = _rows.systemstat(row)
        break
    return result


def insert_row(rows):
    """Create a SystemStat table entry.

    Args:
        rows: SystemStat objects
    Returns:
        None
    """
    # Initialize key variables
    inserts = []

    if isinstance(rows, list) is False:
        rows = [rows]

    # Remove any duplicates
    rows = list(set(rows))

    # Create objects
    for row in rows:
        inserts.append(
            {
                "idx_device": row.idx_device,
                "cpu_5min": row.cpu_5min,
                "mem_used": row.mem_used,
                "mem_free": row.mem_free,
            }
        )

    # Insert
    if bool(inserts):
        db.db_insert_row(1501, SystemStat, inserts)


def update_row(idx, row):
    """Update a systemstat table entry.
    Args:
        idx: idx_systemstat value
        row: SystemStat object
    Returns:
        None
    """
    # Update
    statement = (
        update(SystemStat)
        .where(SystemStat.idx_systemstat == idx)
        .values(
            {
                "idx_device": row.idx_device,
                "cpu_5min": None if row.cpu_5min is None else row.cpu_5min,
                "mem_used": None if row.mem_used is None else row.mem_used,
                "mem_free": None if row.mem_free is None else row.mem_free,
            }
        )
    )

    db.db_update(1510, statement)
