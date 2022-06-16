"""Module for querying the Vlan table."""

from sqlalchemy import select, update, null, and_

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Vlan
from switchmap.db.table import RVlan


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_vlan

    Returns:
        result: RVlan object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Vlan).where(Vlan.idx_vlan == idx)
    rows = db.db_select_row(1210, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def exists(idx_device, vlan):
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
    statement = select(Vlan).where(
        and_(
            Vlan.vlan == vlan,
            Vlan.idx_device == idx_device)
    )
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
                vlan=null() if bool(row.vlan) is False else row.vlan,
                name=null() if bool(row.name) is False else row.name.encode(),
                state=null() if bool(row.state) is False else row.state,
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1093, inserts)


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
                'vlan': null() if bool(row.vlan) is False else row.vlan,
                'name': (
                    null() if bool(row.name) is False else row.name.encode()),
                'state': null() if bool(row.state) is False else row.state,
                'enabled': row.enabled
            }
        )
    db.db_update(1120, statement)


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
        vlan=row.vlan,
        name=None if bool(row.name) is False else row.name.decode(),
        state=row.state,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
