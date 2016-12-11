#!usr/bin/env python3
"""Class for creating device web pages."""

import tempfile
import textwrap
import os

# Import switchmap.libraries
from switchmap.utils import log
from switchmap.utils import general
from switchmap.topology.translator import Translator


class HTMLTable(object):
    """Class that creates the device's various HTML tables.

    Methods:
        ethernet: Table of device Ethernet ports
        device: Summary HTML table

    """

    def __init__(self, config, host):
        """Initialize the class.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            None

        """
        # Process YAML file for host
        translation = Translator(config, host)
        self.ports = translation.ethernet_data()
        self.summary = translation.system_summary()

    def ethernet(self):
        """Create the ports table for the device.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        html = _port_table(self.ports)

        # Return
        return html

    def device(self):
        """Create summary table for the devie.

        Args:
            config: Configuration object
            host: Hostname to process

        Returns:
            html: HTML table string

        """
        # Initialize key variables
        html = _device_table(self.summary)

        # Return
        return html


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

    # Create directory if needed
    temp_dir = tempfile.mkdtemp()

    # Delete all files in temporary directory
    general.delete_files(temp_dir)

    # Skip if device file not found
    if os.path.isfile(config.topology_device_file(host)) is False:
        log_message = (
            'No YAML device file for host %s found in %s. '
            'topoloy agent has not discovered it yet.'
            '') % (host, config.cache_directory())
        log.log2info(1018, log_message)
    else:
        device_file_found = True

    ####################################################################
    #
    # Define variables that will be required for the database update
    # We have to initialize the dict during every loop to prevent
    # data corruption
    #
    ####################################################################
    table = HTMLTable(config, host)

    # Create HTML output
    html = ('%s%s\n%s\n\n%s\n') % (
        _html_header(host), host, table.device(),
        table.ethernet())

    # Do the rest if device_file_found
    if device_file_found is True:
        # Wait on the queue until everything has been processed
        return html


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
        active: True if active

    """
    # Initialize key variables
    enabled = False

    # Assign state
    if _port_enabled(port_data) is True:
        if 'ifOperStatus' in port_data:
            if port_data['ifOperStatus'] == 1:
                enabled = True

    # Return
    return enabled


def _get_state(port_data):
    """Return port state string.

    Args:
        port_data: Data related to the port

    Returns:
        state: State string

    """
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


def _get_inactive():
    """Return days inactive for port.

    Args:
        port_data: Data related to the port

    Returns:
        inactive: Days the port has been inactive

    """
    # Return
    return 'TBD'


def _get_speed(port_data):
    """Return port speed.

    Args:
        port_data: Data related to the port

    Returns:
        speed: Port speed

    """
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


def _get_cdp(port_data):
    """Return port CDP HTML string.

    Args:
        port_data: Data related to the port

    Returns:
        value: required string

    """
    # Initialize key variables
    value = ''

    # Determine whether CDP is enabled and update string
    if 'cdpCacheDeviceId' in port_data:
        value = ('<p>%s<br>%s<br>%s</p>') % (
            port_data['cdpCacheDeviceId'],
            port_data['cdpCachePlatform'],
            port_data['cdpCacheDevicePort'])

    # Return
    return value


def _get_lldp(port_data):
    """Return port LLDP HTML string.

    Args:
        port_data: Data related to the port

    Returns:
        value: required string

    """
    # Initialize key variables
    value = ''

    # Determine whether LLDP is enabled and update string
    if 'lldpRemSysDesc' in port_data:
        value = ('<p>%s<br>%s<br>%s</p>') % (
            port_data['lldpRemSysName'],
            port_data['lldpRemPortDesc'],
            port_data['lldpRemSysDesc'])

    # Return
    return value


def _get_duplex(port_data):
    """Return port duplex string.

    Args:
        port_data: Data related to the port

    Returns:
        duplex: Duplex string

    """
    # Initialize key variables
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


def _get_vlan(port_data):
    """Return VLAN number.

    Args:
        port_data: Data related to the port

    Returns:
        vlans

    """
    # Initialize key variables
    vlans = 'N/A'

    # Assign VLAN
    if 'jm_trunk' in port_data:
        if port_data['jm_trunk'] is False:
            if 'jm_vlan' in port_data:
                if port_data['jm_vlan'] is not None:
                    values = [str(value) for value in port_data['jm_vlan']]
                    vlans = ' '.join(values)
        else:
            if 'jm_nativevlan' in port_data:
                vlans = str(port_data['jm_nativevlan'])

    # Return
    return vlans


def _html_footer():
    """Display HTML footer.

    Args:
        None

    Returns:
        html: HTML for footer

    """
    # Print footer
    html = ("""
</body>
</html>
""")
    return html


def _html_header(host):
    """Display HTML header.

    Args:
        host: Hostname

    Returns:
        html: HTML for header

    """
    # Print header
    html = ("""\
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="refresh" CONTENT="3600">
<META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">
<title>%s Ports List</title>
</head>
<body>
""") % (host)
    return html


def _port_table(data_dict):
    """Return table with port information.

    Args:
        data_dict: Dict of port data

    Returns:
        output: HTML code for table

    """
    # Initialize key variables
    rows = []
    header = [
        'Port', 'VLAN', 'State', 'Days Inactive',
        'Speed', 'Duplex', 'Port Label', 'CDP', 'LLDP']
    output = '<table class="table">\n'
    thstart = '    <th>'

    # Create header
    output = ('%s%s%s') % (
        output, thstart, (('</th>\n%s') % (thstart)).join(header))
    output = ('%s</th>') % (output)

    # Create rows of data
    for _, port_data in sorted(data_dict.items()):
        # Assign values for Ethernet ports only
        port = port_data['ifName']
        label = port_data['ifAlias']
        speed = _get_speed(port_data)
        inactive = _get_inactive()
        vlan = _get_vlan(port_data)
        state = _get_state(port_data)
        duplex = _get_duplex(port_data)
        cdp = _get_cdp(port_data)
        lldp = _get_lldp(port_data)
        rows.append(
            [port, vlan, state, inactive, speed, duplex, label, cdp, lldp])

    # Loop through list
    for row in rows:
        # Print entry row
        output = ('%s\n    <tr>\n        <td>') % (output)
        output = ('%s%s') % (output, '</td><td>'.join(row))
        output = ('%s</td>\n    </tr>') % (output)

    # Finish the table
    output = ('%s\n</table>') % (output)

    # Return
    return output


def _device_table(data_dict):
    """Return table with device information.

    Args:
        data_dict: Dict of device data

    Returns:
        output: HTML code for table

    """
    # Initialize key variables
    rows = []
    labels = ['sysName', 'sysDescr', 'sysObjectID', 'Uptime']
    values = [
        data_dict['sysName'],
        textwrap.fill(data_dict['sysDescr']).replace('\n', '<br>'),
        data_dict['sysObjectID'],
        _uptime(data_dict['sysUpTime'])
        ]
    output = '<table class="table">'

    # Create rows array
    for index, value in enumerate(values):
        rows.append([labels[index], str(value)])

    # Loop through list
    for row in rows:
        # Print entry row
        output = ('%s\n    <tr>\n        <td>') % (output)
        output = ('%s%s') % (output, '</td><td>'.join(row))
        output = ('%s</td>\n    </tr>') % (output)

    # Finish the table
    output = ('%s\n</table>') % (output)

    # Return
    return output


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
