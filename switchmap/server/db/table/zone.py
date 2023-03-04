"""Module for querying the Zone table."""


from sqlalchemy import select, update, null, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Zone
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_zone

    Returns:
        result: RZone record

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Zone).where(Zone.idx_zone == idx)
    rows = db.db_select_row(1204, statement)

    # Return
    for row in rows:
        result = _rows.zone(row)
        break
    return result


def exists(idx_event, name):
    """Determine whether name exists in the Zone table.

    Args:
        idx_event: Event index
        name: Zone

    Returns:
        result: RZone tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get name from database
    statement = select(Zone).where(
        and_(Zone.name == name.encode(), Zone.idx_event == idx_event)
    )
    rows = db.db_select_row(1175, statement)

    # Return
    for row in rows:
        result = _rows.zone(row)
        break
    return result


def zones(idx_event):
    """Get all Zones for a event.

    Args:
        idx_event: Event index

    Returns:
        result: list of RZone tuples

    """
    # Initialize key variables
    result = []
    rows = []

    # Get zone from database
    statement = select(Zone).where(Zone.idx_event == idx_event)
    rows = db.db_select_row(1226, statement)

    # Return
    for row in rows:
        result.append(_rows.zone(row))
    return result


def insert_row(rows):
    """Create a Zone table entry.

    Args:
        rows: IZone objects

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
            Zone(
                idx_event=row.idx_event,
                name=(
                    null() if bool(row.name) is False else row.name.encode()
                ),
                notes=(
                    null() if bool(row.notes) is False else row.notes.encode()
                ),
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1155, inserts)


def update_row(idx, row):
    """Upadate a Zone table entry.

    Args:
        idx: idx_zone value
        row: IZone object

    Returns:
        None

    """
    # Update
    statement = (
        update(Zone)
        .where(Zone.idx_zone == idx)
        .values(
            {
                "idx_event": row.idx_event,
                "name": (
                    null() if bool(row.name) is False else row.name.encode()
                ),
                "notes": (
                    null() if bool(row.notes) is False else row.notes.encode()
                ),
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1113, statement)
