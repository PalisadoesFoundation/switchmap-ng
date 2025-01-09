"""Module of switchmap.webserver routes.

Contains all routes that switchmap.s Flask webserver uses

"""

# Flask imports
from flask import Blueprint, jsonify, request


# Application imports
from switchmap.core import rest
from switchmap.core import graphene
from switchmap.dashboard.configuration import ConfigDashboard
from switchmap.dashboard import graphql_filters

# Define the API global variable
API = Blueprint("API", __name__)


@API.route("/dashboard", methods=["GET"])
def dashboard():
    """Get dashboard data.

    Args:
        None

    Returns:
        html: Webpage HTML

    """
    # Return content
    html = _dashboard()
    return html


@API.route("/dashboard/<int:idx_root>", methods=["GET"])
def historical_dashboard(idx_root):
    """Get dashboard data.

    Args:
        idx_root: IDX of the root in the DB

    Returns:
        html: Webpage HTML

    """
    # Return content
    html = _dashboard(idx_root)
    return html


@API.route("/events/<int:idx_root>", methods=["GET"])
def event_by_idx_root(idx_root):
    """Get event data.

    Args:
        idx_root: IDX of the root in the DB

    Returns:
        result: JSON of zone data

    """
    # return
    return roots_filter(idx_root)


@API.route("/events", methods=["GET"])
def events():
    """Get event data.

    Args:
        None

    Returns:
        result: JSON of zone data

    """
    # return
    return roots_filter()


@API.route("/devices/<int:idx_device>", methods=["GET"])
def devices(idx_device):
    """Get device data.

    Args:
        idx_device: IDX of the DB device table

    Returns:
        result: JSON of zone data

    """
    # Initialize key variables
    config = ConfigDashboard()
    query = """
{
  devices(filter: {idxDevice: {eq: IDX_DEVICE}}) {
    edges {
      node {
        hostname
        sysName
        sysDescription
        sysObjectid
        sysUptime
        lastPolled
        device {
          event {
            tsCreated
            roots {
              edges {
                node {
                  idxRoot
                }
              }
            }
          }
        }
        l1interfaces {
          edges {
            node {
              INTERFACE
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

    # Insert the interface snippet
    updated_query = _insert_interface_snippet(query)

    # Get the data
    result = rest.get_graphql(updated_query, config)
    normalized = graphene.normalize(result)

    # Get the zone data list
    data = normalized.get("data")
    device = data.get("devices")[0]

    # Return
    return jsonify(device)


@API.route("/search", methods=["POST"])
def search():
    """Get device data.

    Args:
        None

    Returns:
        result: JSON of zone data

    """
    # Initialize key variables
    config = ConfigDashboard()
    result = []
    idx_l1interfaces = []

    # Extract the interface list form the POST request
    idx_l1interfaces = request.json

    # Create the filter string
    filter_string = graphql_filters.or_operator(
        "idxL1interface", idx_l1interfaces
    )
    query = """
{
  l1interfaces(filter: FILTER) {
    edges {
      node {
        device {
          name
          sysName
          hostname
          device{
            name
          }
        }
        INTERFACE
      }
    }
  }
}
""".replace(
        "FILTER", filter_string
    )

    # Insert the interface snippet
    updated_query = _insert_interface_snippet(query)

    # Get the data
    data = rest.get_graphql(updated_query, config)

    if bool(data) is True:
        normalized = graphene.normalize(data)

        # Get the zone data list
        data = normalized.get("data")
        result = data.get("l1interfaces")

    # Return
    return jsonify(result)


def _dashboard(idx_root=1):
    """Get dashboard data.

    Args:
        idx_root: Database Root table index

    Returns:
        result: JSON of event data

    """
    # Initialize key variables
    config = ConfigDashboard()
    default = {}
    query = """
{
  roots(filter: {idxRoot: {eq: ROOT}}) {
    edges {
      node {
        event {
          tsCreated
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

""".replace(
        "ROOT", str(idx_root)
    )

    # Get the data
    result = rest.get_graphql(query, config)
    normalized = graphene.normalize(result)

    # Get the zone data list
    data = normalized.get("data")
    if bool(data) is True:
        roots = data.get("roots")
        if bool(roots) is True:
            event = roots[0].get("event")
        else:
            event = default

        # Return
        return jsonify(event)
    else:
        # Return
        return jsonify({})


def _insert_interface_snippet(query):
    """Insert the standard interface query string snippet.

    Args:
        query: original query with the INTERFACE keyword inserted

    Returns:
        result: data with the INTERFACE keyword replaced by the snippet

    """
    # Initialize key variables
    snippet = """
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
        tsIdle
        macports {
          edges {
            node {
              macs {
                mac
                oui {
                  organization
                }
                macips {
                  edges {
                    node {
                      ips {
                        address
                        version
                        hostname
                      }
                    }
                  }
                }
              }
            }
          }
        }
        vlanports {
          edges {
            node {
              vlans {
                vlan
              }
            }
          }
        }
"""
    # Return
    result = query.replace("INTERFACE", snippet)
    return result


def roots_filter(idx_root=False):
    """Get event data.

    Args:
        idx_root: IDX of the DB root

    Returns:
        roots: JSON of zone data

    """
    # Initialize key variables
    config = ConfigDashboard()
    filtration = (
        "(filter: {idxRoot: {eq: IDX_ROOT}}) ".replace(
            "IDX_ROOT", str(idx_root)
        )
        if bool(idx_root) is True
        else ""
    )

    query = """
{
  roots FILTER{
    edges {
      node {
        idxRoot
        event {
          tsCreated
        }
      }
    }
  }
}
""".replace(
        "FILTER", filtration
    )

    # Get the data
    result = rest.get_graphql(query, config)
    normalized = graphene.normalize(result)

    # Get the zone data list
    data = normalized.get("data")
    roots = data.get("roots", {})

    # Return
    return jsonify(roots)
