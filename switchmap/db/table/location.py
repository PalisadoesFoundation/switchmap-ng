"""Module for querying the Location table."""


from sqlalchemy import select, update, null

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
    statement = select(Location).where(Location.idx_location == idx)
    rows = db.db_select_row(1225, statement)

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
                name=(
                    null() if bool(row.name) is False else
                    row.name.encode()),
                company_name=(
                    null() if bool(row.company_name) is False else
                    row.company_name.encode()),
                address_0=(
                    null() if bool(row.address_0) is False else
                    row.address_0.encode()),
                address_1=(
                    null() if bool(row.address_1) is False else
                    row.address_1.encode()),
                address_2=(
                    null() if bool(row.address_2) is False else
                    row.address_2.encode()),
                city=(
                    null() if bool(row.city) is False else
                    row.city.encode()),
                state=(
                    null() if bool(row.state) is False else
                    row.state.encode()),
                country=(
                    null() if bool(row.country) is False else
                    row.country.encode()),
                postal_code=(
                    null() if bool(row.postal_code) is False else
                    row.postal_code.encode()),
                phone=(
                    null() if bool(row.phone) is False else
                    row.phone.encode()),
                notes=(
                    null() if bool(row.notes) is False else
                    row.notes.encode()),
                enabled=row.enabled
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
        Location.idx_location == idx).values(
            {
                'name': (
                    null() if bool(row.name) is False else
                    row.name.encode()),
                'company_name': (
                    null() if bool(row.company_name) is False else
                    row.company_name.encode()),
                'address_0': (
                    null() if bool(row.address_0) is False else
                    row.address_0.encode()),
                'address_1': (
                    null() if bool(row.address_1) is False else
                    row.address_1.encode()),
                'address_2': (
                    null() if bool(row.address_2) is False else
                    row.address_2.encode()),
                'city': (
                    null() if bool(row.city) is False else
                    row.city.encode()),
                'state': (
                    null() if bool(row.state) is False else
                    row.state.encode()),
                'country': (
                    null() if bool(row.country) is False else
                    row.country.encode()),
                'postal_code': (
                    null() if bool(row.postal_code) is False else
                    row.postal_code.encode()),
                'phone': (
                    null() if bool(row.phone) is False else
                    row.phone.encode()),
                'notes': (
                    null() if bool(row.notes) is False else
                    row.notes.encode()),
                'enabled': row.enabled
            }
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
        name=(
            None if row.name is None else row.name.decode()),
        company_name=(
            None if row.company_name is None else row.company_name.decode()),
        address_0=(
            None if row.address_0 is None else row.address_0.decode()),
        address_1=(
            None if row.address_1 is None else row.address_1.decode()),
        address_2=(
            None if row.address_2 is None else row.address_2.decode()),
        city=(
            None if row.city is None else row.city.decode()),
        state=(
            None if row.state is None else row.state.decode()),
        country=(
            None if row.country is None else row.country.decode()),
        postal_code=(
            None if row.postal_code is None else row.postal_code.decode()),
        phone=(
            None if row.phone is None else row.phone.decode()),
        notes=(
            None if row.notes is None else row.notes.decode()),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
