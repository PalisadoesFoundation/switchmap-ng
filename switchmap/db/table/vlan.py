"""Module for querying the Vlan table."""

from sqlalchemy import select, update

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Vlan
from switchmap.db.table import RVlan


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_vlan

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Vlan.idx_vlan).where(Vlan.idx_vlan == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def exists(vlan):
    """Determine whether vlan exists in the Vlan table.

    Args:
        vlan: Vlan

    Returns:
        result: RVlan tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get vlan from database
    statement = select(Vlan).where(Vlan.vlan == vlan)
    rows = db.db_select_row(1226, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a Vlan table entry.

    Args:
        rows: IVlan objects

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
            Vlan(
                idx_device=row.idx_device,
                vlan=row.vlan.encode(),
                name=row.name.encode(),
                state=row.state,
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a Vlan table entry.

    Args:
        idx: idx_vlan value
        row: IVlan object

    Returns:
        None

    """
    # Update
    statement = update(Vlan).where(
        Vlan.idx_vlan == idx).values(
            {
                'idx_device': row.idx_device,
                'vlan': row.vlan.decode(),
                'name': row.name.decode(),
                'state': row.state,
                'enabled': row.enabled,
            }
        )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Vlan row

    Returns:
        result: RVlan tuple

    """
    # Initialize key variables
    result = RVlan(
        idx_vlan=row.idx_vlan,
        idx_device=row.idx_device,
        vlan=row.vlan.decode(),
        name=row.name.decode(),
        state=row.state,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
