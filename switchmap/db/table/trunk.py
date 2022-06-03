"""Module for querying the Trunk table."""

from sqlalchemy import select, update

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Trunk
from switchmap.db.table import RTrunk


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_trunk

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(
        Trunk.idx_trunk).where(Trunk.idx_trunk == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def insert_row(rows):
    """Create a Trunk table entry.

    Args:
        rows: ITrunk objects

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
            Trunk(
                idx_l1interface=row.idx_l1interface,
                idx_vlan=row.idx_vlan,
                enabled=1
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a Trunk table entry.

    Args:
        idx: idx_trunk value
        row: ITrunk object

    Returns:
        None

    """
    # Update
    statement = update(Trunk).where(
        Trunk.idx_trunk == idx
            ).values(
                {
                    'idx_l1interface': row.idx_l1interface,
                    'idx_vlan': row.idx_vlan,
                    'enabled': row.enabled
                }
            )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Trunk row

    Returns:
        result: RTrunk tuple

    """
    # Initialize key variables
    result = RTrunk(
        idx_trunk=row.idx_trunk,
        idx_l1interface=row.idx_l1interface,
        idx_vlan=row.idx_vlan,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
