"""switchmap dashboard URIs."""

# Import project libraries
from switchmap import API_PREFIX


def dashboard():
    """Create the dashboare  page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "{}/dashboard".format(API_PREFIX)
    return result


def devices(idx_device):
    """Create the device page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "{}/devices/{}".format(API_PREFIX, idx_device)
    return result
