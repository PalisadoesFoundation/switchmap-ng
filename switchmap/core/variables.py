"""Module for classes that format variables."""


class AgentAPIVariable:
    """Variable representation for data required by the AgentAPI."""

    def __init__(self, ip_bind_port=20201, ip_listen_address="0.0.0.0"):
        """Initialize the class.

        Args:
            ip_bind_port: ip_bind_port
            listen_address: TCP/IP address on which the API is listening.

        Returns:
            None

        """
        # Initialize variables
        self.ip_bind_port = ip_bind_port
        self.ip_listen_address = ip_listen_address

    def __repr__(self):
        """Return a representation of the attributes of the class.

        Args:
            None

        Returns:
            result: String representation.

        """
        result = """\
<{0} ip_bind_port={1}, ip_listen_address={2}>\
""".format(
            self.__class__.__name__,
            repr(self.ip_bind_port),
            repr(self.ip_listen_address),
        )
        return result
