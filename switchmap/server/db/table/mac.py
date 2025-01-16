"""Module for querying the Mac table."""

from sqlalchemy import select, update, null, and_

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


def exists(idx_zone, _mac):
    """Determine whether MAC exists in the Mac table.

    Args:
        idx_zone: Zone index
        _mac: Mac address

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Fix the MAC address
    mactest = general.mac(_mac)
    if bool(mactest.valid) is False:
        return result
    else:
        mac = mactest.mac

    # Get row from dataase
    statement = select(Mac).where(
        and_(Mac.mac == mac.encode(), Mac.idx_zone == idx_zone)
    )
    rows = db.db_select_row(1178, statement)

    # Return
    for row in rows:
        result = _rows.mac(row)
        break
    return result


def findmac(idx_zone, macs):
    """Determine whether MAC exists in the Mac table.

    Args:
        idx_zone: Zone index
        macs: List or single MAC address

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
        for item in macs:
            # Append if the MAC is valid
            mactest = general.mac(item)
            if bool(mactest.valid) is False:
                continue
            else:
                _mac_ = mactest.mac
            all_macs.append(_mac_.encode())

        # Get row from dataase
        statement = select(Mac).where(
            and_(Mac.mac.in_(all_macs), Mac.idx_zone == idx_zone)
        )
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

    # Remove any duplicates
    rows = list(set(rows))

    # Create objects
    for row in rows:
        # Fix the MAC address
        mactest = general.mac(row.mac)

        # Check the validity
        if bool(mactest.valid) is False:
            continue
        else:
            mac = mactest.mac

        # Find the true idx_oui
        idx_oui = oui.idx_oui(mac)

        # Do the insertion
        inserts.append(
            Mac(
                idx_oui=idx_oui,
                idx_zone=row.idx_zone,
                mac=(null() if bool(mac) is False else mac.encode()),
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1087, inserts)


def bulk_insert_rows(model, rows):
    """Perform bulk insert for the Mac table.

    Args:
        rows: List of IMac objects

    Returns:
        None
    """
    # Initialize key variables
    inserts = []

    # Ensure rows is a list
    if isinstance(rows, list) is False:
        rows = [rows]

    # Remove duplicates
    rows = list(set(rows))

    # Create ORM objects
    for row in rows:
        # Fix the MAC address
        mactest = general.mac(row.mac)

        # Check validity
        if not mactest.valid:
            continue
        else:
            mac = mactest.mac

        # Find the true idx_oui
        idx_oui = oui.idx_oui(mac)

        # Add ORM object for insertion
        inserts.append(
            {
                "idx_oui": idx_oui,
                "idx_zone": row.idx_zone,
                "mac": bytes(mac, "utf-8"),
                "enabled": int(bool(row.enabled)),
            }
        )

    # Perform bulk insert
    if bool(inserts):
        db.db_bulk_insert(1202, model, inserts)


def update_row(idx, row):
    """Upadate a Mac table entry.

    Args:
        idx: idx_mac value
        row: IMac object

    Returns:
        None

    """
    # Fix the MAC address
    mactest = general.mac(row.mac)
    mac = mactest.mac

    # Find the true idx_oui
    idx_oui = oui.idx_oui(mac)

    # Update
    statement = (
        update(Mac)
        .where(Mac.idx_mac == idx)
        .values(
            {
                "idx_oui": idx_oui,
                "idx_zone": row.idx_zone,
                "mac": (null() if bool(mac) is False else mac.encode()),
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1114, statement)
