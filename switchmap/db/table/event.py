"""Module for querying the Event table."""

from sqlalchemy import select, update

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Event
from switchmap.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_event

    Returns:
        result: RZone object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Event).where(Event.idx_event == idx)
    rows = db.db_select_row(1122, statement)

    # Return
    for row in rows:
        result = _rows.event(row)
        break
    return result


def exists(event):
    """Determine whether event exists in the Event table.

    Args:
        event: Event

    Returns:
        result: REvent tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get event from database
    statement = select(Event).where(Event.name == event.encode())
    rows = db.db_select_row(1207, statement)

    # Return
    for row in rows:
        result = _rows.event(row)
        break
    return result


def insert_row(rows):
    """Create a Event table entry.

    Args:
        rows: IEvent objects

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
        inserts.append(Event(name=row.name.encode(), enabled=row.enabled))

    # Insert
    if bool(inserts):
        db.db_add_all(1157, inserts)


def update_row(idx, row):
    """Upadate a Event table entry.

    Args:
        idx: idx_event value
        row: IEvent object

    Returns:
        None

    """
    # Update
    statement = (
        update(Event)
        .where(Event.idx_event == idx)
        .values(
            {
                "name": row.name.encode(),
                "enabled": row.enabled,
            }
        )
    )
    db.db_update(1111, statement)
