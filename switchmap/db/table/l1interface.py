"""Module for querying the L1Interface table."""

from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.db import db
from switchmap.db.models import L1Interface
from switchmap.db.table import RL1Interface


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_l1interface

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(
        L1Interface.idx_l1interface).where(L1Interface.idx_l1interface == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def exists(idx_device, ifindex):
    """Determine whether hostname exists in the L1Interface table.

    Args:
        idx_device: Device.idx_device
        ifindex: SNMP IfIndex number

    Returns:
        result: RL1Interface tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(L1Interface).where(
        and_(
            L1Interface.ifindex == ifindex,
            L1Interface.idx_device == idx_device
        )
    )
    rows = db.db_select_row(1226, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a L1Interface table entry.

    Args:
        rows: IL1Interface objects

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
            L1Interface(
                idx_device=row.idx_device,
                ifindex=row.ifindex,
                duplex=row.duplex,
                ethernet=row.ethernet,
                nativevlan=row.nativevlan,
                trunk=row.trunk,
                ifspeed=row.ifspeed,
                ifalias=row.ifalias.encode(),
                ifdescr=row.ifdescr.encode(),
                ifadminstatus=row.ifadminstatus,
                ifoperstatus=row.ifoperstatus,
                ts_idle=row.ts_idle,
                cdpcachedeviceid=row.cdpcachedeviceid.encode(),
                cdpcachedeviceport=row.cdpcachedeviceport.encode(),
                cdpcacheplatform=row.cdpcacheplatform.encode(),
                lldpremportdesc=row.lldpremportdesc.encode(),
                lldpremsyscapenabled=row.lldpremsyscapenabled.encode(),
                lldpremsysdesc=row.lldpremsysdesc.encode(),
                lldpremsysname=row.lldpremsysname.encode(),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a L1Interface table entry.

    Args:
        idx: idx_l1interface value
        row: IL1Interface object

    Returns:
        None

    """
    # Update
    statement = update(L1Interface).where(
        L1Interface.idx_l1interface == idx).values(
            {
                'idx_device': row.idx_device,
                'ifindex': row.ifindex,
                'duplex': row.duplex,
                'ethernet': row.ethernet,
                'nativevlan': row.nativevlan,
                'trunk': row.trunk,
                'ifspeed': row.ifspeed,
                'ifalias': row.ifalias.encode(),
                'ifdescr': row.ifdescr.encode(),
                'ifadminstatus': row.ifadminstatus,
                'ifoperstatus': row.ifoperstatus,
                'ts_idle': row.ts_idle,
                'cdpcachedeviceid': row.cdpcachedeviceid.encode(),
                'cdpcachedeviceport': row.cdpcachedeviceport.encode(),
                'cdpcacheplatform': row.cdpcacheplatform.encode(),
                'lldpremportdesc': row.lldpremportdesc.encode(),
                'lldpremsyscapenabled': row.lldpremsyscapenabled.encode(),
                'lldpremsysdesc': row.lldpremsysdesc.encode(),
                'lldpremsysname': row.lldpremsysname.encode(),
                'enabled': row.enabled
            }
        )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: L1Interface row

    Returns:
        result: RL1Interface tuple

    """
    # Initialize key variables
    result = RL1Interface(
        idx_l1interface=row.idx_l1interface,
        idx_device=row.idx_device,
        ifindex=row.ifindex,
        duplex=row.duplex,
        ethernet=row.ethernet,
        nativevlan=row.nativevlan,
        trunk=row.trunk,
        ifspeed=row.ifspeed,
        ifalias=row.ifalias.decode(),
        ifdescr=row.ifdescr.decode(),
        ifadminstatus=row.ifadminstatus,
        ifoperstatus=row.ifoperstatus,
        ts_idle=row.ts_idle,
        cdpcachedeviceid=row.cdpcachedeviceid.decode(),
        cdpcachedeviceport=row.cdpcachedeviceport.decode(),
        cdpcacheplatform=row.cdpcacheplatform.decode(),
        lldpremportdesc=row.lldpremportdesc.decode(),
        lldpremsyscapenabled=row.lldpremsyscapenabled.decode(),
        lldpremsysdesc=row.lldpremsysdesc.decode(),
        lldpremsysname=row.lldpremsysname.decode(),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
