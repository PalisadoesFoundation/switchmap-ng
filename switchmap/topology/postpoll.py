#!/usr/bin/env python3
"""Class for normalizing the data read from YAML files."""

# Standard imports
import os
from copy import deepcopy
import time

# Switchmap-NG imports
from switchmap.constants import CONFIG
from switchmap.utils import general
from switchmap.utils import log


def all_devices():
    """Add IP address and Hostname data to device files.

    Args:
        None

    Returns:
        None

    """
    # Add Layer3 information
    _layer3()

    # Add port idle information
    _idle()


def _idle():
    """Add ifindex idle information.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    config = CONFIG
    idle_history = {}

    # Send log message
    log_message = ('Evaluating port idle times for devices.')
    log.log2info(1069, log_message)

    # Cycle through list of files in directory
    for filename in os.listdir(config.temp_topology_directory()):
        # Initialize idle dictionary
        idle_since = {}

        # Examine all the '.yaml' files in directory
        if filename.endswith('.yaml'):
            devicename = filename[0:-5]

            # Log message
            log_message = (
                'Starting port idle times for device {}.'.format(devicename))
            log.log2debug(1034, log_message)

            # Read file and add to string
            filepath = config.temp_topology_device_file(devicename)
            device_dict = general.read_yaml_file(filepath)

            # Get all the status of all the Ethernet ports
            if 'layer1' in device_dict:
                for ifindex, data_dict in device_dict['layer1'].items():
                    if 'jm_ethernet' in data_dict:
                        if data_dict['jm_ethernet'] is True:
                            idle_since[ifindex] = int(time.time())
                            if data_dict['ifOperStatus'] == 1:
                                if data_dict['ifAdminStatus'] == 1:
                                    idle_since[ifindex] = None

            # Read data from idle file
            idle_filepath = (
                '{}/{}.yaml'.format(config.idle_directory(), devicename)
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
                'Completed port idle times for device {}.'.format(devicename))
            log.log2debug(1042, log_message)

    # Send log message
    log_message = ('Completed port idle times for devices.')
    log.log2info(1058, log_message)


def _layer3():
    """Add IP address and Hostname data to device files.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    ifindex_ip_found = False
    ifindex_hostname_found = False
    config = CONFIG

    # Send log message
    log_message = ('Starting Layer3 updates of device files.')
    log.log2info(1045, log_message)

    # Read ARP, RARP tables
    rarp_table = general.read_yaml_file(config.rarp_file())
    hosts_table = general.read_yaml_file(config.hosts_file())

    # Cycle through list of files in directory
    for filename in os.listdir(config.temp_topology_directory()):
        # Examine all the '.yaml' files in directory
        if filename.endswith('.yaml'):
            devicename = filename[0:-5]

            # Log message
            log_message = (
                'Starting Layer3 updates for device {}.'.format(devicename))
            log.log2debug(1046, log_message)

            # Read file and add to string
            filepath = config.temp_topology_device_file(devicename)
            device_dict = general.read_yaml_file(filepath)

            # Update dict with values
            loop_dict = deepcopy(device_dict)

            # Populate ifIndex table
            if 'layer1' in loop_dict:
                layer1_dict = device_dict['layer1']
                # Process each port on device
                for ifindex, port_dict in layer1_dict.items():
                    # Only interested in Ethernet ports
                    if bool(port_dict['jm_ethernet']) is False:
                        continue

                    # We are not interested in populating trunk port MAC data
                    if bool(port_dict['jm_trunk']) is True:
                        continue

                    # Try to update jm_ip and jm_hostname
                    if 'jm_macs' in port_dict:
                        for mac_address in port_dict['jm_macs']:
                            if mac_address in rarp_table:
                                # Get the list of RARP IP addresses
                                ifindex_ips = rarp_table[mac_address]

                                # Only process RARP entries with an IP
                                if bool(ifindex_ips) is True:
                                    device_dict['layer1'][ifindex][
                                        'jm_ip'] = ifindex_ips[0]
                                    ifindex_ip_found = True
                                    break

                        # Set a precautionary value for 'jm_ip'
                        if ifindex_ip_found is False:
                            device_dict['layer1'][ifindex]['jm_ip'] = ''
                        # Attempt to find a hostname
                        else:
                            # A MAC can be assigned to many IP addresses
                            # We check to see whether and of these IP addresses
                            # has a DNS entry
                            for hostname, key in hosts_table.items():
                                # This indicates we have found a match in the
                                # hosts file
                                if key in ifindex_ips:
                                    # Assign values to a meaningful
                                    # IP / hostname pair
                                    device_dict['layer1'][ifindex][
                                        'jm_hostname'] = hostname
                                    device_dict['layer1'][ifindex][
                                        'jm_ip'] = key
                                    ifindex_hostname_found = True
                                    break

                        # Set a precautionary value for 'jm_ip'
                        if ifindex_hostname_found is False:
                            device_dict['layer1'][ifindex]['jm_hostname'] = ''

                    # Reset values
                    ifindex_ip_found = False
                    ifindex_hostname_found = False

            # Write updated file back
            general.create_yaml_file(device_dict, filepath)

            # Log message
            log_message = (
                'Completed Layer3 updates for device {}.'.format(devicename))
            log.log2debug(1044, log_message)

    # Send log message
    log_message = ('Completed Layer3 updates of device files.')
    log.log2info(1047, log_message)


