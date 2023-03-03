"""switchmap dashboard URIs."""

# Import project libraries
from switchmap import API_PREFIX


def dashboard():
    """Create the index page URI.

    Args:
        None

    Returns:
        result: result

    """
    # Get result
    result = "/{}/dashboard".format(API_PREFIX)
    return result
