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


def events():
    """Create the event page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "{}/events".format(API_PREFIX)
    return result


def events_by_idx_root(idx_root=1):
    """Create the filtered event page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "{}/events/{}".format(API_PREFIX, idx_root)
    return result


def search_dashboard_server():
    """Create the device page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "/search"
    return result


def search_api_server():
    """Create the device page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "/post/search"
    return result
