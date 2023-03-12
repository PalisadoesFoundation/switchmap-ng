"""Module for getting interface specific VLAN data."""

# PIP3 imports
from sqlalchemy import select, and_

# Application imports
from switchmap.server.db import db
from switchmap.server.db.misc import rows as _rows
from switchmap.server.db.models import Vlan as _Vlan
from switchmap.server.db.models import VlanPort as _VlanPort


def by_idx_l1interface(idx_l1interface):
    """Search for VLANs tied to interface.

    Args:
        idx_l1interface: idx_l1interface

    Returns:
        result: List of RVlan objects

    """
    # Initialize key variables
    result = []
    rows = []

    # Get data
    statement = select(_Vlan).where(
        and_(
            _VlanPort.idx_l1interface == idx_l1interface,
            _VlanPort.idx_vlan == _Vlan.idx_vlan,
        )
    )
    rows = db.db_select_row(1203, statement)
    for row in rows:
        result.append(_rows.vlan(row))

    # Return
    return result
