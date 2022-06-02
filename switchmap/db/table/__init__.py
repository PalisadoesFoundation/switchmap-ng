"""Constants required for DB queries and updates."""

from collections import namedtuple

ROUI = namedtuple(
    'ROUI', 'idx_oui oui organization enabled ts_modified ts_created')
IOUI = namedtuple(
    'IOUI', 'oui organization enabled')
