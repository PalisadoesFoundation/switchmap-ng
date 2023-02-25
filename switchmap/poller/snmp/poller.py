"""SNMP Poller module."""

# Switchmap imports
from switchmap.poller.configuration import ConfigPoller
from switchmap.poller import POLLING_OPTIONS, SNMP, POLL
from . import snmp_info
from . import snmp_manager
from switchmap.core import log


class Poll:
    """Switchmap-NG agent that gathers data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, hostname):
        """Initialize the class.

        Args:
            hostname: Hostname to poll

        Returns:
            None

        """
        # Initialize key variables
        self._server_config = ConfigPoller()
        self._hostname = hostname
        self._snmp_object = None

        # Get snmp configuration information from Switchmap-NG
        validate = snmp_manager.Validate(
            POLLING_OPTIONS(
                hostname=hostname,
                authorizations=self._server_config.snmp_auth(),
            )
        )
        authorization = validate.credentials()

        # Create an SNMP object for querying
        if _do_poll(authorization) is True:
            self._snmp_object = snmp_manager.Interact(
                POLL(
                    hostname=hostname,
                    authorization=authorization,
                )
            )
        else:
            log_message = (
                "Uncontactable or disabled host {}, or no valid SNMP "
                "credentials found for it.".format(self._hostname)
            )
            log.log2info(1081, log_message)

    def query(self):
        """Query all remote hosts for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        _data = None

        # Only query if wise
        if bool(self._snmp_object) is False:
            return _data

        # Get data
        log_message = """\
Querying topology data from host {}.""".format(
            self._hostname
        )
        log.log2info(1078, log_message)

        # Return the data polled from the device
        status = snmp_info.Query(self._snmp_object)
        _data = status.everything()
        return _data


def _do_poll(authorization):
    """Determine whether doing a poll is valid.

    Args:
        authorization: SNMP object

    Returns:
        poll: True if a poll should be done

    """
    # Initialize key variables
    poll = False

    if bool(authorization) is True:
        if isinstance(authorization, SNMP) is True:
            poll = bool(authorization.enabled)

    # Return
    return poll
