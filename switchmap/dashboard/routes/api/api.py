"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint, jsonify


# Application imports
from switchmap.core import rest
from switchmap.core import graphene
from switchmap.dashboard.configuration import ConfigDashboard

# Define the API global variable
API = Blueprint("API", __name__)


@API.route("/dashboard", methods=["GET"])
def dashboard():
    """Get dashboard data.

    Args:
        None

    Returns:
        JSON of zone data

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

    # Get the data
    result = rest.get_graphql(query, config)
    normalized = graphene.normalize(result)

    # Get the zone data list
    data = normalized.get("data")
    roots = data.get("roots")
    event = roots[0].get("event")
    zones = event.get("zones")

    # Return
    return jsonify(zones)
