#!/usr/bin/env python3
"""Class for normalizing the data read from YAML files."""

import os
import yaml


# Switchmap-NG imports
from switchmap.utils import log


class Translator(object):
    """Process configuration file for a host.

    The aim of this class is to process the YAML file consistently
    across multiple manufacturers and present it to other classes
    consistently. That way manufacturer specific code for processing YAML
    data is in one place.

    For example, there isn’t a standard way of reporting ethernet duplex
    values with different manufacturers exposing this data to different MIBs.
    This class file attempts to determine the true duplex value of the
    device by testing the presence of one or more OID values in the data.
    It adds a ‘duplex’ data key to self._ports to act as the canonical key for
    duplex across all devices.

    """

    def __init__(self, config, hostname):
        """Initialize class.

        Args:
            config: Configuration file object
            hostname: Hostname to process

        Returns:
            data_dict: Dict of summary data

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

            l1_nativevlan: A vendor agnostic Native VLAN
            l1_vlans: A list of vendor agnostic VLANs
            l1_trunk: A vendor agnostic flag of "True" if the port is a Trunk
            l1_duplex: A vendor agnostic status code for the duplex setting

        """
        # Initialize key variables
        self._ports = {}
        self._hostname = hostname
        yaml_file = config.topology_device_file(self._hostname)

        # Fail if yaml file doesn't exist
        if os.path.isfile(yaml_file) is False:
            log_message = (
                "YAML file {} for host {} doesn't exist! "
                "Try polling devices first.".format(yaml_file, self._hostname)
            )
            log.log2die(1017, log_message)

        # Read file
        with open(yaml_file, "r") as file_handle:
            yaml_from_file = file_handle.read()
        yaml_data = yaml.safe_load(yaml_from_file)

        # Create dict for layer1 Ethernet data
        for ifindex, metadata in yaml_data["layer1"].items():
            # Skip non Ethernet ports
            if "l1_ethernet" not in metadata:
                continue

            # Process metadata
            if bool(metadata["l1_ethernet"]) is True:
                # Update ports
                self._ports[int(ifindex)] = metadata

        # Get system
        self._system = yaml_data["system"]
        self._misc = yaml_data["misc"]

    def system_summary(self):
        """Return system summary data.

        Args:
            None

        Returns:
            data_dict: Dict of summary data

        """
        # Initialize key variables
        data_dict = {}

        # Assign system variables
        v2mib = self._system["SNMPv2-MIB"]
        for key in v2mib.keys():
            data_dict[key] = v2mib[key]["0"]

        # Add the hostname to the dictionary
        data_dict["hostname"] = self._hostname
        data_dict["timestamp"] = self._misc["timestamp"]

        # Return
        return data_dict

    def ethernet_data(self):
        """Return L1 data for Ethernet ports only.

        Args:
            None

        Returns:
            self._ports: L1 data for Ethernet ports

        """
        return self._ports
