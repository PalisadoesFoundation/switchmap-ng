"""Module for converting Device table to JSON."""

from copy import deepcopy
import datetime


class Device:
    """Convert device data to JSON."""

    def __init__(self, data):
        """Initialize class.

        Args:
            data: DeviceDetail object

        Returns:
            None

        """
        # Initialize key variables
        self._data = data

    def dictify(self):
        """Convert data to json.

        Args:
            None

        Returns:
            result: Dict representation of DeviceDetail object

        """
        pass


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