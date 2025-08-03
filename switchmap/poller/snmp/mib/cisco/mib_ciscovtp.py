"""Class interacts with CISCO-VTP-MIB."""

from collections import defaultdict
import binascii

from switchmap.poller.snmp.base_query import Query
from switchmap.core import log
import asyncio


def get_query():
    """Return this module's Query class.

    Args:
        None

    Returns:
        CiscoVtpQuery: Query class object
    """
    return CiscoVtpQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class.

    Args:
        snmp_object: SNMP Interact class object from snmp_manager.py

    Returns:
        CiscoVtpQuery: Query class object
    """
    return CiscoVtpQuery(snmp_object)


class CiscoVtpQuery(Query):
    """Class interacts with CISCO-VTP-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        layer1: Returns all needed layer 1 MIB information from the device.
            Keyed by OID's MIB name (primary key), ifIndex (secondary key)

        layer2: Returns all needed layer 2 MIB information from the device.
            Keyed by OID's MIB name (primary key), VLAN number (secondary key)

    """

    def __init__(self, snmp_object):
        """Instantiate the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB (vtpVlanState)
        test_oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.2"

        super().__init__(snmp_object, test_oid, tags=["layer1", "layer2"])

    async def layer2(self):
        """Get layer 2 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Run all the Vtp queries concurrently

        results = await asyncio.gather(
            self.vtpvlanname(),
            self.vtpvlanstate(),
            self.vtpvlantype(),
            return_exceptions=True,
        )

        method_names = ["vtpVlanName", "vtpVlanState", "vtpVlanType"]

        for method_name, values in zip(method_names, results):
            if isinstance(values, Exception):
                continue

            if values:
                for key, value in values.items():
                    final[key][method_name] = value

        return final

    async def layer1(self):
        """Get layer 1 data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        final = defaultdict(lambda: defaultdict(dict))

        # Can Limit concurrent SNMP queries (can adjust according to need)
        semaphore = asyncio.Semaphore(10)

        async def limited_query(method, name):
            """Rate limit SNMP query."""
            async with semaphore:
                try:
                    return name, await method()
                except Exception as e:
                    log.log2warning(
                        1001, f"CISCO-VTP layer1 query failed: {name}: {e}"
                    )
                    return name, {}

        queries = [
            (self.vlantrunkportdynamicstate, "vlanTrunkPortDynamicState"),
            (self.vlantrunkportdynamicstatus, "vlanTrunkPortDynamicStatus"),
            (self.vlantrunkportnativevlan, "vlanTrunkPortNativeVlan"),
            (
                self.vlantrunkportencapsulationtype,
                "vlanTrunkPortEncapsulationType",
            ),
            (self.vlantrunkportvlansenabled, "vlanTrunkPortVlansEnabled"),
        ]

        # Execute all queries concurrently
        results = await asyncio.gather(
            *[limited_query(method, name) for method, name in queries],
            return_exceptions=True,
        )

        for result in results:
            if isinstance(result, Exception):
                continue

            method_name, values = result

            for key, value in values.items():
                final[key][method_name] = value

        return final

    async def vlantrunkportencapsulationtype(self, oidonly=False):
        """Return CISCO-VTP-MIB vlanTrunkPortEncapsulationType per ifIndex.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vlanTrunkPortEncapsulationType
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.3"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value
        
        print(f"result: {results}")
        # Return the interface descriptions
        return data_dict

    async def vlantrunkportnativevlan(self, oidonly=False):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortNativeVlan per ifIndex.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vlanTrunkPortNativeVlan
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.5"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    async def vlantrunkportdynamicstatus(self, oidonly=False):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicStatus per ifIndex.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vlanTrunkPortDynamicStatus
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.14"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    async def vlantrunkportdynamicstate(self, oidonly=False):
        """Return dict of CISCO-VTP-MIB vlanTrunkPortDynamicState per ifIndex.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vlanTrunkPortDynamicState
                using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.13"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    async def vtpvlanname(self, oidonly=False):
        """Return dict of CISCO-VTP-MIB vtpVlanName for each VLAN.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vtpVlanName using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.4"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = str(bytes(value), encoding="utf-8")

        # Return the interface descriptions
        return data_dict

    async def vtpvlantype(self, oidonly=False):
        """Return dict of CISCO-VTP-MIB vtpVlanType for each VLAN.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vtpVlanType using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.3"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            try:
                raw = value.asOctets()
            except AttributeError:
                raw = value if isinstance(value, (bytes, bytearray)) else None
            data_dict[int(key)] = (
                raw.decode("utf-8", errors="replace")
                if raw is not None
                else str(value)
            )

        # Return the interface descriptions
        return data_dict

    async def vtpvlanstate(self, oidonly=False):
        """Return dict of CISCO-VTP-MIB vtpVlanState for each VLAN.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vtpVlanState using the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.4.1.9.9.46.1.3.1.1.2"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    async def vlantrunkportvlansenabled(self, oidonly=False):
        """Return CISCO-VTP-MIB vlanTrunkPortVlansEnabled data per ifIndex.

        Args:
            oidonly: Return OID's value, not results, if True

        Returns:
            data_dict: Dict of vlanTrunkPortVlansEnabled keyed by ifIndex
                with values being lists of enabled VLAN tags.

        """
        # Initialize key variables
        data_dict = defaultdict(dict)
        length_in_bits = 1024
        base = 16

        # Get the trunk status for all ifIndex values
        trunkstatus = await self.vlantrunkportdynamicstatus()

        # OID to Process
        oid = ".1.3.6.1.4.1.9.9.46.1.6.1.1.4"

        # Return OID value. Used for unittests
        if oidonly is True:
            return oid

        # Process results
        results = await self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Get the ifindex value
            ifindex = int(key)
            
            #! is this needed in pysnmp, have to check it throughly
            # Convert hex value to right justified 1024 character binary string
            vlans_hex = binascii.hexlify(value).decode("utf-8")
            binary_string = bin(int(vlans_hex, base))[2:].zfill(length_in_bits)

            # Assign flag vlans on interface
            if trunkstatus[ifindex] == 1:
                for svlan, state in enumerate(binary_string):
                    vlan = int(svlan)
                    if int(state) == 1:
                        if ifindex in data_dict:
                            data_dict[ifindex].append(vlan)
                        else:
                            data_dict[ifindex] = [vlan]

        # Return the interface descriptions
        return data_dict
