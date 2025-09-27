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


def mask_secrets(config: dict) -> dict:
    """Recursively masks sensitive values in a configuration dictionary.

    Specifically, replaces the value of "db_pass" with a masked string,
    while preserving the structure of nested dictionaries.

    Args:
        config (dict): The configuration dictionary to process.

    Returns:
        dict: A new dictionary with secrets masked.
    """
    masked = {}
    for key, value in config.items():
        if key == "db_pass" and value:
            masked[key] = {"isSecret": True, "value": "********"}
        elif isinstance(value, dict):
            masked[key] = mask_secrets(value)
        else:
            masked[key] = value
    return masked


@API_CONFIG.route("/config", methods=["POST"])
def post_config():
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


@API_CONFIG.route("/config", methods=["PATCH"])
def patch_config():
    """Partially update the SwitchMap configuration.

    Handles the db_pass secret securely:
      - Expects db_pass updates in the form {"current": "...", "new": "..."}.
      - Updates db_pass directly without checking for the default placeholder.
      - Other non-secret fields are merged directly.

    Args:
        None

    The request JSON body can contain:
      - "db_pass" (dict, optional): {"new": "<new_password>"}
      - Other configuration keys to update.

    Returns:
        Response: JSON response indicating success or failure:
          - 400 if the request JSON is invalid or db_pass format is incorrect.
          - 200 with {"status": "success"} on successful update.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    current_config = read_config()

    # Handle db_pass specially
    if "db_pass" in data:
        db_pass_data = data["db_pass"]
        if not isinstance(db_pass_data, dict) or "new" not in db_pass_data:
            return jsonify({"error": "Invalid db_pass format"}), 400

        new = db_pass_data.get("new")
        if new:
            current_config["server"]["db_pass"] = new

    # Merge all other non-secret fields
    for key, value in data.items():
        if key != "db_pass":
            current_config[key] = value

    write_config(current_config)
    return jsonify({"status": "success"})
