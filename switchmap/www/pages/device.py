#!usr/bin/env python3
"""Class for creating device web pages."""

import textwrap
import os

# PIP3 imports
from flask_table import Table, Col

# Import switchmap.libraries
from switchmap.utils import log
from switchmap.topology.translator import Translator


class _RawCol(Col):
    """Class that will just output whatever it is given and
    will not escape it.
    """

    def td_format(self, content):
        return content


class Device(object):
    """Class that creates the device's various HTML tables."""

    def __init__(self, config, host):
        """Initialize the class.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            None

        """
        # Initialize key variables
        self.default_action = False

        # Define default action
        if host.lower() == 'default':
            self.default_action = True

        # Process YAML file for host
        if self.default_action is False:
            translation = Translator(config, host)
            self.port_data = translation.ethernet_data()
            self.system_data = translation.system_summary()

    def ports(self):
        """Create the ports table for the device.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        if self.default_action is False:
            # Get data
            data = Port(self.port_data).data()

            # Populate the table
            table = PortTable(data)

            # Get HTML
            html = table.__html__()
        else:
            html = ''

        # Return
        return html

    def system(self):
        """Create summary table for the devie.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        if self.default_action is False:
            # Get data
            data = System(self.system_data).data()

            # Populate the table
            table = SystemTable(data)

            # Get HTML
            html = table.__html__()
        else:
            html = ''

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
    cdp = Col('CDP')
    lldp = Col('LLDP')

    # Define the CSS class to use for the header row
    thead_classes = ['tblHead']
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

    def __init__(
            self, port, vlan, state,
            days_inactive, speed, duplex, label, trunk, cdp, lldp):
        """Method initializing the class.

        Args:
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

        Returns:
            None

        """
        # Initialize key variables
        self.port = port
        self.vlan = vlan
        self.state = state
        self.days_inactive = days_inactive
        self.speed = speed
        self.duplex = duplex
        self.label = label
        self.trunk = trunk
        self.cdp = cdp
        self.lldp = lldp

    def active(self):
        """Active ports."""
        return bool(self.state == 'Active')

    def enabled(self):
        """Enabled ports."""
        return bool(self.state != 'Disabled')


class Port(object):
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, device_data):
        """Return whether port is enabled.

        Args:
            device_data: Dictionary of device data

        Returns:
            None

        """
        # Initialize key variables
        self.device_data = device_data

    def data(self):
        """Return data for the device's ports.

        Args:
            None

        Returns:
            rows: List of Col objects

        """
        # Initialize key variables
        rows = []

        # Create rows of data
        for _, port_data in sorted(self.device_data.items()):
            # Assign values for Ethernet ports only
            name = port_data['ifName']
            label = port_data['ifAlias']

            # Get port data
            port = _Port(port_data)
            speed = port.speed()
            inactive = port.inactive()
            vlan = port.vlan()
            state = port.state()
            duplex = port.duplex()
            trunk = port.trunk()
            cdp = port.cdp()
            lldp = port.lldp()

            # Append row of data
            rows.append(PortRow(
                name, vlan, state, inactive, speed, duplex,
                label, trunk, cdp, lldp))

        # Return
        return rows


class _Port(object):
    """Class that creates the data to be presented for the device's ports."""

    def __init__(self, port_data):
        """Return whether port is enabled.

        Args:
            device_data: Dictionary of device data

        Returns:
            None

        """
        # Initialize key variables
        self.port_data = port_data

    def trunk(self):
        """Return string for trunk status of port.

        Args:
            None

        Returns:
            trunk: Trunk state

        """
        # Assign key variables
        trunk = ''
        port_data = self.port_data

        # Get trunk string
        if bool(port_data['jm_trunk']) is True:
            trunk = 'Trunk'

        # Return
        return trunk

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

    def inactive(self):
        """Return days inactive for port.

        Args:
            None

        Returns:
            inactive: Days the port has been inactive

        """
        # Return
        return 'TBD'

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
            value = ('%s, %s, %s') % (
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
            value = ('<p>%s<br>%s<br>%s</p>') % (
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
        """Return whether port is enabled.

        Args:
            data_dict: Dictionary of device data

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


def create(config, host):
    """Create topology page for host.

    Args:
        config: Configuration object
        host: Hostname to create pages for

    Returns:
        None

    """
    # Initialize key variables
    device_file_found = False
    html = ''

    # Define default action
    if host.lower() == 'default':
        return html

    # Skip if device file not found
    if os.path.isfile(config.topology_device_file(host)) is False:
        log_message = (
            'No YAML device file for host %s found in %s. '
            'topoloy agent has not discovered it yet.'
            '') % (host, config.cache_directory())
        log.log2debug(1018, log_message)
    else:
        device_file_found = True

    # Process information for host
    if device_file_found is True:
        # Create HTML output
        table = Device(config, host)
        html = '{}\n<br>\n{}'.format(table.system(), table.ports())

    # Return
    return html
