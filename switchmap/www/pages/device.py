#!usr/bin/env python3
"""Class for creating device web pages."""

import textwrap
import os
import time
import csv

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.topology.translator import Translator
from switchmap.constants import CONFIG
from switchmap.utils import general
from switchmap.utils import log


class _RawCol(Col):
    """Class outputs whatever it is given and will not escape it."""

    def td_format(self, content):
        return content


class Device(object):
    """Class that creates the device's various HTML tables."""

    def __init__(self, config, host, ifindexes=None):
        """Initialize the class.

        Args:
            config: Configuration object
            host: Hostname to process
            ifindexes: List of ifindexes to retrieve. If None, then do all.

        Returns:
            None

        """
        # Process YAML file for host
        self.hostname = host
        translation = Translator(config, self.hostname)
        self.port_data = translation.ethernet_data()
        self.system_data = translation.system_summary()
        self.ifindexes = ifindexes
        self.display = _Display()

    def ports(self):
        """Create the ports table for the device.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        data = Port(
            self.port_data, self.hostname, self.display, ifindexes=self.ifindexes).data()

        # Populate the table
        table = PortTable(data)

        # Get HTML
        html = table.__html__()

        # Return
        return html

    def system(self):
        """Create summary table for the devie.

        Args:
            None

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        data = System(self.system_data).data()

        # Populate the table
        table = SystemTable(data)

        # Get HTML
        html = table.__html__()

        # Return
        return html


class PortTable(Table):
    """Declaration of the columns in the Ports table."""

    # Initialize class variables
    port = Col('Port')
    vlan = Col('VLAN')
    state = Col('State')
    days_inactive = Col('Days Inactive')
    speed = Col('Speed')
    duplex = Col('Duplex')
    label = Col('Port Label')
    trunk = Col('Trunk')
    cdp = _RawCol('CDP')
    lldp = _RawCol('LLDP')
    mac_address = _RawCol('Mac Address')
    manufacturer = _RawCol('Manufacturer')
    ip_address = _RawCol('IP Address')
    hostname = _RawCol('DNS Name')

    # Define the CSS class to use for the header row
    classes = ['table']

    def get_tr_attrs(self, item):
        """Apply CSS class attributes to regular table row.

        args:
            item: Row of data

        returns:
            class of active stuff

        """
        # Special treatment for rows of enabled ports
        if item.enabled() is True:
            if item.active() is True:
                # Port with link
                return {'class': 'success'}
            else:
                # Port without link
                return {'class': 'info'}
        else:
            # Disabled port
            return {'class': 'warning'}


class PortRow(object):
    """Declaration of the rows in the Ports table."""

    def __init__(self, row):
        """Method initializing the class.

        Args:
            row: List of row values
                port: Port name string
                vlan: VLAN of port string
                state: State of port string
                days_inactive: Number of days the port's inactive string
                speed: Speed of port string
                duplex: Duplex of port string
                label: Label given to the port by the network manager
                trunk: Whether a trunk or not
                cdp: CDP data string
                lldp: LLDP data string
                mac_address: MAC Address
                manufacturer: Name of the manufacturer

        Returns:
            None

        """
        # Initialize key variables
        [
            self.port, self.vlan, self.state, self.days_inactive, self.speed,
            self.duplex, self.label, self.trunk, self.cdp, self.lldp,
            self.mac_address, self.manufacturer, self.ip_address,
            self.hostname] = row

    def active(self):
        """Active ports."""
        return bool(self.state == 'Active')

    def enabled(self):
        """Enabled ports."""
        return bool(self.state != 'Disabled')


