"""Module for updating the database with topology data."""

import time
import socket
from copy import deepcopy

# Application imports
from switchmap.core import log
from switchmap.core import general
from switchmap.core.mac_utils import decode_mac_address
from switchmap.server.db.table import oui as _oui
from switchmap.server import ZoneObjects
from switchmap.server import PairMacIp
from switchmap.server.db.table import (
    IIp,
    IMac,
)


def _decode_mac_address(encoded_mac):
    """Decode double-encoded MAC addresses from async poller.
    
    Args:
        encoded_mac: MAC address that may be double hex-encoded
        
    Returns:
        str: Properly formatted MAC address or original if already valid
        
    """
    import binascii
    
    try:
        # Try to decode hex-encoded string to ASCII
        if isinstance(encoded_mac, str) and len(encoded_mac) > 12:
            decoded = binascii.unhexlify(encoded_mac).decode('ascii')
            # Check if it starts with '0x' (hex prefix)
            if decoded.startswith('0x'):
                return decoded[2:]  # Return MAC without '0x' prefix
        
        # If decoding fails or doesn't match pattern, return original
        return encoded_mac
        
    except Exception:
        # If any decoding fails, return original
        return encoded_mac


def process(data, idx_zone, dns=True):
    """Process data received from a device.

    Args:
        data: Device data (dict)
        idx_zone: Zone index to which the data belongs
        dns: Do DNS lookups if True

    Returns:
        results: ZoneObjects object
    """
    # Process the device
    _topology = Topology(data, idx_zone, dns=dns)
    result = _topology.process()
    return result


class Status:
    """Tracks the status of various Topology methods."""

    def __init__(self):
        """Instantiate the class.

        Args:
            None

        Returns:
            None
        """
        self._mac = False
        self._ip = False

    @property
    def ip(self):
        """Provide the value of the 'ip' property.

        Args:
            None

        Returns:
            None
        """
        return self._ip

    @ip.setter
    def ip(self, value):
        """Set the 'ip' property.

        Args:
            value: Value to set

        Returns:
            None
        """
        self._ip = value

    @property
    def mac(self):
        """Provide the value of the 'mac' property.

        Args:
            None

        Returns:
            None
        """
        return self._mac

    @mac.setter
    def mac(self, value):
        """Set the 'mac' property.

        Args:
            value: Value to set

        Returns:
            None
        """
        self._mac = value

    @property
    def macip(self):
        """Provide the value of the 'macip' property.

        Args:
            None

        Returns:
            None
        """
        return self._macip

    @macip.setter
    def macip(self, value):
        """Set the 'macip' property.

        Args:
            value: Value to set

        Returns:
            None
        """
        self._macip = value


