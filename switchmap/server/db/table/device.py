"""Module for querying the Device table."""

from sqlalchemy import select, update, null, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Device as _Device
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_device

    Returns:
        result: RDevice object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(_Device).where(_Device.idx_device == idx)
    rows = db.db_select_row(1208, statement)

    # Return
    for row in rows:
        result = _rows.device(row)
        break
    return result


def exists(idx_zone, hostname):
    """Determine whether hostname exists in the Device table.

    Args:
        idx_zone: Zone index
        hostname: Device

    Returns:
        result: RDevice tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get hostname from database
    statement = select(_Device).where(
        and_(
            _Device.hostname == hostname.encode(), _Device.idx_zone == idx_zone
        )
    )
    rows = db.db_select_row(1107, statement)

    # Return
    for row in rows:
        result = _rows.device(row)
        break
    return result


def devices(idx_zone):
    """Get all Devices for a zone.

    Args:
        idx_zone: Zone index

    Returns:
        result: list of RDevice tuples

    """
    # Initialize key variables
    result = []
    rows = []

    # Get device from database
    statement = select(_Device).where(_Device.idx_zone == idx_zone)
    rows = db.db_select_row(1027, statement)

    # Return
    for row in rows:
        result.append(_rows.device(row))
    return result


def insert_row(rows):
    """Create a Device table entry.

    Args:
        rows: IDevice objects

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
                "idx_zone": row.idx_zone,
                "sys_name": (
                    None if row.sys_name is None else row.sys_name.encode()
                ),
                "hostname": (
                    None if row.hostname is None else row.hostname.encode()
                ),
                "name": (None if row.name is None else row.name.encode()),
                "sys_description": (
                    None
                    if row.sys_description is None
                    else row.sys_description.encode()
                ),
                "sys_objectid": (
                    None
                    if row.sys_objectid is None
                    else row.sys_objectid.encode()
                ),
                "sys_uptime": (
                    None if row.sys_uptime is None else row.sys_uptime
                ),
                "last_polled": (
                    None if row.last_polled is None else row.last_polled
                ),
                "enabled":int(bool(row.enabled) is True),
            }
        )

    # Insert
    if bool(inserts):
        db.db_insert_row(1156, _Device, inserts)


def update_row(idx, row):
    """Upadate a Device table entry.

    Args:
        idx: idx_device value
        row: IDevice object

    Returns:
        None

    """
    # Update
    statement = (
        update(_Device)
        .where(_Device.idx_device == idx)
        .values(
            {
                "idx_zone": row.idx_zone,
                "sys_name": (
                    None
                    if bool(row.sys_name) is False
                    else row.sys_name.encode()
                ),
                "hostname": (
                    None
                    if bool(row.hostname) is False
                    else row.hostname.encode()
                ),
                "name": (
                    None if bool(row.name) is False else row.name.encode()
                ),
                "sys_description": (
                    None
                    if bool(row.sys_description) is False
                    else row.sys_description.encode()
                ),
                "sys_objectid": (
                    None
                    if bool(row.sys_objectid) is False
                    else row.sys_objectid.encode()
                ),
                "sys_uptime": (
                    None if bool(row.sys_uptime) is False else row.sys_uptime
                ),
                "last_polled": (
                    None if bool(row.last_polled) is False else row.last_polled
                ),
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1110, statement)