class Process(object):
    """Process data polled from a device.

    The aim of this class is to process the YAML file consistently
    across multiple manufacturers and present it to other classes
    consistently. That way manufacturer specific code for processing YAML
    data is in one place.

    For example, there isn’t a standard way of reporting ethernet duplex
    values with different manufacturers exposing this data to different MIBs.
    This class file attempts to determine the true duplex value of the
    device by testing the presence of one or more OID values in the data.
    It adds a ‘duplex’ data key to self.ports to act as the canonical key for
    duplex across all devices.

    """

    def __init__(self, input_data, oui):
        """Initialize class.

        Args:
            input_data: Recently polled device data to processs
            oui: OUI data for lookups

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
        # Send log message
        devicename = input_data['misc']['host']
        log_message = (
            'Processing data from host {}'.format(devicename))
        log.log2debug(1028, log_message)

        # Fix known issues with Juniper devices where certain layer 1
        # parameters such as MAC addresses are assigned to virtual
        # non Ethernet ifIndex values.
        updated_device_data = _fixup(input_data)
        device_data = deepcopy(updated_device_data)

        # Create dict for layer1 Ethernet data
        for ifindex, layer1_data in device_data['layer1'].items():
            updated_layer1_data = deepcopy(layer1_data)
            # Process layer1_data
            if _is_ethernet(layer1_data) is True:
                # Update Ethernet status
                updated_layer1_data['jm_ethernet'] = True

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
                higherlayers = device_data[
                    'system']['IF-MIB']['ifStackStatus'][ifindex]

                # Update vlan to universal switchmap.layer1_data value
                for ifstackhigherlayer in higherlayers:
                    # This is an Ethernet port with no higher level
                    # interfaces. Use lower level ifIndex
                    if bool(ifstackhigherlayer) is False:
                        updated_layer1_data['jm_vlan'] = _vlan(
                            deepcopy(device_data), ifstacklowerlayer)

                        updated_layer1_data['jm_nativevlan'] = _nativevlan(
                            deepcopy(device_data), ifstacklowerlayer)

                        updated_layer1_data['jm_trunk'] = _trunk(
                            deepcopy(device_data), ifstacklowerlayer)
                    else:
                        # Assign native VLAN to higer layer
                        updated_layer1_data['jm_nativevlan'] = _nativevlan(
                            deepcopy(device_data), ifstackhigherlayer)

                        # Update trunk status to universal layer1_data value
                        updated_layer1_data['jm_trunk'] = _trunk(
                            deepcopy(device_data), ifstackhigherlayer)

                        # This is an Ethernet port with a single higher level
                        # interface
                        if len(higherlayers) == 1:
                            updated_layer1_data['jm_vlan'] = _vlan(
                                deepcopy(device_data), ifstackhigherlayer)
                        # This is an Ethernet port with multiple higher level
                        # interfaces
                        else:
                            updated_layer1_data['jm_vlan'].extend(
                                _vlan(
                                    deepcopy(device_data), ifstackhigherlayer))

                #############################################################
                #
                # This stuff relies on ifindex
                #
                #############################################################

                # Update duplex to universal switchmap.layer1_data value
                updated_layer1_data['jm_duplex'] = _duplex(
                    deepcopy(layer1_data))

                # Update manufacturer of MAC
                updated_layer1_data['jm_manufacturer'] = _manufacturer(
                    deepcopy(layer1_data), oui)

            else:
                # Update Ethernet status
                updated_layer1_data['jm_ethernet'] = False

            # Update the data
            new_layer1_data = deepcopy(updated_layer1_data)
            updated_device_data['layer1'][ifindex] = new_layer1_data

        # Done
        self.data = updated_device_data

        # Send log message
        log_message = (
            'Completed processing data from host {}'.format(devicename))
        log.log2debug(1029, log_message)

    def augmented_data(self):
        """Return updated data.

        Args:
            None

        Returns:
            data_dict: Dict of summary data

        """
        # Return
        return self.data


def _fixup(device_data):
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


def _is_ethernet(layer1_data):
    """Return whether ifIndex layer1_data belongs to an Ethernet port.

    Args:
        layer1_data: Data dict related to the port

    Returns:
        valid: True if valid ethernet port

    """
    # Initialize key variables
    valid = False

    # Process ifType
    if 'ifType' in layer1_data:
        # Get port name
        name = layer1_data['ifName'].lower()

        # Process ethernet ports
        if layer1_data['ifType'] == 6:
            # VLAN L2 VLAN interfaces passing as Ethernet
            if name.startswith('vl') is False:
                valid = True

    # Return
    return valid


def _vlan(layer1_data, ifindex):
    """Return vlan for specific ifIndex.

    Args:
        layer1_data: Data dict related to the device
        ifindex: ifindex in question

    Returns:
        vlans: VLAN number

    """
    # Initialize key variables
    vlans = None

    # Failsafe
    if ifindex not in layer1_data['layer1']:
        return vlans

    # Determine vlan number for Cisco devices
    if 'vmVlan' in layer1_data['layer1'][ifindex]:
        vlans = [int(layer1_data['layer1'][ifindex]['vmVlan'])]

    # Determine vlan number for Juniper devices
    if 'jnxExVlanTag' in layer1_data['layer1'][ifindex]:
        tags = layer1_data['layer1'][ifindex]['jnxExVlanTag']
        if bool(tags) is True:
            vlans = tags

    # Return
    return vlans


def _nativevlan(layer1_data, ifindex):
    """Return vlan for specific ifIndex.

    Args:
        layer1_data: Data dict related to the device
        ifindex: ifindex in question

    Returns:
        vlan: VLAN number

    """
    # Initialize key variables
    vlan = None

    # Failsafe
    if ifindex not in layer1_data['layer1']:
        return vlan

    # Determine native VLAN tag number for Cisco devices
    if 'vlanTrunkPortNativeVlan' in layer1_data['layer1'][ifindex]:
        vlan = int(layer1_data['layer1'][ifindex]['vlanTrunkPortNativeVlan'])

    # Determine native VLAN tag number for Juniper devices
    if 'dot1qPvid' in layer1_data['layer1'][ifindex]:
        vlan = layer1_data['layer1'][ifindex]['dot1qPvid']

    # Return
    return vlan


def _duplex(layer1_data):
    """Return duplex value for port.

    Args:
        layer1_data: Data dict related to the port

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
        if status in layer1_data:
            value = layer1_data[status]
            duplex = get_duplex_value(status, value)
            break

    # Process c2900PortDuplexState
    # The Cisco 3500XL is known to report incorrect duplex values.
    # Obsolete device, doesn't make sense supporting it.
    if not duplex and 'c2900PortLinkbeatStatus' in layer1_data:
        status_link = layer1_data['c2900PortLinkbeatStatus']
        status_duplex = layer1_data['c2900PortDuplexStatus']

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


