"""Config API routes for Switchmap."""

from flask import Blueprint, jsonify, request
import yaml
import os

API_CONFIG = Blueprint("config", __name__)

CONFIG_PATH = "/home/abhi/switchmap-ng/etc/config.yaml"


def read_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f) or {}


def write_config(data):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


@API_CONFIG.route("/config", methods=["GET"])
def get_config():
    """Return the current config as JSON."""
    with open("/home/abhi/switchmap-ng/etc/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    return jsonify(config)


@API_CONFIG.route("/config", methods=["POST"])
def update_config():
    """Update the config.yaml with new JSON data."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    write_config(data)
    return jsonify({"status": "success"})
