"""Module for querying the Device table."""

from sqlalchemy import select, update, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Device
from switchmap.db.table import RDevice


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_device

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select().where(Device.idx_device == idx)
    rows = db.db_select_row(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


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
    statement = select(Device).where(Device.hostname == hostname.encode())
    rows = db.db_select_row(1226, statement)

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
            Device(
                idx_location=row.idx_location,
                idx_event=row.idx_event,
                sys_name=(
                    null() if row.sys_name is None else row.sys_name.encode()),
                hostname=(
                    null() if row.hostname is None else row.hostname.encode()),
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
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a Device table entry.

    Args:
        idx: idx_device value
        row: IDevice object

    Returns:
        None

    """
    # Update
    statement = update(Device).where(
        Device.idx_device == idx).values(
            {
                'idx_location': row.idx_location,
                'idx_event': row.idx_event,
                'sys_name': (
                    null() if bool(row.sys_name) is False else
                    row.sys_name.encode()),
                'hostname': (
                    null() if bool(row.hostname) is False else
                    row.hostname.encode()),
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
    db.db_update(1126, statement)


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
        idx_location=row.idx_location,
        idx_event=row.idx_event,
        sys_name=(
            None if bool(row.sys_name) is False else row.sys_name.decode()),
        hostname=(
            None if bool(row.hostname) is False else row.hostname.decode()),
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