def _trunk(layer1_data, ifindex):
    """Return trunk for specific ifIndex.

    Args:
        layer1_data: Data dict related to the device
        ifindex: ifindex in question

    Returns:
        trunk: True if port is in trunking mode

    """
    # Initialize key variables
    trunk = False

    # Failsafe
    if ifindex not in layer1_data['layer1']:
        return trunk

    # Determine if trunk for Cisco devices
    if 'vlanTrunkPortDynamicStatus' in layer1_data['layer1'][ifindex]:
        if layer1_data['layer1'][ifindex]['vlanTrunkPortDynamicStatus'] == 1:
            trunk = True

    # Determine if trunk for Juniper devices
    if 'jnxExVlanPortAccessMode' in layer1_data['layer1'][ifindex]:
        if layer1_data['layer1'][ifindex]['jnxExVlanPortAccessMode'] == 2:
            trunk = True

    # Return
    return trunk


def _manufacturer(layer1_data, oui):
    """Return manufacturer of MAC address' device.

    Args:
        layer1_data: Data dict related to the port
        oui: OUI dict {oui, manufacturer}

    Returns:
        manufacturer: Name of manufacturer

    """
    # Initialize key variables
    manufacturer = ''

    # Process data
    if 'jm_macs' in layer1_data:
        if bool(layer1_data['jm_macs']) is True:
            jm_macs = layer1_data['jm_macs']
            if len(jm_macs) == 1:
                mac_oui = jm_macs[0][0:6]
                if mac_oui in oui:
                    manufacturer = oui[mac_oui]

    # Return
    return manufacturer
