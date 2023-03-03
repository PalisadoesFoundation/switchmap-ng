"""Functions for creating URIs."""

# Standard imports
import sys
import requests
from collections import namedtuple

# Import repository libraries
from switchmap.poller.configuration import ConfigAPIClient
from switchmap.core import log
from switchmap import API_PREFIX
from switchmap.core.log import ExceptionWrapper


def post(uri, data, config):
    """Create URI for datacenter RRD and oid_id data.

    Args:
        uri: URI for posting
        data: Data to post
        config: ConfitAPIClient object

    Returns:
        success: True if successful

    """
    # Initialize key variables
    success = False
    response = False

    # Create the URL for posting
    config = ConfigAPIClient()
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


def get(uri, config, server=True, die=True):
    """Get data fro URI from API server.

    Args:
        uri: URI for posting
        config: ConfigAPIClient object
        server: True if getting data from a server
        die: Die if the connection fails if True

    Returns:
        success: True if successful

    """
    # Initialize key variables
    data = []

    # Create the URL for posting
    if bool(server) is True:
        url_root = config.server_url_root()
    else:
        url_root = config.api_url_root()

    url = _clean_url("{}/{}".format(url_root, uri))

    # Return
    data = _get_json(url, config, die=die)
    return data


def get_graphql(query, config, die=True):
    """Get data fro URI from API server.

    Args:
        query: Query string from GraphQL server
        config: ConfigAPIClient object
        die: Die if the connection fails if True

    Returns:
        success: True if successful

    """
    # Initialize key variables
    data = []

    # Create the URL for posting
    url_root = config.server_url_root()
    url = _clean_url("{}/{}/graphql".format(url_root, API_PREFIX))

    # Return
    data = _get_json(url, config, die=die, query=query)
    return data


def _get_json(url, config, die=True, query=None):
    """Get data fro URI from API server.

    Args:
        url: URL to query
        config: ConfigAPIClient object
        die: Die if the connection fails if True
        query: Query string to use in the HTTP GET

    Returns:
        data: Dict of response

    """
    # Initialize key variables
    data = []

    # Get data from API server
    _result = _get(url, config, die=die, query=query)

    # Get data
    if _result.success is True:
        try:
            data = _result.response.json()
        except Exception as exception_error:
            log_message = (
                "Failed to get JSON data from API server URL {}. Error: {}"
                "".format(url, exception_error)
            )
            if die is True:
                log.log2die(1130, log_message)
            else:
                log.log2info(1595, log_message)

    # Return
    return data


def _get(url, config, die=True, query=None, stream=False):
    """Get data fro URI from API server.

    Args:
        url: URL to query
        config: ConfigAPIClient config
        die: Die if the connection fails if True
        query: Query string to use in the HTTP GET
        stream: True if requesting a file download (Requests stream)

    Returns:
        response: ServerResponse object

    """
    # Initialize key variables
    success = False
    response = []
    ServerResponse = namedtuple("ServerResponse", "success, response")

    # Create the URL for posting
    username = config.server_username()
    password = config.server_password()

    # Post data save to cache if this fails
    try:
        with requests.Session() as session:
            if bool(query) is False:
                response = session.get(
                    url, stream=stream, auth=(username, password)
                )
            else:
                response = session.get(
                    url,
                    stream=stream,
                    auth=(username, password),
                    params={"query": query},
                )
            success = True
    except Exception as exception_error:
        log_message = (
            "Failed to connect to server API URL {}. Error: {}"
            "".format(url, exception_error)
        )
        if die is True:
            log.log2die(1598, log_message)
        else:
            log.log2info(1017, log_message)

    # Return
    response = ServerResponse(response=response, success=success)
    return response


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
