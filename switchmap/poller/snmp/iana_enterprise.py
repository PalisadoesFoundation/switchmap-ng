"""Vendor queries."""


class Query:
    """Class interacts with devices to get vendor information.

    Args:
        None

    Returns:
        None

    Methods:
        All methods rely on this document to determine vendors
        https://www.iana.org/assignments/
            enterprise-numbers/enterprise-numbers

    """

    def __init__(self, enterprise=None, sysobjectid=None):
        """Instantiate the class.

        Args:
            enterprise: The enterprise number of the manufacturer
            sysobjectid: The sysobjectid of the device

        Returns:
            None

        """
        # IANA SNMP enterprise numbers
        if sysobjectid is not None:
            nodes = sysobjectid.split(".")
            self.enterprise_id = int(nodes[7])
        else:
            self.enterprise_id = int(enterprise)

        # Assign sysobjectid
        self.sysobjectid = sysobjectid

    def enterprise(self):
        """Get enterprise number.

        Args:
            None

        Returns:
            self.enterprise_id: Enterprise number

        """
        return self.enterprise_id

    def is_cisco(self):
        """Verify whether device is a Cisco device.

        Args:
            None

        Returns:
            value: True if matches vendor

        """
        # Initialize key variables
        value = False

        # Checks system object ID
        if self.enterprise_id == 9:
            value = True

        # Return
        return value

    def is_juniper(self):
        """Verify whether device is a Juniper device.

        Args:
            None

        Returns:
            value: True if matches vendor

        """
        # Initialize key variables
        value = False

        # Checks system object ID
        if self.enterprise_id == 2636:
            value = True

        # Return
        return value
