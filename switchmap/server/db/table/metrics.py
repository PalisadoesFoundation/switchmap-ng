"""Database table operations for metrics."""

import math
from switchmap.server.db import db
from switchmap.server.db.models import (
    DeviceMetricsHistory as _DeviceMetricsHistory,
)
import datetime
from collections.abc import Iterable


def _pct(value):
    """Normalize a percentage to the 0.0-100.0 range.

    Args:
        value (float | None): Input percentage value.
            - If None, returns None.
            - If not a finite float, returns None.
            - If less than 0.0, returns 0.0.
            - If greater than 100.0, returns 100.0.
            - Otherwise, returns the float value.

    Returns:
        float: Normalized percentage value between 0.0 and 100.0.
        None: If the input is None or invalid.

    """
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(f):
        return None
    return min(100.0, max(0.0, f))


def _to_uint(value):
    """Normalize an integer to a non-negative integer.

    Args:
        value (int | None): Input integer value.
            - If None, returns None.
            - If not an integer or cannot be converted to int, returns None.
            - If less than 0, returns 0.
            - Otherwise, returns the integer value.

    Returns:
        int: Non-negative integer value.
        None: If the input is None or invalid.

    """
    if value is None:
        return None
    try:
        n = int(value)
    except (TypeError, ValueError):
        return None
    return 0 if n < 0 else n


def _to_epoch(value):
    """Normalize int/float/datetime/ISO-8601 string to epoch seconds (int).

    Args:
        value (int, float, datetime, str, None): Input value to normalize.
            - If None, returns current UTC epoch time.
            - If int or float, returns int(value).
            - If datetime, returns int(value.timestamp()).
            - If str, attempts to parse as ISO-8601 datetime and returns
              int(parsed_datetime.timestamp()).

    Returns:
        int: Epoch time in seconds.

    """
    if value is None:
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    if isinstance(value, (int, float)):
        f = float(value)
        if not math.isfinite(f):
            raise TypeError("Invalid last_polled float")  # noqa: TRY003
        return max(0, int(f))
    if isinstance(value, datetime.datetime):
        dt = value
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
        return max(0, int(dt.timestamp()))
    if isinstance(value, str):
        try:
            s = value.strip()
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"
            dt = datetime.datetime.fromisoformat(s)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            return max(0, int(dt.timestamp()))
        except ValueError as exc:
            raise TypeError("Invalid last_polled ISO-8601 string") from exc
    raise TypeError("Invalid type for last_polled")  # noqa: TRY003


def insert_row(rows):
    """Insert rows into smap_device_metrics_history (historical metrics).

    Args:
        rows (list or object): Single row or list of rows to insert. Each row is
            expected to have the following attributes:
                - hostname (str or None): Device hostname
                - last_polled (int, float, datetime, str, or None):
                  Timestamp of last poll
                - uptime (int or None): Device uptime in seconds
                - cpu_utilization (float or None): CPU utilization percentage
                - memory_utilization (float or None): Memory utilization in %

    Returns:
        None

    """
    if isinstance(rows, Iterable) and not isinstance(
        rows, (str, bytes, bytearray, dict)
    ):
        rows = list(rows)
    else:
        rows = [rows]

    inserts = []
    for row in rows:

        # Validate/encode hostname (VARBINARY NOT NULL)
        if getattr(row, "hostname", None) is None:
            raise ValueError("hostname is required for DeviceMetricsHistory")
        _host = (
            row.hostname.encode("utf-8")
            if isinstance(row.hostname, str)
            else (
                bytes(row.hostname)
                if isinstance(row.hostname, (bytes, bytearray))
                else None
            )
        )
        if _host is None:
            raise TypeError("hostname must be str or bytes")  # noqa: TRY003
        if len(_host) > 256:
            raise ValueError("hostname exceeds 256 bytes")  # noqa: TRY003
        inserts.append(
            {
                "hostname": _host,
                "last_polled": _to_epoch(getattr(row, "last_polled", None)),
                "uptime": _to_uint(getattr(row, "uptime", None)),
                "cpu_utilization": _pct(getattr(row, "cpu_utilization", None)),
                "memory_utilization": _pct(
                    getattr(row, "memory_utilization", None)
                ),
            }
        )

    if inserts:
        db.db_insert_row(2000, _DeviceMetricsHistory, inserts)
