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


@API.route("/devices/<int:idx_device>", methods=["GET"])
def devices(idx_device):
    """Get device data.

    Args:
        None

    Returns:
        JSON of zone data

    """
    # Initialize key variables
    config = ConfigDashboard()
    query = """
{
  devices(filter: {idxDevice: {eq: IDX_DEVICE}}) {
    edges {
      node {
        hostname
        l1interfaces {
          edges {
            node {
              ifname
              ifalias
              ifoperstatus
              ifadminstatus
              ifspeed
              iftype
              duplex
              trunk
              cdpcachedeviceid
              cdpcacheplatform
              cdpcachedeviceport
              lldpremsysname
              lldpremportdesc
              lldpremsysdesc
              nativevlan
              vlanports {
                edges {
                  node {
                    vlans {
                      vlan
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

""".replace(
        "IDX_DEVICE", str(idx_device)
    )

    # Get the data
    result = rest.get_graphql(query, config)
    normalized = graphene.normalize(result)

    # Get the zone data list
    data = normalized.get("data")
    device = data.get("devices")[0]

    # Return
    return jsonify(device)
