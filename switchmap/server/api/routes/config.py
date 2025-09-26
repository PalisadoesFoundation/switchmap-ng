"""Config API routes for Switchmap."""

from flask import Blueprint, jsonify, request
import yaml
import os

API_CONFIG = Blueprint("config", __name__)

CURRENT_DIR = os.path.dirname(__file__)

CONFIG_PATH = os.environ.get(
    "CONFIG_PATH",
    os.path.abspath(os.path.join(CURRENT_DIR, "../../../../etc/config.yaml")),
)


def read_config():
    """Read the configuration file from disk.

    Args:
        None

    Returns:
        dict: The loaded configuration data. Returns an empty dictionary if
            the configuration file does not exist or is empty.
    """
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f) or {}


def write_config(data):
    """Write the configuration data to disk.

    Args:
        data (dict): The configuration data to write.

    Returns:
        None
    """
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


@API_CONFIG.route("/config", methods=["GET"])
def get_config():
    """Return the current configuration as JSON.

    Args:
        None

    Returns:
        Response: A Flask JSON response containing the current config
        loaded from config.yaml.
    """
    return jsonify(read_config())


@API_CONFIG.route("/config", methods=["POST"])
def update_config():
    """Update the config.yaml with new JSON data from the request.

    Args:
        None

    Returns:
        Response: A Flask JSON response indicating success or failure.
            Returns 400 if the JSON data is invalid, otherwise returns
            a success message.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    write_config(data)
    return jsonify({"status": "success"})
