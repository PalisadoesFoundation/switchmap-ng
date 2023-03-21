"""Module for updating the database with topology data."""

import time
import socket
from copy import deepcopy

# Application imports
from switchmap.core import log
from switchmap.core import general
from switchmap.server.db.table import oui as _oui
from switchmap.server import ZoneObjects
from switchmap.server.db.table import (
    IIp,
    IMac,
)


def process(data, idx_zone, dns=True):
    """Process data received from a device.

    Args:
        data: Device data (dict)
        idx_zone: Zone index to which the data belongs
        dns: Do DNS lookups if True

    Returns:
        None

    """
    # Process the device
    _topology = Topology(data, idx_zone, dns=dns)
    _topology.process()


class Status:
    """Tracks the status of various Topology methods."""

    def __init__(self):
        """Instantiate the class."""
        self._mac = False
        self._ip = False

    @property
    def ip(self):
        """Provide the value of  the 'ip' property."""
        return self._ip

    @ip.setter
    def ip(self, value):
        """Set the 'ip' property."""
        self._ip = value

    @property
    def mac(self):
        """Provide the value of  the 'mac' property."""
        return self._mac

    @mac.setter
    def mac(self, value):
        """Set the 'mac' property."""
        self._mac = value


class Topology:
    """Update Device data in the database."""

    def __init__(self, data, idx_zone, dns=True):
        """Initialize class.

        Args:
            exists: RDevice object
            data: Dict of device data

        Returns:
            None

        """
        # Initialize key variables
        self._data = deepcopy(data)
        self._idx_zone = idx_zone
        self._dns = dns
        self._valid = False not in [
            bool(data),
            isinstance(data, dict),
        ]
        self._status = Status()
        self._start = int(time.time())

    def process(self):
        """Process data received from a device.

        Args:
            None

        Returns:
            None

        """
        # Process zone data
        macs = self.mac()
        ips = self.ip()
        result = ZoneObjects(ips=ips, macs=macs)
        return result

    def mac(self):
        """Update the Mac DB table.

        Args:
            None

        Returns:
            rows: List of unique IMac objects

        """
        # Initialize key variables
        all_macs = []
        unique_macs = []
        unique_ouis = []
        lookup = {}
        rows = []

        # Test validity
        if bool(self._valid) is False:
            # Log
            log_message = "No interfaces detected for for host {}".format(
                self._device.hostname
            )
            log.log2debug(1021, log_message)
            return rows

        # Get interfaces
        interfaces = self._data.get("layer1")

        # Log
        self.log("Mac")

        # Process each interface
        for ifindex, interface in interfaces.items():
            these_macs = interface.get("l1_macs")
            if bool(these_macs) is True:
                all_macs.extend(these_macs)

        # Get macs and ouis
        unique_macs = list(set(_.lower() for _ in all_macs))
        unique_ouis = list(set([_[:6].lower() for _ in unique_macs]))

        # Process ouis
        for item in sorted(unique_ouis):
            if bool(lookup.get(item)) is False:
                exists = _oui.exists(item)
                lookup[item] = exists.idx_oui if bool(exists) is True else 1

        # Process macs
        for item in sorted(unique_macs):
            rows.append(
                IMac(
                    idx_oui=lookup.get(item[:6], 1),
                    idx_zone=self._idx_zone,
                    mac=item,
                    enabled=1,
                )
            )

        # Log
        self.log("Mac", updated=True)

        # Everything is completed
        self._status.mac = True

        # Return
        rows = list(set(rows))
        return rows

    def ip(self):
        """Update the Ip DB table.

        Args:
            data: Ip data

        Returns:
            None

        """
        # Initialize key variables
        dns = self._dns
        ipv6 = None
        ipv4 = None
        rows = []

        # Test prerequisite
        if bool(self._status.macport) is False:
            self.log_invalid("Ip")
            return rows

        # Log
        self.log("Ip")

        # Get Ip data
        layer3 = self._data.get("layer3")
        if bool(layer3) is True:
            ipv4 = layer3.get("ipNetToMediaTable")
            ipv6 = layer3.get("ipNetToPhysicalPhysAddress")

            # Process arp table data
            for table in [ipv4, ipv6]:
                if bool(table) is True:

                    # Process data
                    for next_ip, _ in table.items():
                        # Create expanded lower case versions of the IP address
                        myp = general.ipaddress(next_ip)
                        if bool(myp) is False:
                            continue

                        # Get hostname for DB
                        if bool(dns) is True:
                            try:
                                hostname = socket.gethostbyaddr(myp.address)[0]
                            except:
                                hostname = None
                        else:
                            hostname = None

                        # Create a DB record
                        rows.append(
                            IIp(
                                idx_zone=self._idx_zone,
                                address=myp.address,
                                hostname=hostname,
                                version=myp.version,
                                enabled=1,
                            )
                        )

        # Log
        self.log("Ip", updated=True)

        # Everything is completed
        self._status.ip = True

        # Return
        rows = list(set(rows))
        return rows

    def log(self, table, updated=False):
        """Create standardized log messaging.

        Args:
            table: Name of table being updated
            updated: True if the table has been updated

        Returns:
            None

        """
        # Initialize key variables
        log_message = '\
{} table update "{}" for host {}, {} seconds after starting'.format(
            "Completed" if bool(updated) else "Starting",
            table,
            self._device.hostname,
            int(time.time()) - self._start,
        )
        log.log2debug(1028, log_message)

    def log_invalid(self, table):
        """Create standardized log messaging for invalid states.

        Args:
            table: Name of table being updated
            updated: True if the table has been updated

        Returns:
            None

        """
        # Initialize key variables
        log_message = "\
Invalid update sequence for table {} when processing host {}, {} seconds\
after starting".format(
            table,
            self._device.hostname,
            int(time.time()) - self._start,
        )
        log.log2debug(1029, log_message)
