"""Database server API. HTTP POST routes."""

# Standard imports
import os
import hashlib

# PIP3 imports
from flask import Blueprint, request, jsonify
import yaml

# Repository imports
from switchmap.core import log
from switchmap import API_POLLER_POST_URI
from switchmap import API_POLLER_SEARCH_URI
from switchmap.server.configuration import ConfigServer
from switchmap.server.db.misc import search


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
    try:
        zone = data["misc"]["zone"]
    except:
        zone = None

    if bool(hostname):
        # Only write data if file doesn't exist. This reduces the risk of
        # duplicate data if data from a previously existing file is still
        # being ingested.
        filepath = "{}{}{}-{}.yaml".format(
            config.cache_directory(),
            os.sep,
            hostname,
            hashlib.md5(zone.encode("utf-8")).hexdigest()[:5],
        )
        if os.path.exists(filepath) is False:
            # Write data to file
            # data_as_string = json.dumps(data)
            with open(filepath, "w") as f_handle:
                yaml.dump(data, f_handle)

            # Log
            log_message = "Successfully created data cache file {}.".format(
                filepath
            )
            log.log2info(1043, log_message)

        else:
            # Log
            log_message = (
                "Cache file {} already exists. Will not update.".format(
                    filepath
                )
            )
            log.log2info(1042, log_message)

    # Return
    return "OK"


@API_POST.route(API_POLLER_SEARCH_URI, methods=["POST"])
def post_searchterm():
    """Accept posts searches.

    Args:
        None

    Returns:
        _response: OK message when successful

    """
    # Initialize key variables
    result = []

    # Get data
    data = request.json
    try:
        searchterm = data.get("searchterm", "")
        idx_root = data.get("idx_root", 1)

    except:
        searchterm = ""
        idx_root = 1

    if bool(searchterm):
        result = search.search(int(idx_root), searchterm)
        return jsonify(result)
    else:
        return jsonify(result)
