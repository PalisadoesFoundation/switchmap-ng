"""Database server API. HTTP POST routes."""

# Standard imports
import os
import json

# PIP3 imports
from flask import Blueprint, request

# Repository imports
from switchmap.core import log
from switchmap import API_POLLER_POST_URI
from switchmap.server.configuration import ConfigServer


# Define the API_POST global variable
API_POST = Blueprint("API_POST", __name__)


@API_POST.route(API_POLLER_POST_URI, methods=["POST"])
def post_device_data():
    """Accept posts of network device data from pollers.

    Args:
        None

    Returns:
        _response: OK message when successful

    """
    # Initialize key variables
    config = ConfigServer()

    # Get data
    data = request.json
    try:
        hostname = data["misc"]["host"]
    except:
        hostname = None

    # Only write data if file doesn't exist. This reduces the risk of duplicate
    # data if data from a previously existing file is still being ingested.
    filepath = "{}{}{}.json".format(config.cache_directory(), os.sep, hostname)
    if os.path.exists(filepath) is False:
        # Write data to file
        data_as_string = json.dumps(data)
        with open(filepath, "w") as f_handle:
            f_handle.write(data_as_string)

        # Log
        log_message = "Successfully created data cache file {}.".format(
            filepath
        )
        log.log2info(1043, log_message)

    else:
        # Log
        log_message = "Cache file {} already exists. Will not update.".format(
            filepath
        )
        log.log2info(1042, log_message)

    # Return
    return "OK"
