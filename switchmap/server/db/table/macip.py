"""Module for querying the MacIp table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import MacIp
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_macip

    Returns:
        result: RMacIp object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(MacIp).where(MacIp.idx_macip == idx)
    rows = db.db_select_row(1098, statement)

    # Return
    for row in rows:
        result = _rows.macip(row)
        break
    return result


def exists(idx_mac, idx_ip):
    """Determine whether mac exists in the MacIp table.

    Args:
        idx_mac: Mac.idx_mac
        idx_ip: Ip.idx_ip

    Returns:
        result: RMacIp tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(MacIp).where(
        and_(
            MacIp.idx_mac == idx_mac,
            MacIp.idx_ip == idx_ip,
        )
    )
    rows = db.db_select_row(1201, statement)

    # Return
    for row in rows:
        result = _rows.macip(row)
        break
    return result


def insert_row(rows):
    """Create a MacIp table entry.

    Args:
        rows: IMacIp objects

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
        inserts.append(
            {
                "idx_ip": row.idx_ip,
                "idx_mac": row.idx_mac,
                "enabled": int(bool(row.enabled) is True),
            }
        )

    # Insert
    if bool(inserts):
        db.db_insert_row(1091, MacIp, inserts)


def update_row(idx, row):
    """Upadate a MacIp table entry.

    Args:
        idx: idx_macip value
        row: IMacIp object

    Returns:
        None

    """
    # Update
    statement = (
        update(MacIp)
        .where(MacIp.idx_macip == idx)
        .values(
            {
                "idx_ip": row.idx_ip,
                "idx_mac": row.idx_mac,
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1115, statement)


def idx_ips_exist(idx_mac):
    """Get a list of idx_ip values matching idx_mac from the MacIp table.

    Args:
        idx_mac: Mac.idx_mac

    Returns:
        result: List of RMacIp tuples

    """
    # Initialize key variables
    result = []

    # Get row from dataase
    statement = select(MacIp).where(
        MacIp.idx_mac == idx_mac,
    )
    rows = db.db_select_row(1087, statement)

    # Return
    for row in rows:
        result.append(_rows.macip(row))

    return result
