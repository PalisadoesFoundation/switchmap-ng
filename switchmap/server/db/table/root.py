"""Module for querying the Root table."""


from sqlalchemy import select, update

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Root
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_root

    Returns:
        result: RRoot record

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Root).where(Root.idx_root == idx)
    rows = db.db_select_row(1034, statement)

    # Return
    for row in rows:
        result = _rows.root(row)
        break
    return result


def exists(root):
    """Determine whether root exists in the Root table.

    Args:
        root: Root

    Returns:
        result: RRoot tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get root from database
    statement = select(Root).where(Root.name == root.encode())
    rows = db.db_select_row(1035, statement)

    # Return
    for row in rows:
        result = _rows.root(row)
        break
    return result


def insert_row(rows):
    """Create a Root table entry.

    Args:
        rows: IRoot objects

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
            Root(
                idx_event=row.idx_event,
                name=row.name.encode(),
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1033, inserts)


def update_row(idx, row):
    """Upadate a Root table entry.

    Args:
        idx: idx_root value
        row: IRoot object

    Returns:
        None

    """
    # Update
    statement = (
        update(Root)
        .where(Root.idx_root == idx)
        .values(
            {
                "idx_event": row.idx_event,
                "name": row.name.encode(),
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1030, statement)


def roots():
    """Get list of Roots.

    Args:
        idx: idx_root

    Returns:
        result: RRoot object

    """
    # Initialize key variables
    result = []
    rows = []

    # Get data
    statement = select(Root)
    rows = db.db_select_row(1031, statement)

    # Return
    for row in rows:
        result.append(_rows.root(row))
    return result