class Port(object):
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, device_data, hostname, display, ifindexes=None):
        """Method instantiating the class.

        Args:
            device_data: Dictionary of device data
            hostname: Name of host to which this data belongs
            display: _Display object
            ifindexes: List of ifindexes to retrieve. If None, then do all.

        Returns:
            None

        """
        # Initialize key variables
        self.device_data = device_data
        self.display = display
        self.hostname = hostname
        if bool(ifindexes) is True and isinstance(ifindexes, list) is True:
            self.ifindexes = ifindexes
        else:
            self.ifindexes = []

    def data(self):
        """Return data for the device's ports.

        Args:
            None

        Returns:
            rows: List of Col objects

        """
        # Initialize key variables
        rows = []
        idle_history = {}
        config = CONFIG

        # Get idle data for device
        idle_filepath = (
            '{}/{}.yaml'.format(config.idle_directory(), self.hostname)
            )
        if os.path.isfile(idle_filepath) is True:
            idle_history = general.read_yaml_file(idle_filepath)

        # Create rows of data
        for ifindex, port_data in sorted(self.device_data.items()):
            # Filter results if required
            if bool(self.ifindexes) is True:
                if int(port_data['ifIndex']) not in self.ifindexes:
                    continue

            # Assign values for Ethernet ports only
            name = port_data['ifName']
            label = port_data['ifAlias']

            # Get port data
            port = _Port(port_data)
            speed = port.speed()
            inactive = self._inactive(ifindex, idle_history)
            vlan = port.vlan()
            state = port.state()
            duplex = port.duplex()
            trunk = port.trunk()
            cdp = port.cdp()
            lldp = port.lldp()
            mac_addresses = port.mac_addresses()

            # Get HTML related to the MAC address
            html = self.display.html(mac_addresses)
            manufacturer = html['manufacturer']
            ip_address = html['ip_address']
            hostname = html['hostname']
            mac_address = html['mac_address']

            # Append row of data
            rows.append(PortRow([
                name, vlan, state, inactive, speed, duplex,
                label, trunk, cdp, lldp, mac_address, manufacturer,
                ip_address, hostname]))

        # Return
        return rows

    def _inactive(self, ifindex, idle_history):
        """Return days inactive for port.

        Args:
            ifindex: IfIndex of port (String)
            idle_history: History of idleness of port

        Returns:
            inactive: Days the port has been inactive

        """
        # Initialize key variables
        inactive = 'TBD'
        s_ifindex = str(ifindex)

        # Return
        if s_ifindex in idle_history:
            if bool(idle_history[s_ifindex]) is False:
                inactive = ''
            else:
                seconds = int(time.time()) - idle_history[s_ifindex]
                inactive = int(round(seconds / 86400, 0))

        return inactive


