"""MAC address utility functions."""

import binascii


def decode_mac_address(encoded_mac):
    """Decode double-encoded MAC addresses from async poller.

    This function handles MAC addresses that may be double hex-encoded
    and returns them in a standard format.

    Args:
        encoded_mac: MAC address that may be double hex-encoded

    Returns:
        str: Properly formatted MAC address or original if already valid

    """
    # Fast-path non-strings
    if not isinstance(encoded_mac, str):
        return encoded_mac

    s = encoded_mac.strip()

    # Handle plain '0x' prefix
    if s.lower().startswith("0x"):
        return s[2:]

    # Attempt to unhexlify only when likely hex and long enough
    hexchars = "0123456789abcdefABCDEF"
    if len(s) > 12 and len(s) % 2 == 0 and all(c in hexchars for c in s):
        try:
            decoded = binascii.unhexlify(s).decode("ascii")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            return encoded_mac
        if decoded.lower().startswith("0x"):
            return decoded[2:]
        return decoded

    return s
