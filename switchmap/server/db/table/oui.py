"""Module for querying the Oui table."""

from sqlalchemy import select, update, null

# Import project libraries
from switchmap.server.db.import db
from switchmap.server.db.models import Oui
from switchmap.server.db.misc import rows as _rows


def idx_oui(mac):
    """Get the idx_oui value.

    Args:
        row: MAC address

    Returns:
        result: idx_oui value

    """
    # Initialize key variables
    result = 1

    # Find the true idx_oui
    if bool(mac) is True:
        statement = select(Oui.idx_oui).where(Oui.oui == mac[:6].encode())
        items = db.db_select(1177, statement)
        for item in items:
            result = item.idx_oui
            break
    return result


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_oui

    Returns:
        result: ROui record

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Oui).where(Oui.idx_oui == idx)
    rows = db.db_select_row(1102, statement)

    # Return
    for row in rows:
        result = _rows.oui(row)
        break
    return result


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
        result = _rows.oui(row)
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
                oui=(null() if bool(row.oui) is False else row.oui.encode()),
                organization=(
                    null()
                    if bool(row.organization) is False
                    else row.organization.encode()
                ),
                enabled=row.enabled,
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
    statement = (
        update(Oui)
        .where(Oui.idx_oui == idx)
        .values(
            {
                "organization": (
                    null()
                    if bool(row.organization) is False
                    else row.organization.encode()
                ),
                "oui": (
                    null() if bool(row.oui) is False else row.oui.encode()
                ),
                "enabled": row.enabled,
            }
        )
    )
    db.db_update(1118, statement)
