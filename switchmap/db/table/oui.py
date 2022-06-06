"""Module for querying the OUI table."""

from sqlalchemy import select, update

# Import project libraries
from switchmap.db import db
from switchmap.db.models import OUI
from switchmap.db.table import ROUI


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
    statement = select(OUI.idx_oui).where(OUI.idx_oui == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def exists(oui):
    """Determine whether oui exists in the OUI table.

    Args:
        oui: OUI

    Returns:
        result: ROUI tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get oui from database
    statement = select(OUI).where(OUI.oui == oui.encode())
    rows = db.db_select_row(1226, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a OUI table entry.

    Args:
        rows: IOUI objects

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
            OUI(
                oui=row.oui.encode(),
                organization=row.organization.encode(),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a OUI table entry.

    Args:
        idx: idx_oui value
        row: IOUI object

    Returns:
        None

    """
    # Update
    statement = update(OUI).where(
        OUI.idx_oui == idx).values(
            {
                'organization': row.organization.encode(),
                'oui': row.oui.encode(),
                'enabled': row.enabled,
            }
        )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: OUI row

    Returns:
        result: ROUI tuple

    """
    # Initialize key variables
    result = ROUI(
        idx_oui=row.idx_oui,
        oui=row.oui.decode(),
        organization=row.organization.decode(),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
