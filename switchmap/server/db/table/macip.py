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


# def findip(idx_ip, ipaddress):
#     """Find IP address.

#     Args:
#         idx_ip: Device index
#         ipaddress: IP address

#     Returns:
#         result: RMacIp tuple

#     """
#     # Initialize key variables
#     result = []
#     rows = []

#     # Get row from dataase
#     statement = select(MacIp).where(
#         and_(MacIp.ip_ == ipaddress.encode(), MacIp.idx_ip == idx_ip)
#     )
#     rows = db.db_select_row(1186, statement)

#     # Return
#     for row in rows:
#         result.append(_rows.macip(row))
#     return result


# def findhostname(idx_ip, hostname):
#     """Find hostname.

#     Args:
#         idx_ip: Device index
#         hostname: Hostname

#     Returns:
#         result: MacIp tuple

#     """
#     # Initialize key variables
#     result = []
#     rows = []

#     # Get row from database (Contains)
#     statement = select(MacIp).where(
#         and_(
#             MacIp.hostname.like(
#                 func.concat(func.concat("%", hostname.encode(), "%"))
#             ),
#             MacIp.idx_ip == idx_ip,
#         )
#     )

#     rows_contains = db.db_select_row(1191, statement)

#     # Merge results and remove duplicates
#     if bool(rows_contains) is True:
#         rows.extend(rows_contains)

#     # Return
#     for row in rows:
#         result.append(_rows.macip(row))

#     # Remove duplicates and return
#     result = list(set(result))
#     return result


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
            MacIp(
                idx_ip=row.idx_ip,
                idx_mac=row.idx_mac,
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1091, inserts)


def bulk_insert_rows(model, rows):
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
            MacIp(
                idx_ip=row.idx_ip,
                idx_mac=row.idx_mac,
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_bulk_insert(1091,model, inserts)


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
