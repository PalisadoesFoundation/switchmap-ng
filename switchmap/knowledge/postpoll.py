#!/usr/bin/env python3
"""Class for normalizing the data read from YAML files."""

from copy import deepcopy
from pprint import pprint

# Switchmap-NG imports


class Process(object):
    """Process configuration file for a host.

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

    def __init__(self, device_data):
        """Initialize class.

        Args:
            device_data: Recently polled device data to processs

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
        updated_device_data = deepcopy(device_data)

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
                for higherlayer in higherlayers:
                    # All numeric keys in YAML need to be strings. Prepare
                    # for key checking.
                    ifstackhigherlayer = str(higherlayer)

                    # This is an Ethernet port with no higher level
                    # interfaces. Use lower level ifIndex
                    if ifstackhigherlayer == '0':
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

            else:
                # Update Ethernet status
                updated_layer1_data['jm_ethernet'] = False

            # Update the data
            new_layer1_data = deepcopy(updated_layer1_data)
            updated_device_data['layer1'][ifindex] = new_layer1_data

        # Done
        self.data = updated_device_data

    def augmented_data(self):
        """Return updated data.

        Args:
            None

        Returns:
            data_dict: Dict of summary data

        """
        # Return
        return self.data


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
