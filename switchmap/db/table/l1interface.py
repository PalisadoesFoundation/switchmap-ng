"""Module for querying the L1Interface table."""

from sqlalchemy import select, update, and_, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import L1Interface
from switchmap.db.table import RL1Interface


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_l1interface

    Returns:
        result: RL1Interface object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(L1Interface).where(L1Interface.idx_l1interface == idx)
    rows = db.db_select_row(1206, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


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
    rows = db.db_select_row(1205, statement)

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
                duplex=null() if row.duplex is None else row.duplex,
                ethernet=null() if row.ethernet is None else row.ethernet,
                nativevlan=(
                    null() if row.nativevlan is None else row.nativevlan),
                trunk=null() if row.trunk is None else row.trunk,
                ifspeed=null() if row.ifspeed is None else row.ifspeed,
                ifalias=(
                    null() if row.ifalias is None else row.ifalias.encode()),
                ifdescr=(
                    null() if row.ifdescr is None else row.ifdescr.encode()),
                ifadminstatus=(
                    null() if row.ifadminstatus is None
                    else row.ifadminstatus),
                ifoperstatus=(
                    null() if row.ifoperstatus is None else row.ifoperstatus),
                ts_idle=0 if not bool(row.ts_idle) else row.ts_idle,
                cdpcachedeviceid=(
                    null() if row.cdpcachedeviceid is None else
                    row.cdpcachedeviceid.encode()),
                cdpcachedeviceport=(
                    null() if row.cdpcachedeviceport is None else
                    row.cdpcachedeviceport.encode()),
                cdpcacheplatform=(
                    null() if row.cdpcacheplatform is None else
                    row.cdpcacheplatform.encode()),
                lldpremportdesc=(
                    null() if row.lldpremportdesc is None else
                    row.lldpremportdesc.encode()),
                lldpremsyscapenabled=(
                    null() if row.lldpremsyscapenabled is None else
                    row.lldpremsyscapenabled.encode()),
                lldpremsysdesc=(
                    null() if row.lldpremsysdesc is None else
                    row.lldpremsysdesc.encode()),
                lldpremsysname=(
                    null() if row.lldpremsysname is None else
                    row.lldpremsysname.encode()),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1154, inserts)


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
                'duplex': null() if row.duplex is None else row.duplex,
                'ethernet': null() if row.ethernet is None else row.ethernet,
                'nativevlan': (
                    null() if row.nativevlan is None else row.nativevlan),
                'trunk': null() if row.trunk is None else row.trunk,
                'ifspeed': null() if row.ifspeed is None else row.ifspeed,
                'ifalias': (
                    null() if row.ifalias is None else row.ifalias.encode()),
                'ifdescr': (
                    null() if row.ifdescr is None else row.ifdescr.encode()),
                'ifadminstatus': (
                    null() if row.ifadminstatus is None else
                    row.ifadminstatus),
                'ifoperstatus': (
                    null() if row.ifoperstatus is None else row.ifoperstatus),
                'ts_idle': 0 if not bool(row.ts_idle) else row.ts_idle,
                'cdpcachedeviceid': (
                    null() if row.cdpcachedeviceid is None else
                    row.cdpcachedeviceid.encode()),
                'cdpcachedeviceport': (
                    null() if row.cdpcachedeviceport is None else
                    row.cdpcachedeviceport.encode()),
                'cdpcacheplatform': (
                    null() if row.cdpcacheplatform is None else
                    row.cdpcacheplatform.encode()),
                'lldpremportdesc': (
                    null() if row.lldpremportdesc is None else
                    row.lldpremportdesc.encode()),
                'lldpremsyscapenabled': (
                    null() if row.lldpremsyscapenabled is None else
                    row.lldpremsyscapenabled.encode()),
                'lldpremsysdesc': (
                    null() if row.lldpremsysdesc is None else
                    row.lldpremsysdesc.encode()),
                'lldpremsysname': (
                    null() if row.lldpremsysname is None else
                    row.lldpremsysname.encode()),
                'enabled': row.enabled
            }
        )
    db.db_update(1112, statement)


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
        ifalias=None if row.ifalias is None else row.ifalias.decode(),
        ifdescr=None if row.ifdescr is None else row.ifdescr.decode(),
        ifadminstatus=row.ifadminstatus,
        ifoperstatus=row.ifoperstatus,
        ts_idle=row.ts_idle,
        cdpcachedeviceid=(
            None if row.cdpcachedeviceid is None else
            row.cdpcachedeviceid.decode()),
        cdpcachedeviceport=(
            None if row.cdpcachedeviceport is None else
            row.cdpcachedeviceport.decode()),
        cdpcacheplatform=(
            None if row.cdpcacheplatform is None else
            row.cdpcacheplatform.decode()),
        lldpremportdesc=(
            None if row.lldpremportdesc is None else
            row.lldpremportdesc.decode()),
        lldpremsyscapenabled=(
            None if row.lldpremsyscapenabled is None else
            row.lldpremsyscapenabled.decode()),
        lldpremsysdesc=(
            None if row.lldpremsysdesc is None else
            row.lldpremsysdesc.decode()),
        lldpremsysname=(
            None if row.lldpremsysname is None else
            row.lldpremsysname.decode()),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
