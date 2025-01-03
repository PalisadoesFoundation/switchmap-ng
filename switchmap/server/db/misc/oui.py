"""Switchmap OUI library."""

# PIP imports
import pandas

# Module imports
from switchmap.server.db.table import IOui
from switchmap.server.db.table import oui as _oui
from switchmap.server.db import SCOPED_SESSION
from switchmap.server.db.models import Oui


def update_db_oui(filepath):
    """Update the database with Oui data.

    Args:
        df_: pd.Dataframe

    Returns:
        None

    """
    # Initialize key variables
    inserts = []
    rows = []

    # Get the row count
    row_count = SCOPED_SESSION.query(Oui).count()

    # Read OUI file
    df_ = pandas.read_csv(filepath, delimiter=":")
    df_.columns = ["oui", "organization"]

    # Process DataFrame
    for _, row in df_.iterrows():
        rows.append(
            IOui(oui=row["oui"], organization=row["organization"], enabled=1)
        )

    # Insert rows into the database if it is empty
    if row_count <= 1:
        _oui.insert_row(rows)

    # Selectively update rows if the database is not empty
    else:
        for row in rows:
            # Determine whether the record already exists
            exists = _oui.exists(row.oui)

            # Process insertions and updates
            if bool(exists) is False:
                inserts.add(row)
            else:
                if exists.organization != row.organization:
                    _oui.update_row(exists.idx_oui, row)

        # Do insertions
        if bool(inserts):
            _oui.insert_row(inserts)
