"""switchmap dashboard URIs."""

# Standard import
import urllib.parse

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


def events():
    """Create the device page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "{}/events".format(API_PREFIX)
    return result


def search(idx_l1interfaces):
    """Create the device page URI.

    Args:
        idx_l1interfaces: List of idx_l1interfaces values

    Returns:
        result: result

    """
    # Create args list
    args_list = urllib.parse.urlencode([("idx", _) for _ in idx_l1interfaces])

    # Get result
    result = "{}/search?{}".format(API_PREFIX, args_list)
    return result


def search_post():
    """Create the device page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "/post/search"
    return result
