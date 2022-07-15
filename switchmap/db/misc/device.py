"""Module for querying the Device table."""

from sqlalchemy import select, update, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import L1Interface as _L1Interface
from switchmap.db.table import RL1Interface
from switchmap.db.table import RDevice
from switchmap.db.table import device
from switchmap.db.misc import rows as _rows


class Device():
    """Get all Device data."""

    def __init__(self, hostname):
        """Initialize class.

        Args:
            hostname: Hostname to process

        Returns:
            None

        """
        # Initialize key variables
        self._hostname = hostname
        self._device = device.exists(self._hostname)

    def device(self):
        """Return system summary data.

        Args:
            None

        Returns:
            Result: RDevice object

        """
        # Get data
        result = self._device
        return result

    def interfaces(self):
        """Return L1 data for Ethernet ports only.

        Args:
            None

        Returns:
            self._ports: L1 data for Ethernet ports

        """
        # Initialize key variables
        result = []
        _interfaces = []

        # Setup
        if bool(self._device) is True:
            statement = select(_L1Interface).where(
                    _L1Interface.idx_device == self._device.idx_device
            )
        rows = db.db_select_row(1197, statement)
        for row in rows:
            _interfaces.append(_rows.l1interface(row))
        return result
