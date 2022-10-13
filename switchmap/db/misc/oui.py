"""Switchmap OUI library."""


# PIP imports
import pandas

# Module imports
from switchmap.core import log
from switchmap.db.table import IOui
from switchmap.db.table import oui as _oui


def update_db_oui(filepath, new=False):
    """Update the database with Oui data.

    Args:
        df_: pd.Dataframe
        new: True if newly created DB. Existing records are not checked.

    Returns:
        None

    """
    # Initialize key variables
    inserts = []

    # Read OUI file
    df_ = pandas.read_csv(filepath, delimiter=":")
    df_.columns = ["oui", "organization"]

    # Process DataFrame (Enables)
    for _, row in df_.iterrows():
        db_record = _oui.exists(row["oui"]) if bool(new) else False
        file_record = IOui(
            oui=row["oui"], organization=row["organization"], enabled=1
        )

        # Process insertions and updates
        if bool(db_record) is False:
            try:
                inserts.append(file_record)
            except:
                log_message = """OUI: {} for organization: {} already exists. Ignoring. Don\'t use the \
--new_installation flag for updating the OUI data.""".format(
                    row["oui"], row["organization"]
                )

                log.log2see(1116, log_message)
        else:
            if db_record.organization != file_record.organization:
                _oui.update_row(db_record.idx_oui, file_record)

    # Do insertions
    if bool(inserts):
        _oui.insert_row(inserts)
