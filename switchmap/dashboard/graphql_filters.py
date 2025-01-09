"""switchmap GraphQL filter operators."""


def or_operator(key, items):
    """Create a GraphQL filter string for OR operations.

    Args:
        key: GraphQL key to run the OR operation against
        items: List of iitems for filtering

    Returns:
        result: result

    """
    # Formulate the result
    result = "{{or: [{{or: [{0}]}}]}}".format(
        ", ".join(["{{KEY: {{eq: {0}}}}}".format(_) for _ in items])
    ).replace("KEY", key)
    return result
