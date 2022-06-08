"""Module for querying the Event table."""

from sqlalchemy import select, update

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Event
from switchmap.db.table import REvent


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_event

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Event.idx_event).where(Event.idx_event == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


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
    statement = select(Event).where(Event.event == event.encode())
    rows = db.db_select_row(1226, statement)

    # Return
    for row in rows:
        result = _row(row)
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
        inserts.append(
            Event(
                event=row.event.encode(),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a Event table entry.

    Args:
        idx: idx_event value
        row: IEvent object

    Returns:
        None

    """
    # Update
    statement = update(Event).where(
        Event.idx_event == idx).values(
            {
                'event': row.event.encode(),
                'enabled': row.enabled,
            }
        )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Event row

    Returns:
        result: REvent tuple

    """
    # Initialize key variables
    result = REvent(
        idx_event=row.idx_event,
        event=row.event.decode(),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
