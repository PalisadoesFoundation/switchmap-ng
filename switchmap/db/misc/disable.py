"""Module for disabling table entries."""

from sqlalchemy import select, update

from switchmap.db import db
from switchmap.db.models import Device
from switchmap.db.models import L1Interface
from switchmap.db.models import Vlan
from switchmap.db.models import MacIp
from switchmap.db.models import Mac
from switchmap.db.models import MacPort


def post_poll_cleanup(idx_event):
    """Disable all column rows not related to idx_event.

    Args:
        idx_event: idx_event

    Returns:
        None

    """
    # Initialize key variables
    idx_devices = []
    idx_macs = []
    not_idx_events = []

    # Disable all devices and related entities that do not match
    # the idx_event value
    statement = select(Device).where(Device.idx_event != idx_event)
    rows = db.db_select_row(1005, statement)

    # Process data
    for row in rows:
        idx_devices.append(row.idx_device)
    for idx_device in idx_devices:
        # Disable Device
        statement = (
            update(Device).where(Device.idx_device == idx_device).values({"enabled": 0})
        )
        db.db_update(1124, statement)

        # Disable L1Interface
        statement = (
            update(L1Interface)
            .where(L1Interface.idx_device == idx_device)
            .values({"enabled": 0})
        )
        db.db_update(1125, statement)

        # Disable Vlan
        statement = (
            update(Vlan).where(Vlan.idx_device == idx_device).values({"enabled": 0})
        )
        db.db_update(1127, statement)

        # Disable MacIp
        statement = (
            update(MacIp).where(MacIp.idx_device == idx_device).values({"enabled": 0})
        )
        db.db_update(1145, statement)

    # Disable Mac that don't match the idx_event value
    statement = select(Mac).where(Mac.idx_event != idx_event)
    rows = db.db_select_row(1064, statement)

    # Process data
    for row in rows:
        not_idx_events.append(row.idx_event)
        idx_macs.append(row.idx_mac)

    for not_idx_event in not_idx_events:
        # Disable Mac
        statement = (
            update(Mac).where(Mac.idx_event == not_idx_event).values({"enabled": 0})
        )
        db.db_update(1144, statement)

    for idx_mac in idx_macs:

        # Disable MacPort
        statement = (
            update(MacPort).where(MacPort.idx_mac == idx_mac).values({"enabled": 0})
        )
        db.db_update(1069, statement)
