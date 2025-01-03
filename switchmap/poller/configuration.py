"""switchmap classes that manage various configurations."""

from switchmap.core.configuration import ConfigAPIClient
from switchmap.core import log
from switchmap.poller import ZONE, SNMP


class ConfigPoller(ConfigAPIClient):
    """Class gathers all configuration information."""

    def __init__(self):
        """Intialize the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        section = "poller"

        # Instantiate sub class
        ConfigAPIClient.__init__(self, section)

        # Get poller config
        self._config_poller = self._config_complete.get(section)

        # Error if incorrectly configured
        if bool(self._config_poller) is False:
            log_message = (
                'No "{}:" section found in the configuration file(s)'.format(
                    section
                )
            )
            log.log2die_safe(1007, log_message)

    def hostnames(self):
        """Get hostnames.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = []
        candidates = self._config_poller.get("hostnames", [])

        # Get result
        if isinstance(candidates, list) is True:
            candidates = list(set(candidates))
            result = sorted(candidates)

        # Return
        return result

    def polling_interval(self):
        """Get polling_interval.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_poller.get("polling_interval", 86400)
        return result

    def snmp_auth(self):
        """Get list of dicts of SNMP information in configuration file.

        Args:
            None

        Returns:
            snmp_data: List of SNMP objects.

        """
        # Initialize key variables
        _groups = self._config_poller.get("snmp_groups", [])
        result = []

        # Read configuration's SNMP information. Return 'None' if none found
        if isinstance(_groups, list) is True:
            if len(_groups) < 1:
                return result
        else:
            return result

        # Start populating information
        for _group in _groups:
            # Next entry if this is not a dict
            if isinstance(_group, dict) is False:
                continue

            # Apply values
            result.append(
                SNMP(
                    enabled=_group.get("enabled", True),
                    group=_group.get("group_name"),
                    version=int(_group.get("snmp_version", 3)),
                    secname=_group.get("snmp_secname"),
                    authprotocol=_group.get("snmp_authprotocol"),
                    authpassword=_group.get("snmp_authpassword"),
                    privprotocol=_group.get("snmp_privprotocol"),
                    privpassword=_group.get("snmp_privpassword"),
                    port=int(_group.get("snmp_port", 161)),
                    community=_group.get("snmp_community"),
                )
            )

        # Return
        return result

    def username(self):
        """Get username.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._config_poller.get("username", "switchmap")
        return result

    def zones(self):
        """Get list of dicts of polling zone information in configuration file.

        Args:
            None

        Returns:
            result: List of ZONE objects.

        """
        # Initialize key variables
        _zones = self._config_poller.get("zones", [])
        result = []

        # Read configuration. Return [] if none found
        if isinstance(_zones, list) is True:
            if len(_zones) < 1:
                return result
        else:
            return result

        # Start populating information
        for _zone in _zones:
            # Next entry if this is not a dict
            if isinstance(_zone, dict) is False:
                continue

            # Assign good data
            result.append(
                ZONE(
                    name=_zone.get("zone"),
                    hostnames=(
                        _zone.get("hostnames")
                        if isinstance(_zone.get("hostnames"), list)
                        else None
                    ),
                )
            )

        # Return
        return result
