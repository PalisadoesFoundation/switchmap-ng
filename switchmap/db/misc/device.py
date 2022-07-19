"""Module for querying the Device table."""

from sqlalchemy import select

# Import project libraries
from switchmap.db import db
from switchmap import InterfaceDetail
from switchmap.db.models import L1Interface as _L1Interface
from switchmap.db.models import MacPort as _MacPort
from switchmap.db.table import device
from switchmap.db.misc import rows as _rows
from switchmap.db.misc import macdetail


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
        l1_rows = []
        mac_rows = []
        result = []
        l1interfaces = []
        idx_macs = []

        if bool(self._device) is True:
            # Get interface data
            statement = select(_L1Interface).where(
                    _L1Interface.idx_device == self._device.idx_device
            )
            l1_rows = db.db_select_row(1199, statement)
            for row in l1_rows:
                l1interfaces.append(_rows.l1interface(row))

            # Get MacIp and MacPort information
            for l1int in l1interfaces:
                # Initialize loop variables
                macresult = []
                idx_macs = []

                # Get the MAC idx_mac values associated with the interface.
                statement = select(_MacPort).where(
                        l1int.idx_l1interface == _MacPort.idx_l1interface
                )
                mac_rows = db.db_select_row(1200, statement)
                for row in mac_rows:
                    idx_macs.append(row.idx_mac)

                # Get the MacDetail values
                for item in idx_macs:
                    macresult.extend(macdetail.by_idx_mac(item))

                # Update the result
                result.append(
                    InterfaceDetail(
                        RL1Interface=l1int,
                        MacDetails=macresult
                    )
                )

        # Get interface data
        return result
