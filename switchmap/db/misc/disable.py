"""Module for disabling table entries."""

from sqlalchemy import select, update, and_, null

from switchmap.db import db
from switchmap.db.models import Device
from switchmap.db.table import L1Interface
from switchmap.db.table import Vlan
from switchmap.db.table import MacIp
from switchmap.db.table import Mac
from switchmap.db.table import MacPort


def post_poll_cleanup(idx_event):
    """Disable all column rows not related to idx_event.

    Args:
        idx_event: idx_event

    Returns:
        None

    """
    # Disable all devices and related entities that do not match
    # the idx_event value
    statement = select(Device).where(Device.idx_device != idx_event)
    rows = db.db_select(1226, statement)

    # Disable Device and its interfaces
    for row in rows:
        # Disable Device
        statement = update(Device).where(
                Device.idx_device == row.idx_device).values(
                    {
                        'enabled': 0
                    }
                )
        db.db_update(1126, statement)

        # Disable L1Interface
        statement = update(L1Interface).where(
                L1Interface.idx_device == row.idx_device).values(
                    {
                        'enabled': 0
                    }
                )
        db.db_update(1126, statement)

        # Disable Vlan
        statement = update(Vlan).where(
                Vlan.idx_device == row.idx_device).values(
                    {
                        'enabled': 0
                    }
                )
        db.db_update(1126, statement)

        # Disable MacIp
        statement = update(MacIp).where(
                MacIp.idx_device == row.idx_device).values(
                    {
                        'enabled': 0
                    }
                )
        db.db_update(1126, statement)

    # Disable Mac that don't match the idx_event value
    statement = select(Mac).where(Mac.idx_event != idx_event)
    rows = db.db_select(1226, statement)

    # Disable Device and its interfaces
    for row in rows:
        # Disable Mac
        statement = update(MacPort).where(
                Mac.idx_event == row.idx_event).values(
                    {
                        'enabled': 0
                    }
                )
        db.db_update(1126, statement)

        # Disable Mac
        statement = update(Mac).where(
                Mac.idx_event == row.idx_event).values(
                    {
                        'enabled': 0
                    }
                )
        db.db_update(1126, statement)
