"""switchmap.Search class.

Description:

    This files has classes that process searches for:
        1) IP and MAC address
        2) Port names
        3) Hostnames

"""
# Standard imports
import re

# Switchmap-NG imports
from switchmap import CONFIG
from switchmap.utils import general


class Search(object):
    """Class that manages searches.

    Methods return lists of dicts keyed 'layer 1' with ifindex values
    where search stings were found. This data is then used to create result
    tables.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, searchstring):
        """Initialize the class.

        Args:
            searchstring: search string to look for

        Returns:
            None

        """
        # Initialize key variables
        self._search = []
        self.config = CONFIG

        # Generate various possible strings that could be used for searches
        self._search = _search_list(searchstring)

        # Read ifindex file
        self.ifindex_data = general.read_yaml_file(self.config.ifindex_file())

        # Read host file
        self.arp_data = general.read_yaml_file(self.config.arp_file())

        # Read ifalias file
        self.ifalias_data = general.read_yaml_file(self.config.ifalias_file())

    def find(self):
        """Find search string.

        Args:
            None

        Returns:
            result: list of dicts that contain matching items

        """
        # Initialize key variables
        result = []

        # Do each successive search
        result.extend(self.macaddress())
        result.extend(self.ifalias())
        result.extend(self.ipaddress())
        result.extend(self.hostname())

        # Return
        return result

    def macaddress(self):
        """Search for macaddress.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Return
        result = _macaddress(self._search, self.ifindex_data)
        return result

    def ipaddress(self):
        """Search for ipaddress.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []

        # Process the ifindex file
        for _, devices in self.ifindex_data.items():
            # Get all the hostnames and ifindexes that have the MAC
            for device, ifindexes in devices.items():
                for ifindex, ipaddresses in ifindexes.items():
                    for ipaddress in ipaddresses:
                        # Find search string in MAC address keys
                        for possible in self._search:
                            if possible in "{}".format(ipaddress).lower():
                                data_dict = {}
                                data_dict[device] = int(ifindex)
                                result.append(data_dict)

        # Return
        return result

    def ifalias(self):
        """Search for string in ifalias names.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []

        for ifalias, ifalias_dict in self.ifalias_data.items():
            # Find search string in ifalias keys
            for possible in self._search:
                if possible in "{}".format(ifalias).lower():
                    # We have found something
                    for device, ifindexes in ifalias_dict.items():
                        for ifindex in ifindexes:
                            data_dict = {}
                            data_dict[device] = int(ifindex)
                            result.append(data_dict)

        # Return
        return result

    def hostname(self):
        """Search for string hostnames.

        Args:
            None

        Returns:
            result: list of dicts that contain matching addresses

        """
        # Initialize key variables
        result = []
        macaddresses = []

        for _, data_dict in self.arp_data.items():
            # Make sure we can get the hostname and MAC
            if "hostname" not in data_dict:
                continue
            if "mac_address" not in data_dict:
                continue

            # Find search string in MAC address keys
            hostname = data_dict["hostname"]
            macaddress = data_dict["mac_address"]

            # If there is no hostname return (multicast)
            if bool(hostname) is False:
                continue

            for possible in self._search:
                if possible in hostname.lower():
                    macaddresses.append(macaddress)

        # See if we can get the ifindex for the macaddress
        result.extend(_macaddress(macaddresses, self.ifindex_data))

        # Return
        return result


def _macaddress(_search, ifindex_data):
    """Search for macaddress.

    Args:
        _search: List of search values to Find
        ifindex_data: ifindex data to search through

    Returns:
        result: list of dicts that contain matching addresses

    """
    # Initialize key variables
    result = []

    # Process the ifindex file
    for macaddress, devices in ifindex_data.items():
        # Find search string in MAC address keys
        for possible in _search:

            if possible in "{}".format(macaddress).lower():
                # Get all the devices and ifindexes that have the MAC
                for device, ifindexes in devices.items():
                    for ifindex, _ in ifindexes.items():
                        data_dict = {}
                        data_dict[device] = int(ifindex)
                        result.append(data_dict)

    # Return
    return result


def _search_list(searchstring):
    """Generate various possible strings that could be used for searches.

    Args:
        searchstring: search string to look for

    Returns:
        result: List of possible search terms

    """
    # Initialize key variables
    result = [searchstring.lower()]

    # Lowercase alphanumeric search string for MAC addresses
    pattern = re.compile(r"[\W_]+")
    next_string = pattern.sub("", searchstring).lower()
    if next_string not in result:
        result.append(next_string)

    # Return
    return result
