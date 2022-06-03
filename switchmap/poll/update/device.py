"""Class for aggregating all necessary device data."""

# Standard imports
import os
from copy import deepcopy
import time

# Switchmap-NG imports
from switchmap import CONFIG
from switchmap.poll.snmp import poller
from switchmap.utils import general
from switchmap.utils import log


class IdleTimes():
    """Process device port idle times."""

    def __init__(self, devicename):
        """Initialize class.

        Args:
            devicename: Name of device to calculate idle times

        Returns:
            None

        """
        # Initialize key variables
        self._config = CONFIG
        self._device_dict = {}
        self._devicename = devicename

        # Log message
        log_message = (
            'Starting port idle times for device {}.'.format(devicename))
        log.log2debug(1034, log_message)

        # Read file and add to string
        filepath = self._config.temp_topology_device_file(devicename)
        if os.path.isfile(filepath) is True:
            self._device_dict = general.read_yaml_file(filepath)

    def save(self):
        """Save the idle times to file.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        device_dict = self._device_dict
        idle_history = {}
        idle_since = {}

        # Do nothing if no file found
        if bool(device_dict) is False:
            # Send log message
            log_message = (
                'No topology file found for device {}'
                ''.format(self._devicename))
            log.log2info(1058, log_message)
            return

        # Get all the status of all the Ethernet ports
        idle_since = _idle_since(device_dict)

        # Read data from idle file
        idle_filepath = (
            '{}/{}.yaml'.format(
                self._config.idle_directory(), self._devicename)
            )
        if os.path.isfile(idle_filepath) is True:
            idle_history = general.read_yaml_file(idle_filepath)

        # Update idle_since values depending on history
        for ifindex, timestamp in idle_since.items():
            if ifindex in idle_history:
                # Initialize key variables
                timestamp_historical = idle_history[ifindex]

                if bool(timestamp) is False:
                    # Do nothing if the timestamp is None
                    # Interface is operational
                    pass
                else:
                    if bool(timestamp_historical) is True:
                        # Update history value
                        idle_since[ifindex] = min(
                            timestamp, timestamp_historical)
                    else:
                        # Do nothing. Use current idle_since value
                        pass

        # Update idle_since file
        general.create_yaml_file(idle_since, idle_filepath)

        # Log message
        log_message = (
            'Completed port idle times for device {}.'
            ''.format(self._devicename))
        log.log2debug(1042, log_message)


class Device():
    """Process data for a device.

    The aim of this class is to process the YAML file consistently
    across multiple manufacturers and present it to other classes
    consistently. That way manufacturer specific code for processing YAML
    data is in one place.

    For example, there isn't a standard way of reporting ethernet duplex
    values with different manufacturers exposing this data to different MIBs.
    This class file attempts to determine the true duplex value of the
    device by testing the presence of one or more OID values in the data.
    It adds a 'duplex' data key to self.ports to act as the canonical key for
    duplex across all devices.

    """

    def __init__(self, data):
        """Initialize class.

        Args:
            data: Dict of device data

        Returns:
            None

        """
        # Initialize key variables
        self._devicename = data['misc']['host']
        self._data = deepcopy(data)

    def process(self):
        """Initialize class.

        Args:
            None

        Returns:
            None

        Summary:

            IF-MIB

            A significant portion of this code relies on ifIndex
            IF-MIB::ifStackStatus information. This is stored under the
            'system' key of the device YAML files.

            According to the official IF-MIB file. ifStackStatus is a
            "table containing information on the relationships
            between the multiple sub-layers of network interfaces.  In
            particular, it contains information on which sub-layers run
            'on top of' which other sub-layers, where each sub-layer
            corresponds to a conceptual row in the ifTable.  For
            example, when the sub-layer with ifIndex value x runs over
            the sub-layer with ifIndex value y, then this table
            contains:

              ifStackStatus.x.y=active

            For each ifIndex value, I, which identifies an active
            interface, there are always at least two instantiated rows
            in this table associated with I.  For one of these rows, I
            is the value of ifStackHigherLayer; for the other, I is the
            value of ifStackLowerLayer.  (If I is not involved in
            multiplexing, then these are the only two rows associated
            with I.)

            For example, two rows exist even for an interface which has
            no others stacked on top or below it:

              ifStackStatus.0.x=active
              ifStackStatus.x.0=active"

            In the case of Juniper equipment, VLAN information is only
            visible on subinterfaces of the main interface. For example
            interface ge-0/0/0 won't have VLAN information assigned to it
            directly.

            When a VLAN is assigned to this interface, a subinterface
            ge-0/0/0.0 is automatically created with a non-Ethernet ifType.
            VLAN related OIDs are only maintained for this new subinterface
            only. This makes determining an interface's VLAN based on
            Ethernet ifType more difficult. ifStackStatus maps the ifIndex of
            the primary interface (ge-0/0/0) to the ifIndex of the secondary
            interface (ge-0/0/0.0) which manages higher level protocols and
            data structures such as VLANs and LLDP.

            The primary interface is referred to as the
            ifStackLowerLayer and the secondary subinterface is referred to
            as the ifStackHigherLayer.

            =================================================================

            Layer1 Keys

            The following Layer1 keys are presented by the ethernet_data
            method due to this instantiation:

            jm_nativevlan: A vendor agnostic Native VLAN
            jm_vlan: A list of vendor agnostic VLANs
            jm_trunk: A vendor agnostic flag of "True" if the port is a Trunk
            jm_duplex: A vendor agnostic status code for the duplex setting

        """
        # Initialize key variables
        updated_device_data = deepcopy(self._data)
        layer1_data = updated_device_data['layer1']

        # Send log message
        log_message = (
            'Processing data from host {}'.format(self._devicename))
        log.log2debug(1028, log_message)

        # Create dict for layer1 Ethernet data
        for ifindex, _port_data in sorted(layer1_data.items()):
            # Make a copy of the port data to reduce the risk of corruption
            port_data = deepcopy(_port_data)

            # Process port_data
            if _is_ethernet(port_data) is True:
                # Update Ethernet status
                port_data['jm_ethernet'] = True

                # Get the ifIndex of the lower layer interface
                ifstacklowerlayer = ifindex

                #############################################################
                #
                # This stuff relies on ifstacklowerlayer / ifstackhigherlayer
                #
                #############################################################
                # Determine the ifIndex for any existing higher
                # layer subinterfaces whose data could be used
                # for upper layer2 features such as VLANs and
                # LAG trunking
                higherlayers = updated_device_data[
                    'system']['IF-MIB']['ifStackStatus'][ifindex]

                # Update vlan to universal switchmap.port_data value
                for ifstackhigherlayer in higherlayers:
                    # This is an Ethernet port with no higher level
                    # interfaces. Use lower level ifIndex
                    if bool(ifstackhigherlayer) is False:
                        (port_data['jm_vlan'],
                         port_data['jm_nativevlan'],
                         port_data['jm_trunk']) = _process_non_trunk(
                             layer1_data[ifstacklowerlayer])

                    else:
                        (port_data['jm_vlan'],
                         port_data['jm_nativevlan'],
                         port_data['jm_trunk']) = _process_trunk(
                             layer1_data[ifstackhigherlayer], higherlayers)

                #############################################################
                #
                # This stuff relies on ifindex
                #
                #############################################################

                # Update duplex to universal switchmap.port_data value
                port_data['jm_duplex'] = _duplex(deepcopy(port_data))

            else:
                # Update Ethernet status
                port_data['jm_ethernet'] = False

            # Update the data
            updated_device_data['layer1'][ifindex] = port_data

        # Send log message
        log_message = (
            'Completed processing data from host {}'.format(self._devicename))
        log.log2debug(1029, log_message)

        # Return
        return updated_device_data

    def save(self):
        """Create the master dictionary for the host.

        Args:
            None
        Returns:
            value: Index value

        """
        # Initialize key variables
        temp_dir = CONFIG.temp_topology_directory()
        temp_file = ('{}/{}.yaml'.format(temp_dir, self._devicename))

        # Add additional switchmap-ng specific fields to the dict
        data = self.process()
        yaml_string = general.dict2yaml(data)

        # Dump data
        with open(temp_file, 'w') as file_handle:
            file_handle.write(yaml_string)

        # Get data
        log_message = ('''\
Completed topology query from host {}.'''.format(self._devicename))
        log.log2info(1077, log_message)


def _process_non_trunk(port_data):
    """Assign trunk values to the non trunk Ethernet port.

    Args:
        port_data: Data dict related to the port

    Returns:
        result: Tuple of (vlan, nativevlan, trunk) for the port

    """
    # Return trunk values for non trunk ports
    vlan = _vlan(port_data)
    nativevlan = _nativevlan(port_data)
    trunk = _trunk(port_data)
    result = (vlan, nativevlan, trunk)
    return result


def _process_trunk(port_data, higherlayers):
    """Assign trunk values to the trunk Ethernet port.

    Args:
        port_data: Data dict related to the port
        higherlayers: Number of layers above the current port

    Returns:
        result: Tuple of (vlan, nativevlan, trunk) for the port

    """
    # Assign native VLAN to higher layer
    nativevlan = _nativevlan(port_data)

    # Update trunk status to universal port_data value
    trunk = _trunk(port_data)

    # This is an Ethernet port with a single higher level
    # interface
    if len(higherlayers) == 1:
        vlan = _vlan(port_data)

    # This is an Ethernet port with multiple higher level
    # interfaces
    else:
        vlan = _vlan(port_data)
        if 'jm_vlan' in port_data:
            vlan.extend(vlan)
        else:
            vlan = vlan

    # Return trunk values for non trunk ports
    result = (vlan, nativevlan, trunk)
    return result


def _juniper_fix(device_data):
    """Assign layer 1 values to the correct Ethernet port.

    Args:
        device_data: Data dict related to the device

    Returns:
        result: Result of assignments

    """
    # Initialize key variables
    source = deepcopy(device_data)
    result = deepcopy(device_data)
    valid = False

    # Send log message
    devicename = source['misc']['host']
    log_message = (
        'Starting data fixup of host {}'.format(devicename))
    log.log2debug(1031, log_message)

    # Get ifStackStatus data
    if 'system' in source:
        if 'IF-MIB' in source['system']:
            if 'ifStackStatus' in source['system']['IF-MIB']:
                valid = True

    # Return if not valid
    if valid is False:
        # Send log message
        devicename = source['misc']['host']
        log_message = (
            'Completed data fixup of host {}'.format(devicename))
        log.log2debug(1032, log_message)
        return result

    # Get a list of ifIndex values to Process
    status_values = source['system']['IF-MIB']['ifStackStatus']

    # Get the ones that are non Ethernet and have Ethernet parents
    for parent, children in status_values.items():
        for child in children:
            if bool(child) is False:
                continue
            else:
                # Copy key values from child to parent
                if source['layer1'][parent]['ifType'] == 6:
                    for parameter, value in source['layer1'][child].items():
                        if parameter not in result['layer1'][parent]:
                            result['layer1'][parent][parameter] = value

    # Send log message
    devicename = source['misc']['host']
    log_message = (
        'Completed data fixup of host {}'.format(devicename))
    log.log2debug(1033, log_message)

    # Return
    return result


def _is_ethernet(port_data):
    """Return whether ifIndex port_data belongs to an Ethernet port.

    Args:
        port_data: Data dict related to the port

    Returns:
        valid: True if valid ethernet port

    """
    # Initialize key variables
    valid = False

    # Process ifType
    if 'ifType' in port_data:
        # Get port name
        name = port_data['ifName'].lower()

        # Process ethernet ports
        if port_data['ifType'] == 6:
            # VLAN L2 VLAN interfaces passing as Ethernet
            if name.startswith('vl') is False:
                valid = True

    # Return
    return valid


def _vlan(port_data):
    """Return vlan for specific ifIndex.

    Args:
        port_data: Data dict related to the port port

    Returns:
        vlans: VLAN number

    """
    # Initialize key variables
    vlans = None

    # Determine vlan number for Cisco devices (Older models)
    if 'vmVlan' in port_data:
        vlans = [int(port_data['vmVlan'])]

    # Determine vlan number for Cisco devices (Newer models)
    if 'vlanTrunkPortVlansEnabled' in port_data:
        if isinstance(port_data['vlanTrunkPortVlansEnabled'], list) is True:
            vlans = port_data['vlanTrunkPortVlansEnabled']
        else:
            vlans = [int(port_data['vlanTrunkPortVlansEnabled'])]

    # Determine vlan number for Cisco devices (Router trunk subinterfaces)
    if 'cviRoutedVlanIfIndex' in port_data:
        vlans = port_data['cviRoutedVlanIfIndex']

    # Determine vlan number for Juniper devices
    if 'jnxExVlanTag' in port_data:
        tags = port_data['jnxExVlanTag']
        if bool(tags) is True:
            vlans = tags

    # Return
    return vlans


def _nativevlan(port_data):
    """Return vlan for specific ifIndex.

    Args:
        port_data: Data dict related to the port
        ifindex: ifindex in question

    Returns:
        vlan: VLAN number

    """
    # Initialize key variables
    vlan = None

    # Determine native VLAN tag number for Cisco devices
    if 'vlanTrunkPortNativeVlan' in port_data:
        vlan = int(port_data['vlanTrunkPortNativeVlan'])

    # Determine native VLAN tag number for Juniper devices
    if 'dot1qPvid' in port_data:
        vlan = port_data['dot1qPvid']

    # Return
    return vlan


def _duplex(port_data):
    """Return duplex value for port.

    Args:
        port_data: Data dict related to the port

    Returns:
        duplex: Duplex value
            0) Unknown
            1) Half
            2) Full
            3) Half Auto
            4) Full Auto

    """
    # Initialize key variables
    duplex = 0

    value = ''

    statuses = ('swPortDuplexStatus',
                'dot3StatsDuplexStatus',
                'portDuplex')

    def get_duplex_value(status, val):
        """Return duplex value based on port status.

        Args:
            status: The status of the port
            value: The value of the port status

        Returns:
            value: Duplex value

        """
        cases = {
            'swPortDuplexStatus': 2 if val == 1 else 1,
            'dot3StatsDuplexStatus': 1 if val == 2 else (2 if val == 3 else 0),
            'portDuplex': 1 if val == 1 else (2 if val == 2 else 0),
        }

        return cases[status]

    for status in statuses:
        if status in port_data:
            value = port_data[status]
            duplex = get_duplex_value(status, value)
            break

    # Process c2900PortDuplexState
    # The Cisco 3500XL is known to report incorrect duplex values.
    # Obsolete device, doesn't make sense supporting it.
    if not duplex and 'c2900PortLinkbeatStatus' in port_data:
        status_link = port_data['c2900PortLinkbeatStatus']
        status_duplex = port_data['c2900PortDuplexStatus']

        if status_link == 3:
            # If no link beats (Not AutoNegotiate)
            if status_duplex == 1:
                duplex = 2
            elif status_duplex == 2:
                duplex = 1
        else:
            # If link beats (AutoNegotiate)
            if status_duplex == 1:
                duplex = 4
            elif status_duplex == 2:
                duplex = 3

    # Return
    return duplex


def _trunk(port_data):
    """Return trunk for specific ifIndex.

    Args:
        port_data: Data dict related to the port

    Returns:
        trunk: True if port is in trunking mode

    """
    # Initialize key variables
    trunk = False

    # Determine if trunk for Cisco devices
    if 'vlanTrunkPortDynamicStatus' in port_data:
        if port_data['vlanTrunkPortDynamicStatus'] == 1:
            trunk = True

    # Determine if trunk for Juniper devices
    if 'jnxExVlanPortAccessMode' in port_data:
        if port_data['jnxExVlanPortAccessMode'] == 2:
            trunk = True

    # Return
    return trunk


def _idle_since(device_dict):
    """Get .

    Args:
        device_dict: Device information dictionary

    Returns:
        idle_since: Dict of idle since values per port

    """
    # Initialize key variables
    idle_since = {}

    # Get all the status of all the Ethernet ports
    if 'layer1' in device_dict:
        for ifindex, data_dict in device_dict['layer1'].items():
            if 'jm_ethernet' in data_dict:
                if data_dict['jm_ethernet'] is True:
                    if (data_dict['ifOperStatus'] == 1) and (
                            data_dict['ifAdminStatus'] == 1):
                        idle_since[ifindex] = None
                    else:
                        idle_since[ifindex] = int(time.time())
    # Return
    return idle_since
