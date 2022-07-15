"""Module for querying the Device table."""

from sqlalchemy import select, update, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Device as _Device
from switchmap.db.table import RDevice


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
        result = _row(row)
        break
    return result


def exists(hostname):
    """Determine whether hostname exists in the Device table.

    Args:
        hostname: Device

    Returns:
        result: RDevice tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get hostname from database
    statement = select(_Device).where(_Device.hostname == hostname.encode())
    rows = db.db_select_row(1107, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
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

    # Create objects
    for row in rows:
        inserts.append(
            _Device(
                idx_zone=row.idx_zone,
                idx_event=row.idx_event,
                sys_name=(
                    null() if row.sys_name is None else row.sys_name.encode()),
                hostname=(
                    null() if row.hostname is None else row.hostname.encode()),
                name=(
                    null() if row.name is None else row.name.encode()),
                sys_description=(
                    null() if row.sys_description is None else
                    row.sys_description.encode()),
                sys_objectid=(
                    null() if row.sys_objectid is None else
                    row.sys_objectid.encode()),
                sys_uptime=(
                    null() if row.sys_uptime is None else row.sys_uptime),
                last_polled=(
                    0 if row.last_polled is None else row.last_polled),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1156, inserts)


def update_row(idx, row):
    """Upadate a Device table entry.

    Args:
        idx: idx_device value
        row: IDevice object

    Returns:
        None

    """
    # Update
    statement = update(_Device).where(
        _Device.idx_device == idx).values(
            {
                'idx_zone': row.idx_zone,
                'idx_event': row.idx_event,
                'sys_name': (
                    null() if bool(row.sys_name) is False else
                    row.sys_name.encode()),
                'hostname': (
                    null() if bool(row.hostname) is False else
                    row.hostname.encode()),
                'name': (
                    null() if bool(row.name) is False else
                    row.name.encode()),
                'sys_description': (
                    null() if bool(row.sys_description) is False else
                    row.sys_description.encode()),
                'sys_objectid': (
                    null() if bool(row.sys_objectid) is False else
                    row.sys_objectid.encode()),
                'sys_uptime': (
                    null() if bool(row.sys_uptime) is False else
                    row.sys_uptime),
                'last_polled': (
                    0 if bool(row.last_polled) is False else
                    row.last_polled),
                'enabled': row.enabled
            }
        )
    db.db_update(1110, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Device row

    Returns:
        result: RDevice tuple

    """
    # Initialize key variables
    result = RDevice(
        idx_device=row.idx_device,
        idx_zone=row.idx_zone,
        idx_event=row.idx_event,
        sys_name=(
            None if bool(row.sys_name) is False else row.sys_name.decode()),
        hostname=(
            None if bool(row.hostname) is False else row.hostname.decode()),
        name=(
            None if bool(row.name) is False else row.name.decode()),
        sys_description=(
            None if bool(row.sys_description) is False else
            row.sys_description.decode()),
        sys_objectid=(
            None if bool(row.sys_objectid) is False else
            row.sys_objectid.decode()),
        sys_uptime=row.sys_uptime,
        last_polled=row.last_polled,
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