class Topology:
    """Update Device data in the database."""

    def __init__(self, data, idx_zone, dns=True):
        """Initialize class.

        Args:
            data: Dict of device data
            idx_zone: idx_zone of the Zone being processed
            dns: Do DNS lookups if True

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
        self._hostname = str(self._data["misc"]["host"]).lower()
        self._arp_table = _arp_table(idx_zone, self._data)

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
        pairmacips = self.macip()
        result = ZoneObjects(ips=ips, macs=macs, pairmacips=pairmacips)
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
            log_message = "No MAC addresses detected for for host {}".format(
                self._hostname
            )
            log.log2debug(1083, log_message)
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

        # Process ARP table
        for item in self._arp_table:
            all_macs.append(item.mac)

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
            None

        Returns:
            None
        """
        # Initialize key variables
        rows = []

        # Test prerequisite
        if bool(self._status.mac) is False:
            self.log_invalid("Ip")
            return rows

        # Log
        self.log("Ip")

        # Process the ARP Table
        ips = [item.ip for item in self._arp_table]
        unique_ips = set(ips)
        hostname_map = {}
        if self._dns:
            for item in unique_ips:
                try:
                    hostname_map[item] = socket.gethostbyaddr(item)[0]
                except Exception as e:
                    log.log2debug(
                        1035,
                        f"""\
Unexpected error during DNS lookup for {item}: {str(e)}""",
                    )
                    hostname_map[item] = None
                except:
                    log.log2debug(
                        1037, f"Unexpected error during DNS lookup for {item}"
                    )
                    hostname_map[item] = None

        # Create a DB record
        rows = [
            IIp(
                idx_zone=self._idx_zone,
                address=item.ip,
                hostname=hostname_map.get(item.ip) if self._dns else None,
                version=item.ip_version,
                enabled=1,
            )
            for item in self._arp_table
        ]

        # Log
        self.log("Ip", updated=True)

        # Everything is completed
        self._status.ip = True

        # Return
        rows = list(set(rows))
        return rows

    def macip(self):
        """Update the MacIp DB table.

        Args:
            None

        Returns:
            rows: List of PairMacIp objects
        """
        # Initialize key variables
        rows = []

        # Test prerequisite
        if bool(self._status.ip) is False:
            self.log_invalid("MacIp")
            return rows

        # Log
        self.log("MacIp")

        # Get MacIp data
        rows = self._arp_table

        # Log
        self.log("MacIp", updated=True)

        # Everything is completed
        self._status.macip = True

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
        suffix = (
            ""
            if bool(updated) is False
            else ", {} seconds after starting.".format(
                int(time.time()) - self._start
            )
        )
        log_message = '\
{} "{}" data retrieval for host {}{}'.format(
            "Completed" if bool(updated) else "Starting",
            table,
            self._hostname,
            suffix,
        )
        log.log2debug(1082, log_message)

    def log_invalid(self, table):
        """Create standardized log messaging for invalid states.

        Args:
            table: Name of table being updated

        Returns:
            None
        """
        # Initialize key variables
        log_message = "\
Invalid update sequence for table {} when processing host {}, {} seconds\
after starting".format(
            table,
            self._hostname,
            int(time.time()) - self._start,
        )
        log.log2debug(1079, log_message)


def _process_pairmacips(idx_zone, table):
    """Update the mac DB table.

    Args:
        idx_zone: idx_zone value in the DB
        table: ARP table keyed by ip address

    Returns:
        results: List of PairMacIp objects
    """
    # Initialize key variables
    results = []

    # Process data
    for next_ip, next_mac in table.items():
        # Create expanded lower case versions of the IP address
        myp = general.ipaddress(next_ip)
        if bool(myp) is False:
            continue

        # Create lowercase version of mac address. Skip if invalid
        # Handle double-encoded MAC addresses from async poller
        decoded_mac = decode_mac_address(next_mac)
        mactest = general.mac(decoded_mac)
        if bool(mactest.valid) is False:
            continue
        else:
            mac = mactest.mac

        # Update the results
        results.append(PairMacIp(mac=mac, ip=myp.address, idx_zone=idx_zone))

    # Return
    return results


def _arp_table(idx_zone, data):
    """Update the Ip DB table.

    Args:
        idx_zone: Zone table index
        data: YAML data

    Returns:
        results: List of PairMacIp objects
    """
    # Get Ip data
    layer3 = data.get("layer3")
    results = []

    if bool(layer3) is True:
        ipv4 = layer3.get("ipNetToMediaTable")
        ipv6 = layer3.get("ipNetToPhysicalPhysAddress")

        # Process arp table data
        for table in [ipv4, ipv6]:
            if bool(table) is True:
                # Process data
                for next_ip, next_mac in table.items():
                    # Create expanded lower case versions of the IP address
                    myp = general.ipaddress(next_ip)
                    if bool(myp) is False:
                        continue

                    # Create lowercase version of mac address. Skip if invalid.
                    # Handle double-encoded MAC addresses from async poller
                    decoded_mac = decode_mac_address(next_mac)
                    mactest = general.mac(decoded_mac)
                    if bool(mactest.valid) is False:
                        continue
                    else:
                        mac = mactest.mac

                    # Update the results
                    results.append(
                        PairMacIp(
                            mac=mac,
                            ip=myp.address,
                            ip_version=myp.version,
                            idx_zone=idx_zone,
                        )
                    )
    return results
