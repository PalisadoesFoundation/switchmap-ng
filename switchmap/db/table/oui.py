"""Module for querying the Oui table."""

from sqlalchemy import select, update

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Oui
from switchmap.db.table import ROui


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_oui

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Oui.idx_oui).where(Oui.idx_oui == idx)
    rows = db.db_select(1102, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def exists(oui):
    """Determine whether oui exists in the Oui table.

    Args:
        oui: Oui

    Returns:
        result: ROui tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get oui from database
    statement = select(Oui).where(Oui.oui == oui.encode())
    rows = db.db_select_row(1106, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a Oui table entry.

    Args:
        rows: IOui objects

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
            Oui(
                oui=row.oui.encode(),
                organization=row.organization.encode(),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1096, inserts)


def update_row(idx, row):
    """Upadate a Oui table entry.

    Args:
        idx: idx_oui value
        row: IOui object

    Returns:
        None

    """
    # Update
    statement = update(Oui).where(
        Oui.idx_oui == idx).values(
            {
                'organization': row.organization.encode(),
                'oui': row.oui.encode(),
                'enabled': row.enabled,
            }
        )
    db.db_update(1118, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Oui row

    Returns:
        result: ROui tuple

    """
    # Initialize key variables
    result = ROui(
        idx_oui=row.idx_oui,
        oui=row.oui.decode(),
        organization=row.organization.decode(),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
