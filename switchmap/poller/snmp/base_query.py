"""Base Query Class for interacting with devices."""


class Query:
    """Base snmp query object.

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

    """

    tags = []

    def __init__(self, snmp_object, test_oid, tags):
        """Instantiate the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py
            test_oid: Oid that is used to check if the mib is supported
            tags: List of the layers for which this query gathers information

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

        # Oid that is used to check if the mib is supported
        self.test_oid = test_oid

        # List of the layers for which this query gathers information
        self.tags = tags

    async def supported(self):
        """Return device's support for the MIB.

        Args:
            None

        Returns:
            validity: True if supported

        """
        # Support OID
        validity = False

        # Return nothing if oid doesn't exist
        if await self.snmp_object.oid_exists(self.test_oid) is True:
            validity = True

        # Return
        return validity
