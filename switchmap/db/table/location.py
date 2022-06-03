"""Module for querying the Location table."""


from sqlalchemy import select, update, and_

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Location
from switchmap.db.table import RLocation


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_location

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(
        Location.idx_location).where(Location.idx_location == idx)
    rows = db.db_select(1225, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return bool(result)


def insert_row(rows):
    """Create a Location table entry.

    Args:
        rows: ILocation objects

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
            Location(
                name=row.name.encode(),
                company_name=row.company_name.encode(),
                address_0=row.address_0.encode(),
                address_1=row.address_1.encode(),
                address_2=row.address_2.encode(),
                city=row.city.encode(),
                state=row.state.encode(),
                country=row.country.encode(),
                postal_code=row.postal_code.encode(),
                phone=row.phone.encode(),
                notes=row.notes.encode(),
                enabled=1
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1043, inserts)


def update_row(idx, row):
    """Upadate a Location table entry.

    Args:
        idx: idx_location value
        row: ILocation object

    Returns:
        None

    """
    # Update
    statement = update(Location).where(
        and_(
            Location.idx_location == idx
        ).values(
            {
                'name': row.name.encode(),
                'company_name': row.company_name.encode(),
                'address_0': row.address_0.encode(),
                'address_1': row.address_1.encode(),
                'address_2': row.address_2.encode(),
                'city': row.city.encode(),
                'state': row.state.encode(),
                'country': row.country.encode(),
                'postal_code': row.postal_code.encode(),
                'phone': row.phone.encode(),
                'notes': row.notes.encode(),
                'enabled': row.enabled
            }
        )
    )
    db.db_update(1126, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Location row

    Returns:
        result: RLocation tuple

    """
    # Initialize key variables
    result = RLocation(
        idx_location=row.idx_location,
        name=row.name.decode(),
        company_name=row.company_name.decode(),
        address_0=row.address_0.decode(),
        address_1=row.address_1.decode(),
        address_2=row.address_2.decode(),
        city=row.city.decode(),
        state=row.state.decode(),
        country=row.country.decode(),
        postal_code=row.postal_code.decode(),
        phone=row.phone.decode(),
        notes=row.notes.decode(),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
