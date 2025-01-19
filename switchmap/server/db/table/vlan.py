"""Module for querying the Vlan table."""

from sqlalchemy import select, update, null, and_

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import Vlan
from switchmap.server.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_vlan

    Returns:
        result: RVlan object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Vlan).where(Vlan.idx_vlan == idx)
    rows = db.db_select_row(1210, statement)

    # Return
    for row in rows:
        result = _rows.vlan(row)
        break
    return result


def exists(idx_device, vlan):
    """Determine whether vlan exists in the Vlan table.

    Args:
        idx_device: DB idx for the device
        vlan: Vlan

    Returns:
        result: RVlan tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get vlan from database
    statement = select(Vlan).where(
        and_(Vlan.vlan == vlan, Vlan.idx_device == idx_device)
    )
    rows = db.db_select_row(1022, statement)

    # Return
    for row in rows:
        result = _rows.vlan(row)
        break
    return result


def vlans(idx_device):
    """Get all VLANs for a device.

    Args:
        idx_device: Device index

    Returns:
        result: list of RVlan tuples

    """
    # Initialize key variables
    result = []
    rows = []

    # Get vlan from database
    statement = select(Vlan).where(Vlan.idx_device == idx_device)
    rows = db.db_select_row(1019, statement)

    # Return
    for row in rows:
        result.append(_rows.vlan(row))
    return result


def insert_row(rows):
    """Create a Vlan table entry.

    Args:
        rows: IVlan objects

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
                "idx_device": row.idx_device,
                "vlan": None if row.vlan is None else row.vlan,
                "name": None if bool(row.name) is False else row.name.encode(),
                "state": None if bool(row.state) is False else row.state,
                "enabled": int(bool(row.enabled) is True),
            }
        )

    # Insert
    if bool(inserts):
        db.db_insert_row(1093, Vlan, inserts)


def update_row(idx, row):
    """Upadate a Vlan table entry.

    Args:
        idx: idx_vlan value
        row: IVlan object

    Returns:
        None

    """
    # Update
    statement = (
        update(Vlan)
        .where(Vlan.idx_vlan == idx)
        .values(
            {
                "idx_device": row.idx_device,
                "vlan": None if bool(row.vlan) is False else row.vlan,
                "name": (
                    None if bool(row.name) is False else row.name.encode()
                ),
                "state": None if bool(row.state) is False else row.state,
                "enabled": int(bool(row.enabled) is True),
            }
        )
    )
    db.db_update(1120, statement)