class _Port(object):
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, port_data):
        """Method instantiating the class.

        Args:
            port_data: Dictionary of port data

        Returns:
            None

        """
        # Initialize key variables
        self.port_data = port_data
        self.max_macs = 4

    def is_trunk(self):
        """Return trunk status of port.

        Args:
            None

        Returns:
            result: True if Trunk

        """
        # Assign key variables
        result = False
        port_data = self.port_data

        # Get trunk string
        if 'jm_trunk' in port_data:
            if bool(port_data['jm_trunk']) is True:
                result = True

        # Return
        return result

    def trunk(self):
        """Return string for trunk status of port.

        Args:
            None

        Returns:
            trunk: Trunk state

        """
        # Assign key variables
        trunk = ''

        # Get trunk string
        if bool(self.is_trunk()) is True:
            trunk = 'Trunk'

        # Return
        return trunk

    def mac_addresses(self):
        """Return string for mac_address on port.

        Args:
            None

        Returns:
            mac_addresses: mac_address state

        """
        # Assign key variables
        mac_addresses = []
        port_data = self.port_data

        # Don't show manufacturer on trunk ports
        if bool(self.is_trunk()) is False:
            if 'jm_macs' in port_data:
                mac_addresses = port_data['jm_macs'][:4]

        # Return
        return mac_addresses

    def speed(self):
        """Return port speed.

        Args:
            None

        Returns:
            speed: Port speed

        """
        # Assign key variables
        port_data = self.port_data

        # Assign speed
        if _port_up(port_data) is False:
            speed = 'N/A'
        else:
            if 'ifHighSpeed' in port_data:
                value = port_data['ifHighSpeed']
            elif 'ifSpeed' in port_data:
                value = int(port_data['ifSpeed']) / 1000000
            else:
                value = None

            if bool(value) is True:
                if value >= 1000:
                    speed = ('%.0fG') % (value / 1000)
                elif value > 0 and value < 1000:
                    speed = ('%.0fM') % (value)
                else:
                    speed = 'N/A'
            else:
                speed = 'N/A'

        # Return
        return speed

    def vlan(self):
        """Return VLAN number.

        Args:
            None

        Returns:
            vlans

        """
        # Assign key variables
        port_data = self.port_data
        vlans = 'N/A'

        # Assign VLAN
        if 'jm_trunk' in port_data:
            if port_data['jm_trunk'] is False:
                if 'jm_vlan' in port_data:
                    if port_data['jm_vlan'] is not None:
                        values = [
                            str(value) for value in port_data['jm_vlan']]
                        vlans = ' '.join(values)
            else:
                if 'jm_nativevlan' in port_data:
                    vlans = str(port_data['jm_nativevlan'])

        # Return
        return vlans

    def state(self):
        """Return port state string.

        Args:
            None

        Returns:
            state: State string

        """
        # Assign key variables
        port_data = self.port_data

        # Assign state
        if _port_enabled(port_data) is False:
            state = 'Disabled'
        else:
            if _port_up(port_data) is False:
                state = 'Inactive'
            else:
                state = 'Active'

        # Return
        return state

    def duplex(self):
        """Return port duplex string.

        Args:
            None

        Returns:
            duplex: Duplex string

        """
        # Assign key variables
        port_data = self.port_data
        duplex = 'Unknown'
        options = {
            0: 'Unknown',
            1: 'Half',
            2: 'Full',
            3: 'Half-Auto',
            4: 'Full-Auto',
        }

        # Assign duplex
        if _port_up(port_data) is False:
            duplex = 'N/A'
        else:
            if 'jm_duplex' in port_data:
                duplex = options[port_data['jm_duplex']]

        # Return
        return duplex

    def cdp(self):
        """Return port CDP HTML string.

        Args:
            None

        Returns:
            value: required string

        """
        # Assign key variables
        port_data = self.port_data
        value = ''

        # Determine whether CDP is enabled and update string
        if 'cdpCacheDeviceId' in port_data:
            value = ('%s<br>%s<br>%s') % (
                port_data['cdpCacheDeviceId'],
                port_data['cdpCachePlatform'],
                port_data['cdpCacheDevicePort'])

        # Return
        return value

    def lldp(self):
        """Return port LLDP HTML string.

        Args:
            None

        Returns:
            value: required string

        """
        # Assign key variables
        port_data = self.port_data
        value = ''

        # Determine whether LLDP is enabled and update string
        if 'lldpRemSysDesc' in port_data:
            value = ('%s<br>%s<br>%s') % (
                port_data['lldpRemSysName'],
                port_data['lldpRemPortDesc'],
                port_data['lldpRemSysDesc'])

        # Return
        return value


class SystemTable(Table):
    """Declaration of the columns in the Systems table."""

    # Initialize class variables
    parameter = Col('Parameter')
    value = _RawCol('Value')

    # Define the CSS class to use for the header row
    thead_classes = ['tblHead']
    classes = ['table']


class SystemRow(object):
    """Declaration of the rows in the Systems table."""

    def __init__(self, parameter, value):
        """Method initializing the class.

        Args:
            parameter: System parameter string
            value: System parameter value string

        Returns:
            None

        """
        # Initialize key variables
        self.parameter = parameter
        self.value = value


class System(object):
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, system_data):
        """Method instantiating the class.

        Args:
            system_data: Dictionary of system data

        Returns:
            None

        """
        # Initialize key variables
        self.system_data = system_data

    def data(self):
        """Return data for the device's system information.

        Args:
            None

        Returns:
            rows: List of Col objects

        """
        # Initialize key variables
        rows = []

        # Configured name
        rows.append(
            SystemRow('System Name', self.system_data['sysName']))

        # System IP Address / Hostname
        rows.append(
            SystemRow('System Hostname', self.system_data['hostname']))

        # System Description
        rows.append(
            SystemRow(
                'System Description',
                textwrap.fill(
                    self.system_data['sysDescr']).replace('\n', '<br>')))

        # System Object ID
        rows.append(
            SystemRow('System sysObjectID', self.system_data['sysObjectID']))

        # System Uptime
        rows.append(
            SystemRow('System Uptime', _uptime(self.system_data['sysUpTime'])))

        # Return
        return rows


def _port_enabled(port_data):
    """Return whether port is enabled.

    Args:
        port_data: Data related to the port

    Returns:
        active: True if active

    """
    # Initialize key variables
    enabled = False

    # Assign state
    if 'ifAdminStatus' in port_data:
        value = port_data['ifAdminStatus']
        if value == 1:
            enabled = True

    # Return
    return enabled


