"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint, jsonify


# Application imports
from switchmap.core import rest
from switchmap.dashboard.configuration import ConfigDashboard

# Define the API global variable
API = Blueprint("API", __name__)


@API.route("/dashboard", methods=["GET"])
def dashboard():
    """Get dashboard data.

    Args:
        None

    Returns:
        JSON of device data

    """
    # Initialize key variables
    config = ConfigDashboard()
    query = """
{
  roots(filter: {idxRoot: {eq: 1}}) {
    edges {
      node {
        event {
          zones {
            edges {
              node {
                name
                devices {
                  edges {
                    node {
                      hostname
                      idxDevice
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

"""
    #
    # Get the data
    data = rest.get_graphql(query, config)

    # Return
    return jsonify(data)
