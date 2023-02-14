"""Module for data handling."""

# Standard libraries
import hashlib
import datetime


def hashstring(string, sha=256, utf8=False):
    """Create a UTF encoded SHA hash string.

    Args:
        string: String to hash
        length: Length of SHA hash
        utf8: Return utf8 encoded string if true

    Returns:
        result: Result of hash

    """
    # Initialize key variables
    listing = [1, 224, 384, 256, 512]

    # Select SHA type
    if sha in listing:
        index = listing.index(sha)
        if listing[index] == 1:
            hasher = hashlib.sha1()
        elif listing[index] == 224:
            hasher = hashlib.sha224()
        elif listing[index] == 384:
            hasher = hashlib.sha384()
        elif listing[index] == 512:
            hasher = hashlib.sha512()
        else:
            hasher = hashlib.sha256()

    # Encode the string
    hasher.update(bytes(string.encode()))
    target_hash = hasher.hexdigest()
    if utf8 is True:
        result = target_hash.encode()
    else:
        result = target_hash

    # Return
    return result


def dictify(data):
    """Convert NamedTuple to dict.

    Args:
        data: NamedTuple

    Returns:
        result: Dict representation of object

    """
    # Initialize key variables

    if isinstance(data, tuple):
        result = {}
        converted = data._asdict()
        for key, value in converted.items():
            # Convert datetime objects to a serializable object
            if isinstance(value, datetime.datetime):
                value = _time(value)
            result[key] = dictify(value)
    elif isinstance(data, list):
        result = []
        for value in data:
            item = dictify(value)
            # Convert datetime objects to a serializable object
            if isinstance(item, datetime.datetime):
                item = _time(item)
            result.append(item)
    else:
        result = data
    return result


def _time(data):
    """Convert Date to string.

    Args:
        data: datetime object

    Returns:
        result: String time

    """
    # Initialize key variables
    result = data.strftime("%Y-%m-%d %H:%M:%S.%f")
    return result
