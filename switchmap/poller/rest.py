"""Functions for creating URIs."""

# Standard imports
import sys
import requests

# Import repository libraries
from switchmap.poller.configuration import ConfigPoller
from switchmap.core import log
from switchmap import API_PREFIX
from switchmap.core.log import ExceptionWrapper


def post(uri, data):
    """Create URI for datacenter RRD and oid_id data.

    Args:
        uri: URI for posting
        data: Data to post

    Returns:
        success: True if successful

    """
    # Initialize key variables
    success = False
    response = False

    # Create the URL for posting
    config = ConfigPoller()
    username = config.server_username()
    password = config.server_password()
    url_root = config.server_url_root()
    url = _clean_url("{}/{}/{}".format(url_root, API_PREFIX, uri))

    # Log
    log_message = "Attempting to post data to {}.".format(url)
    log.log2info(1583, log_message)

    # Post data save to cache if this fails
    try:
        with requests.Session() as session:
            if bool(username) is False or bool(password) is False:
                result = session.post(url, json=data)
            else:
                result = session.post(
                    url, json=data, auth=(username, password)
                )
            response = True
    except Exception as error:
        log_message = "Error posting to {}".format(url)
        log.log2warning(1537, log_message)
        log.log2exception(1641, sys.exc_info())
        return ExceptionWrapper(error)
    except:
        log_message = "Failed to post data to API server URL {}.".format(url)
        log.log2info(1038, log_message)

    # Define success
    if response is True:
        if result.status_code == 200:
            success = True

            # Log
            log_message = "Successfully posted data to {}.".format(url)
            log.log2info(1037, log_message)
        else:
            # Log
            log_message = "Error {} for post to {}.".format(
                result.status_code, url
            )
            log.log2info(1039, log_message)

    # Return
    return success


def _clean_url(url):
    """Remove excess / from url.

    Args:
        url: URI to process

    Returns:
        result: Clean URI

    """
    # Initialize key variables.
    result = url.replace("//", "/")
    result = result.replace("http:/", "http://")
    result = result.replace("https:/", "https://")
    return result
