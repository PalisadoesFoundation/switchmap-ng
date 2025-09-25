"""Switchmap OUI library."""

# PIP imports
import pandas

# Module imports
from switchmap.server.db.table import IOui
from switchmap.server.db.table import oui as _oui
from switchmap.server.db import SCOPED_SESSION
from switchmap.server.db.models import Oui
from sqlalchemy.exc import IntegrityError


def update_db_oui(filepath, new=False):
    """Update the database with Oui data.

    Args:
        filepath: File to process
        new: If True, skip existing entry checks for new installations

    Returns:
        None

    Raises:
        FileNotFoundError: If the file cannot be found
        ValueError: If the CSV is improperly formatted
    """
    try:
        # Read OUI file
        df_ = pandas.read_csv(filepath, delimiter=":", header=None)
        if len(df_.columns) != 2:
            raise ValueError(
                "CSV must have exactly two columns: OUI and Organization"
            )
        df_.columns = ["oui", "organization"]

        # Validate for duplicate OUIs
        if df_["oui"].duplicated().any():
            raise ValueError("The input file contains duplicate OUIs.")
    except pandas.errors.EmptyDataError:
        raise ValueError("The CSV file is empty")

    # Process rows and update database
    rows = []
    for _, row in df_.iterrows():
        oui = row["oui"].strip()
        organization = row["organization"].strip()
        rows.append(IOui(oui=oui, organization=organization, enabled=1))

    if new:
        # Bulk insert on fresh install, skip checks
        try:
            _oui.insert_row(rows)
        except IntegrityError:
            SCOPED_SESSION.rollback()
            new = False
    if not new:
        # For updates, check existing entries
        for row in rows:
            existing_entry = _oui.exists(row.oui)
            if not existing_entry:
                _oui.insert_row([row])
            elif existing_entry.organization != row.organization:
                _oui.update_row(existing_entry.idx_oui, row)

    SCOPED_SESSION.commit()
