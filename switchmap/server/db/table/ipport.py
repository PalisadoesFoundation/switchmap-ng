"""Module for querying the IpPort table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import IpPort
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_ipport

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(IpPort).where(IpPort.idx_ipport == idx)
    rows = db.db_select_row(1060, statement)

    # Return
    for row in rows:
        result = _rows.ipport(row)
        break
    return result


def exists(idx_l1interface, idx_ip):
    """Determine whether entry exists in the IpPort table.

    Args:
        idx_l1interface: Device.idx_l1interface
        idx_ip: Ip.idx_ip

    Returns:
        result: RIpPort tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(IpPort).where(
        and_(
            IpPort.idx_ip == idx_ip,
            IpPort.idx_l1interface == idx_l1interface,
        )
    )
    rows = db.db_select_row(1061, statement)

    # Return
    for row in rows:
        result = _rows.ipport(row)
        break
    return result


def find_idx_ip(idx_ip):
    """Find all ports on which MAC address has been found.

    Args:
        idx_ip: Ip.idx_ip

    Returns:
        result: RIpPort tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from dataase
    statement = select(IpPort).where(IpPort.idx_ip == idx_ip)
    rows = db.db_select_row(1072, statement)

    # Return
    for row in rows:
        result.append(_rows.ipport(row))
    return result


def insert_row(rows):
    """Create a IpPort table entry.

    Args:
        rows: IIpPort objects

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
            IpPort(
                idx_l1interface=row.idx_l1interface,
                idx_ip=row.idx_ip,
                enabled=int(bool(row.enabled) is True),
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1063, inserts)


def update_row(idx, row):
    """Upadate a IpPort table entry.

    Args:
        idx: idx_ipport value
        row: IIpPort object

    Returns:
        None

    """
    # Update
    statement = (
        update(IpPort)
        .where(IpPort.idx_ipport == idx)
        .values(
            {
                "idx_l1interface": row.idx_l1interface,
                "idx_ip": row.idx_ip,
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1070, statement)
