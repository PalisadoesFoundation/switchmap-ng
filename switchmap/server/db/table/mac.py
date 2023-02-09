"""Module for querying the Mac table."""

from sqlalchemy import select, update, null

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Mac
from switchmap.server.db.misc import rows as _rows
from switchmap.server.db.table import oui
from switchmap.core import general


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_mac

    Returns:
        result: RMac object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Mac).where(Mac.idx_mac == idx)
    rows = db.db_select_row(1097, statement)

    # Return
    for row in rows:
        result = _rows.mac(row)
        break
    return result


def exists(_mac):
    """Determine whether MAC exists in the Mac table.

    Args:
        _mac: Mac address

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Fix the MAC address
    mac = general.mac(_mac)

    # Get row from dataase
    statement = select(Mac).where(Mac.mac == mac.encode())
    rows = db.db_select_row(1178, statement)

    # Return
    for row in rows:
        result = _rows.mac(row)
        break
    return result


def findmac(macs):
    """Determine whether MAC exists in the Mac table.

    Args:
        _mac: Mac address

    Returns:
        result: list of RMac tuples

    """
    # Initialize key variables
    result = []
    rows = []
    all_macs = []

    if isinstance(macs, str):
        macs = [macs]

    if isinstance(macs, list):
        # Fix the MAC address
        for item in macs:
            all_macs.append(general.mac(item).encode())

        # Get row from dataase
        statement = select(Mac).where(Mac.mac.in_(all_macs))
        rows = db.db_select_row(1193, statement)

    # Return
    for row in rows:
        result.append(_rows.mac(row))
    return result


def insert_row(rows):
    """Create a Mac table entry.

    Args:
        rows: TopologyMac objects

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
        # Fix the MAC address
        mac = general.mac(row.mac)

        # Find the true idx_oui
        idx_oui = oui.idx_oui(mac)

        # Do the insertion
        inserts.append(
            Mac(
                idx_oui=idx_oui,
                idx_event=row.idx_event,
                idx_zone=row.idx_zone,
                mac=(null() if bool(mac) is False else mac.encode()),
                enabled=row.enabled,
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1087, inserts)


def update_row(idx, row):
    """Upadate a Mac table entry.

    Args:
        idx: idx_mac value
        row: IMac object

    Returns:
        None

    """
    # Fix the MAC address
    mac = general.mac(row.mac)

    # Find the true idx_oui
    idx_oui = oui.idx_oui(mac)

    # Update
    statement = (
        update(Mac)
        .where(Mac.idx_mac == idx)
        .values(
            {
                "idx_oui": idx_oui,
                "idx_event": row.idx_event,
                "idx_zone": row.idx_zone,
                "mac": (null() if bool(mac) is False else mac.encode()),
                "enabled": row.enabled,
            }
        )
    )
    db.db_update(1114, statement)
