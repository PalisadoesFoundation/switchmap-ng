"""Module for querying the Device table."""

from sqlalchemy import select, and_

# Import project libraries
from switchmap.server.db import db
from switchmap import InterfaceDetail
from switchmap import DeviceDetail
from switchmap.server.db.models import L1Interface as _L1Interface
from switchmap.server.db.models import MacPort as _MacPort
from switchmap.server.db.models import VlanPort as _VlanPort
from switchmap.server.db.models import Vlan as _Vlan
from switchmap.server.db.table import device
from switchmap.server.db.misc import rows as _rows
from switchmap.server.db.misc.interface import mac as macdetail
from switchmap.server.db.misc.interface import vlan


class Device:
    """Get all Device data."""

    def __init__(self, idx_zone, hostname):
        """Initialize class.

        Args:
            idx_zone: Zone index to which the data belongs
            hostname: Hostname to process

        Returns:
            None

        """
        # Initialize key variables
        self._hostname = hostname
        self._device = device.exists(idx_zone, self._hostname)

    def data(self):
        """Return complete device.

        Args:
            None

        Returns:
            Result: DeviceDetail object

        """
        # Get data
        interfaces_ = self.interfaces()
        device_ = self.device()
        result = DeviceDetail(RDevice=device_, InterfaceDetails=interfaces_)
        return result

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
                vlans = []

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

                # Get Vlan data
                vlans = vlan.by_idx_l1interface(l1int.idx_l1interface)

                # Update the result
                result.append(
                    InterfaceDetail(
                        RL1Interface=l1int, MacDetails=macresult, RVlans=vlans
                    )
                )

        # Get interface data
        return result


def vlanports(idx_device):
    """Get all the VlanPorts for a device.

    Args:
        idx_device:

    Returns:
        result: List of RVlanPort tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from dataase
    statement = select(_VlanPort).where(
        and_(
            _Vlan.idx_device == idx_device,
            _Vlan.idx_vlan == _VlanPort.idx_vlan,
        )
    )
    rows = db.db_select_row(1190, statement)

    # Return
    for row in rows:
        result.append(_rows.vlanport(row))
    return result
