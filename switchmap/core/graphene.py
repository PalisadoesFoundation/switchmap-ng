"""Module with graphene functions."""


def normalize(data):
    """Remove all 'edges' and 'node' keys from graphene results.

    Args:
        data: Dict of graphene results

    Returns:
        result: Dict withoug 'edges' and 'node' keys

    """
    # Initialize key variables
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "edges":
                result = nodes(value)
            else:
                if isinstance(value, dict):
                    result[key] = normalize(value)
                else:
                    result[key] = value
    else:
        return data

    return result


def nodes(_nodes):
    """Strip the 'node' key from a list of graphene nodes.

    Args:
        _nodes: List of graphene node dicts

    Returns:
        result: List without the 'node' key

    """
    # Initilize key variables
    result = []

    # Process the data
    for _node in _nodes:
        node = _node.get("node")
        if isinstance(node, dict):
            result.append(normalize(node))
        else:
            result.append(node)
    return result