def _port_up(port_data):
    """Return whether port is up.

    Args:
        port_data: Data related to the port

    Returns:
        port_up: True if active

    """
    # Initialize key variables
    port_up = False

    # Assign state
    if _port_enabled(port_data) is True:
        if 'ifOperStatus' in port_data:
            if port_data['ifOperStatus'] == 1:
                port_up = True

    # Return
    return port_up


def _uptime(seconds):
    """Return uptime string.

    Args:
        seconds: Seconds of uptime

    Returns:
        result: Uptime string

    """
    # Initialize key variables
    (minutes, remainder_seconds) = divmod(seconds/100, 60)
    (hours, remainder_minutes) = divmod(minutes, 60)
    (days, remainder_hours) = divmod(hours, 24)

    # Return
    result = ('%.f Days, %d:%02d:%02d') % (
        days, remainder_hours, remainder_minutes, remainder_seconds)
    return result


class _Display(object):
    """Class that creates the device's various HTML tables."""

    def __init__(self):
        """Initialize the class.

        Args:
            None

        Returns:
            None

        """
        # Get configuration
        config = CONFIG
        mac_address_file = config.mac_address_file()
        self.oui = {}

        # Read file
        with open(mac_address_file, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=':')
            for row in spamreader:
                mac_address = row[0]
                manufacturer = row[1]
                self.oui[mac_address] = manufacturer

        # Read ARP, RARP tables
        self.rarp_table = general.read_yaml_file(config.rarp_file())
        self.arp_table = general.read_yaml_file(config.arp_file())

    def html(self, mac_addresses):
        """Create list of dicts of MAC, host, manufacturer, IP address.

        Args:
            mac_addresses

        Returns:
            oui: OUI dictionary

        """
        # Initialize key variables
        listing = self._listing(mac_addresses)
        html_manufacturer = ''
        html_mac_address = ''
        html_ip_address = ''
        html_hostname = ''
        result = {}

        for item in listing:
            html_hostname = '{}<p>{}<p>'.format(
                html_hostname, item['hostname'])
            html_manufacturer = '{}<p>{}<p>'.format(
                html_manufacturer, item['manufacturer'])
            html_ip_address = '{}<p>{}<p>'.format(
                html_ip_address, item['ip_address'])

            if bool(item['mac_address']) is True:
                html_mac_address = '{}<p>{}<p>'.format(
                    html_mac_address, item['mac_address'])
            else:
                html_mac_address = ''

        # Return
        result['ip_address'] = html_ip_address
        result['hostname'] = html_hostname
        result['manufacturer'] = html_manufacturer
        result['mac_address'] = html_mac_address
        return result

    def _listing(self, mac_addresses):
        """Create list of dicts of MAC, host, manufacturer, IP address.

        Args:
            None

        Returns:
            oui: OUI dictionary

        """
        # Initialize key variables
        preliminary_listing = []
        listing = []

        # Cycle through mac addresses, get the manufacturer
        for mac_address in mac_addresses:
            # Get manufacturer
            manufacturer = self._manufacturer(mac_address)
            data_dict = {}
            data_dict['mac_address'] = mac_address
            data_dict['manufacturer'] = manufacturer
            preliminary_listing.append(data_dict)

        # Get IP address and hostname for each mac address
        for item in preliminary_listing:
            mac_address = item['mac_address']
            manufacturer = item['manufacturer']

            if mac_address in self.rarp_table:
                for ip_address in self.rarp_table[mac_address]:
                    data_dict = {}
                    data_dict['mac_address'] = mac_address
                    data_dict['manufacturer'] = manufacturer
                    data_dict['ip_address'] = ip_address
                    data_dict['hostname'] = ''

                    if ip_address in self.arp_table:
                        if 'hostname' in self.arp_table[ip_address]:
                            hostname = self.arp_table[ip_address]['hostname']
                            data_dict['hostname'] = hostname

                    listing.append(data_dict)

        # Return
        return listing

    def _manufacturer(self, mac_address):
        """Return manufacturer of MAC address' device.

        Args:
            mac_address: MAC address

        Returns:
            manufacturer: Name of manufacturer

        """
        # Initialize key variables
        manufacturer = ''

        # Process data
        mac_oui = mac_address[0:6]
        if mac_oui in self.oui:
            manufacturer = self.oui[mac_oui]

        # Return
        return manufacturer
