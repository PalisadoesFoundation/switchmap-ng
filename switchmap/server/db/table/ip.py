"""Module for querying the Ip table."""

from sqlalchemy import select, update, null, and_, func

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Ip
from switchmap.server.db.misc import rows as _rows
from switchmap.core import general


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_ip

    Returns:
        result: RIp object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Ip).where(Ip.idx_ip == idx)
    rows = db.db_select_row(1064, statement)

    # Return
    for row in rows:
        result = _rows.ip(row)
        break
    return result


def exists(idx_zone, _ip):
    """Determine whether MAC exists in the Ip table.

    Args:
        idx_zone: Zone index
        _ip: Ip address

    Returns:
        result: RIp tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Fix the MAC address
    ip = general.ipaddress(_ip)

    # Get row from dataase
    statement = select(Ip).where(
        and_(Ip.address == ip.address.encode(), Ip.idx_zone == idx_zone)
    )
    rows = db.db_select_row(1073, statement)

    # Return
    for row in rows:
        result = _rows.ip(row)
        break
    return result


def findhostname(idx_zone, hostname):
    """Determine whether hostname exists in the Ip table.

    Args:
        idx_zone: Zone index
        hostname: hostname

    Returns:
        results: RIp list

    """
    # Initialize key variables
    results = []
    rows = []

    # Get row from dataase
    statement = select(Ip).where(
        and_(
            Ip.hostname.like(
                func.concat(func.concat("%", hostname.encode(), "%"))
            ),
            Ip.idx_zone == idx_zone,
        )
    )
    rows = db.db_select_row(1066, statement)

    # Return
    for row in rows:
        results.append(_rows.ip(row))
    return results


def findip(idx_zone, ips):
    """Determine whether MAC exists in the Ip table.

    Args:
        idx_zone: Zone index
        ips: one or more IP addresses

    Returns:
        result: list of RIp tuples

    """
    # Initialize key variables
    result = []
    rows = []
    all_ips = []

    if isinstance(ips, str):
        ips = [ips]

    if isinstance(ips, list):
        # Fix the MAC address
        for item in ips:
            ip_ = general.ipaddress(item)
            if bool(ip_):
                all_ips.append(general.ipaddress(item).address.encode())

        # Get row from dataase
        if bool(all_ips):
            statement = select(Ip).where(
                and_(Ip.address.in_(all_ips), Ip.idx_zone == idx_zone)
            )
            rows = db.db_select_row(1068, statement)

    # Return
    for row in rows:
        result.append(_rows.ip(row))
    return result

def insert_row(rows):
    """Perform bulk insert for the Mac table.

    Args:
        model: SQLAlchemy model representing the target database table.
        rows: List of IMac objects to be inserted into the database.

    Returns:
        None: This function does not return any value.
    """
    # Initialize key variables
    inserts = []

    # Ensure input is a list
    if isinstance(rows, list) is False:
        rows = [rows]

    # Remove duplicates
    rows = list(set(rows))

    # Create objects for insertion
    for row in rows:
        ip = general.ipaddress(row.address)
        inserts.append(
                {
                    "idx_zone": row.idx_zone,
                    "hostname": None
                    if bool(row.hostname) is False
                    else row.hostname.encode(),
                    "version": row.version,
                    "address": (None if bool(ip) is False else ip.address.encode()),
                    "enabled":int(bool(row.enabled)),
                }
            )

    # Perform bulk insert
    if inserts:
        db.db_insert_row(1070, Ip, inserts)

def update_row(idx, row):
    """Upadate a Ip table entry.

    Args:
        idx: idx_ip value
        row: IIp object

    Returns:
        None

    """
    # Fix the MAC address
    ip = general.ipaddress(row.address)

    # Update
    statement = (
        update(Ip)
        .where(Ip.idx_ip == idx)
        .values(
            {
                "idx_zone": row.idx_zone,
                "address": (
                    None if bool(ip) is False else ip.address.encode()
                ),
                "version": row.version,
                "hostname": (
                    None
                    if bool(row.hostname) is False
                    else row.hostname.lower().encode()
                ),
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1069, statement)
