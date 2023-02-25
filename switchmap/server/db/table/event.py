"""Module for querying the Event table."""

from sqlalchemy import select, update, delete as _delete

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Event
from switchmap.server.db.misc import rows as _rows

from switchmap.server.db.models import Root
from switchmap.server.db.table import IEvent
from switchmap.server.db.table import IRoot
from switchmap.server.db.table import root
from switchmap.core import general


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_event

    Returns:
        result: REvent object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Event).where(Event.idx_event == idx)
    rows = db.db_select_row(1032, statement)

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
        inserts.append(
            Event(
                name=row.name.encode(), enabled=int(bool(row.enabled) is True)
            )
        )

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
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1111, statement)


def events():
    """Get list of Events.

    Args:
        idx: idx_event

    Returns:
        result: REvent object

    """
    # Initialize key variables
    result = []
    rows = []

    # Get data
    statement = select(Event)
    rows = db.db_select_row(1122, statement)

    # Return
    for row in rows:
        result.append(_rows.event(row))
    return result


def delete(idx):
    """Delete event.

    Args:
        idx: idx_event

    Returns:
        None

    """
    # Verify existence
    result = idx_exists(idx)
    if bool(result) is False:
        return

    # Don't delete the very first record.
    # This must always exist for polling to work correctly
    if idx != 1:
        # Delete data
        statement = _delete(Event).where(Event.idx_event == idx)
        db.db_delete(1055, statement)

        # Delete root
        statement = _delete(Root).where(Root.idx_event == idx)
        db.db_delete(1053, statement)


def create():
    """Create an event.

    Args:
        None

    Returns:
        result: Event object for row that doesn't already exist

    """
    # Get configuration
    while True:
        name = general.random_hash()
        _exists = exists(name)
        if bool(_exists) is False:
            break

    # Get REvent object
    row = IEvent(name=name, enabled=1)
    insert_row(row)
    result = exists(name)

    # Create a root entry
    root.insert_row(
        IRoot(idx_event=result.idx_event, name=result.name, enabled=True)
    )
    return result


def purge():
    """Purge all events except the first and last.

    Args:
        None

    Returns:
        result: None

    """
    # Get all the event data
    _events = events()

    # Get the first and last event
    indexes = [_.idx_event for _ in _events]
    first = min(indexes)
    last = max(indexes)

    for item in _events:
        if (item.idx_event != first) and (item.idx_event != last):
            delete(item.idx_event)
