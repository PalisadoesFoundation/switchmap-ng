"""Config API routes for Switchmap."""

from flask import Blueprint, jsonify, request
import yaml
import os
import tempfile

API_CONFIG = Blueprint("config", __name__)

CURRENT_DIR = os.path.dirname(__file__)

CONFIG_PATH = os.environ.get(
    "CONFIG_PATH",
    os.path.abspath(os.path.join(CURRENT_DIR, "../../../../etc/config.yaml")),
)

PLACEHOLDER = "********"
SECRET_KEYS = {
    "db_pass",
    "snmp_authpassword",
    "snmp_privpassword",
    "snmp_community",
}


def _is_secret_placeholder(v):
    return (
        isinstance(v, dict)
        and v.get("isSecret")
        and v.get("value") == PLACEHOLDER
    ) or (isinstance(v, str) and v == PLACEHOLDER)


def merge_preserving_secrets(current, incoming):
    """Merge two configuration objects while preserving secret values.

    Args:
        current (dict | Any): Existing configuration or value.
        incoming (dict | Any): New configuration or value to merge.

    Returns:
        result: Merged configuration where secrets are preserved.
    """
    if isinstance(current, dict) and isinstance(incoming, dict):
        out = dict(current)
        for k, v in incoming.items():
            if k in SECRET_KEYS:
                # accept updates only if not a placeholder or empty
                if _is_secret_placeholder(v):
                    continue
                if v in ("", None):
                    continue
                out[k] = v
            else:
                out[k] = merge_preserving_secrets(current.get(k), v)
        return out
    # Merge lists positionally (best-effort). If shapes diverge, prefer incoming.
    if isinstance(current, list) and isinstance(incoming, list):
        merged = []
        for i, v in enumerate(incoming):
            prev = current[i] if i < len(current) else None
            merged.append(merge_preserving_secrets(prev, v))
        return merged
    return incoming


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
    try:
        with open(CONFIG_PATH, "r") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return {}
    except OSError:
        return {}


def write_config(data):
    """Write the configuration data to disk.

    Args:
        data (dict): The configuration data to write.

    Returns:
        None
    """
    dir_name = os.path.dirname(CONFIG_PATH) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix=".config.", text=True)
    try:
        with os.fdopen(fd, "w") as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, CONFIG_PATH)
        try:
            os.chmod(CONFIG_PATH, 0o600)
        except OSError:
            pass
    finally:
        try:
            os.unlink(tmp_path)
        except FileNotFoundError:
            pass


@API_CONFIG.route("/config", methods=["GET"])
def get_config():
    """Return the current configuration as JSON.

    Args:
        None

    Returns:
        Response: A Flask JSON response containing the current config
        loaded from config.yaml.
    """
    return jsonify(mask_secrets(read_config()))


def mask_secrets(config: dict) -> dict:
    """Recursively masks sensitive values in a configuration dictionary.

    Specifically, replaces the value of "db_pass" with a masked string,
    while preserving the structure of nested dictionaries.

    Args:
        config (dict): The configuration dictionary to process.

    Returns:
        dict: A new dictionary with secrets masked.
    """
    if isinstance(config, dict):
        out = {}
        for k, v in config.items():
            if k in SECRET_KEYS and v:
                out[k] = {"isSecret": True, "value": PLACEHOLDER}
            else:
                out[k] = mask_secrets(v)
        return out
    if isinstance(config, list):
        return [mask_secrets(x) for x in config]
    return config


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
    current_config = read_config()
    sanitized = merge_preserving_secrets(current_config, data)
    write_config(sanitized)
    return jsonify({"status": "success"})


def deep_merge(dst, src):
    """Recursively merge two dictionaries or values.

    Args:
        dst (dict | Any): Destination dictionary or value.
        src (dict | Any): Source dictionary or value to merge into dst.

    Returns:
        result: Result of merging src into dst.
    """
    if isinstance(dst, dict) and isinstance(src, dict):
        out = dict(dst)
        for k, v in src.items():
            out[k] = deep_merge(out.get(k), v)
        return out
    return src


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
        if "server" not in current_config or not isinstance(
            current_config["server"], dict
        ):
            current_config["server"] = {}
        if new is not None:
            current_config["server"]["db_pass"] = new

    # Merge all other non-secret fields
    for key, value in data.items():
        if key == "db_pass":
            continue
        current_config[key] = deep_merge(current_config.get(key), value)
    write_config(current_config)
    return jsonify({"status": "success"})
