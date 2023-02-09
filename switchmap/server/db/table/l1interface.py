"""Module for querying the L1Interface table."""

from sqlalchemy import select, update, and_, null, func

# Import project libraries
from switchmap.server.db import db
from switchmap.server.db.models import L1Interface
from switchmap.server.db.misc import rows as _rows


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
        result = _rows.l1interface(row)
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
            L1Interface.idx_device == idx_device,
        )
    )
    rows = db.db_select_row(1205, statement)

    # Return
    for row in rows:
        result = _rows.l1interface(row)
        break
    return result


def findifalias(ifalias):
    """Find ifalias.

    Args:
        ifalias: Hostname

    Returns:
        result: L1Interface tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from database (Contains)
    statement = select(L1Interface).where(
        L1Interface.ifalias.like(
            func.concat(func.concat("%", ifalias.encode(), "%"))
        )
    )
    rows_contains = db.db_select_row(1188, statement)

    # Merge results and remove duplicates
    rows.extend(rows_contains)

    # Return
    for row in rows:
        result.append(_rows.l1interface(row))

    # Remove duplicates and return
    result = list(set(result))
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
                    null() if row.nativevlan is None else row.nativevlan
                ),
                trunk=null() if row.trunk is None else row.trunk,
                ifspeed=null() if row.ifspeed is None else row.ifspeed,
                ifalias=(
                    null() if row.ifalias is None else row.ifalias.encode()
                ),
                ifdescr=(
                    null() if row.ifdescr is None else row.ifdescr.encode()
                ),
                ifadminstatus=(
                    null() if row.ifadminstatus is None else row.ifadminstatus
                ),
                ifoperstatus=(
                    null() if row.ifoperstatus is None else row.ifoperstatus
                ),
                ts_idle=0 if not bool(row.ts_idle) else row.ts_idle,
                cdpcachedeviceid=(
                    null()
                    if row.cdpcachedeviceid is None
                    else row.cdpcachedeviceid.encode()
                ),
                cdpcachedeviceport=(
                    null()
                    if row.cdpcachedeviceport is None
                    else row.cdpcachedeviceport.encode()
                ),
                cdpcacheplatform=(
                    null()
                    if row.cdpcacheplatform is None
                    else row.cdpcacheplatform.encode()
                ),
                lldpremportdesc=(
                    null()
                    if row.lldpremportdesc is None
                    else row.lldpremportdesc.encode()
                ),
                lldpremsyscapenabled=(
                    null()
                    if row.lldpremsyscapenabled is None
                    else row.lldpremsyscapenabled.encode()
                ),
                lldpremsysdesc=(
                    null()
                    if row.lldpremsysdesc is None
                    else row.lldpremsysdesc.encode()
                ),
                lldpremsysname=(
                    null()
                    if row.lldpremsysname is None
                    else row.lldpremsysname.encode()
                ),
                enabled=row.enabled,
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
    statement = (
        update(L1Interface)
        .where(L1Interface.idx_l1interface == idx)
        .values(
            {
                "idx_device": row.idx_device,
                "ifindex": row.ifindex,
                "duplex": null() if row.duplex is None else row.duplex,
                "ethernet": null() if row.ethernet is None else row.ethernet,
                "nativevlan": (
                    null() if row.nativevlan is None else row.nativevlan
                ),
                "trunk": null() if row.trunk is None else row.trunk,
                "ifspeed": null() if row.ifspeed is None else row.ifspeed,
                "ifalias": (
                    null() if row.ifalias is None else row.ifalias.encode()
                ),
                "ifdescr": (
                    null() if row.ifdescr is None else row.ifdescr.encode()
                ),
                "ifadminstatus": (
                    null() if row.ifadminstatus is None else row.ifadminstatus
                ),
                "ifoperstatus": (
                    null() if row.ifoperstatus is None else row.ifoperstatus
                ),
                "ts_idle": 0 if not bool(row.ts_idle) else row.ts_idle,
                "cdpcachedeviceid": (
                    null()
                    if row.cdpcachedeviceid is None
                    else row.cdpcachedeviceid.encode()
                ),
                "cdpcachedeviceport": (
                    null()
                    if row.cdpcachedeviceport is None
                    else row.cdpcachedeviceport.encode()
                ),
                "cdpcacheplatform": (
                    null()
                    if row.cdpcacheplatform is None
                    else row.cdpcacheplatform.encode()
                ),
                "lldpremportdesc": (
                    null()
                    if row.lldpremportdesc is None
                    else row.lldpremportdesc.encode()
                ),
                "lldpremsyscapenabled": (
                    null()
                    if row.lldpremsyscapenabled is None
                    else row.lldpremsyscapenabled.encode()
                ),
                "lldpremsysdesc": (
                    null()
                    if row.lldpremsysdesc is None
                    else row.lldpremsysdesc.encode()
                ),
                "lldpremsysname": (
                    null()
                    if row.lldpremsysname is None
                    else row.lldpremsysname.encode()
                ),
                "enabled": row.enabled,
            }
        )
    )
    db.db_update(1112, statement)
