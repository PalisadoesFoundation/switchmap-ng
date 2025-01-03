"""Class interacts with devices supporting ENTITY-MIB."""

from collections import defaultdict

from switchmap.poller.snmp.base_query import Query


def get_query():
    """Return this module's Query class."""
    return EntityQuery


def init_query(snmp_object):
    """Return initialize and return this module's Query class."""
    return EntityQuery(snmp_object)


class EntityQuery(Query):
    """Class interacts with devices supporting ENTITY-MIB.

    Args:
        None

    Returns:
        None

    Key Methods:

        supported: Queries the device to determine whether the MIB is
            supported using a known OID defined in the MIB. Returns True
            if the device returns a response to the OID, False if not.

        system: Returns all relevant system information from the device.
            In some cases a system will have multiple subsystems that are
            covered by an OID. (eg. module / circuit board serial numbers).
            It will therefore be impossible to have a consistent key format
            for data values returned. Data returned by this method will
            therefore be keyed by :
            1) MIB name (primary key)
            2) OID name in the MIB, (secondary key),
            3) Leaf value, or zero (0) if there are no leaves.

    """

    def __init__(self, snmp_object):
        """Intialize the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Get one OID entry in MIB (entPhysicalName).
        test_oid = ".1.3.6.1.2.1.47.1.1.1.1.7"

        super().__init__(snmp_object, test_oid, tags=["system"])

    def system(self):
        """Get system data from device.

        Args:
            None

        Returns:
            final: Final results

        """
        # Initialize key variables
        data_dict = defaultdict(lambda: defaultdict(dict))
        final = {}

        # Get data
        hw_rev = self.entphysicalhardwarerev()
        fw_rev = self.entphysicalfirmwarerev()
        sw_rev = self.entphysicalsoftwarerev()
        name = self.entphysicalname()
        model = self.entphysicalmodelname()
        serial = self.entphysicalserialnum()
        classtype = self.entphysicalclass()
        description = self.entphysicaldescr()

        # Only process if a serial number is found
        count = 0
        for key, value in sorted(serial.items()):
            if bool(value) is True:
                data_dict["entPhysicalSerialNum"][count] = serial[key]
                data_dict["entPhysicalName"][count] = name[key]
                data_dict["entPhysicalModelName"][count] = model[key]
                data_dict["entPhysicalHardwareRev"][count] = hw_rev[key]
                data_dict["entPhysicalSoftwareRev"][count] = sw_rev[key]
                data_dict["entPhysicalFirmwareRev"][count] = fw_rev[key]
                data_dict["entPhysicalClass"][count] = classtype[key]
                data_dict["entPhysicalDescr"][count] = description[key]
                count = count + 1

        # Return
        final["ENTITY-MIB"] = data_dict
        return final

    def entphysicaldescr(self):
        """Return dict of ENTITY-MIB entPhysicalDescr for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalDescr using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.2"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict

    def entphysicalclass(self):
        """Return dict of ENTITY-MIB entPhysicalClass for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalClass using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.5"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = value

        # Return the interface descriptions
        return data_dict

    def entphysicalsoftwarerev(self):
        """Return dict of ENTITY-MIB entPhysicalSoftwareRev for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalSoftwareRev using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.10"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict

    def entphysicalserialnum(self):
        """Return dict of ENTITY-MIB entPhysicalSerialNum for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalSerialNum using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.11"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict

    def entphysicalmodelname(self):
        """Return dict of ENTITY-MIB entPhysicalModelName for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalModelName using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.13"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict

    def entphysicalname(self):
        """Return dict of ENTITY-MIB entPhysicalName for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalName using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.7"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict

    def entphysicalhardwarerev(self):
        """Return dict of ENTITY-MIB entPhysicalHardwareRev for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalHardwareRev using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.8"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict

    def entphysicalfirmwarerev(self):
        """Return dict of ENTITY-MIB entPhysicalFirmwareRev for device.

        Args:
            None

        Returns:
            data_dict: Dict of entPhysicalFirmwareRev using
                the oid's last node as key

        """
        # Initialize key variables
        data_dict = defaultdict(dict)

        # Descriptions
        oid = ".1.3.6.1.2.1.47.1.1.1.1.9"
        results = self.snmp_object.swalk(oid, normalized=True)
        for key, value in results.items():
            # Process OID
            data_dict[int(key)] = str(bytes(value), encoding="utf-8").strip()

        # Return the interface descriptions
        return data_dict
