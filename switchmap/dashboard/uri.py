"""switchmap dashboard URIs."""

# Import project libraries
from switchmap import API_PREFIX


def dashboard():
    """Create the dashboard  page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "{}/dashboard".format(API_PREFIX)
    return result


def historical_dashboard(idx_root=1):
    """Create the dashboard  page URI.

    Args:
        idx_root: Root index

    Returns:
        result: result

    """
    # Get result
    result = "{}/dashboard/{}".format(API_PREFIX, idx_root)
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
