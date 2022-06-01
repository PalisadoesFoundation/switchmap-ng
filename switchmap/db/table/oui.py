#!/usr/bin/env python3
"""Pattoo classes querying the Language table."""

from collections import namedtuple

# Import project libraries
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import Language


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_language

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20046) as session:
        rows = session.query(Language.idx_language).filter(
            Language.idx_language == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(code):
    """Determine whether code exists in the Language table.

    Args:
        code: language code

    Returns:
        result: Language.idx_language value

    """
    # Initialize key variables
    result = False
    rows = []

    # Lowercase the code
    code = code.lower().strip()

    # Get code from database
    with db.db_query(20038) as session:
        rows = session.query(Language.idx_language).filter(
            Language.code == code.encode())

    # Return
    for row in rows:
        result = row.idx_language
        break
    return result


def insert_row(code, name=''):
    """Create a Language table entry.

    Args:
        code: Language code
        name: Language code name

    Returns:
        None

    """
    # Verify values
    if bool(name) is False or isinstance(name, str) is False:
        name = 'Change me. Language name not provided.'
    if bool(code) is False or isinstance(code, str) is False:
        log_message = 'Language code "{}" is invalid'.format(code)
        log.log2die(20069, log_message)

    # Lowercase the code
    code = code.strip().lower()[:MAX_KEYPAIR_LENGTH]
    name = name.strip()[:MAX_KEYPAIR_LENGTH]

    # Insert
    row = Language(code=code.encode(), name=name.encode())
    with db.db_modify(20055, die=True) as session:
        session.add(row)


def update_name(code, name):
    """Upadate a Language table entry.

    Args:
        code: Language code
        name: Language code name

    Returns:
        None

    """
    # Update
    code = code.strip().lower()
    with db.db_modify(20048, die=False) as session:
        session.query(Language).filter(
            Language.code == code.encode()).update(
                {'name': name.strip().encode()}
            )


def cli_show_dump():
    """Get entire content of the table.

    Args:
        None

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []

    # Get the result
    with db.db_query(20049) as session:
        rows = session.query(Language)

    # Process
    for row in rows:
        Record = namedtuple('Record', 'idx_language code name')
        result.append(
            Record(
                idx_language=row.idx_language,
                name=row.name.decode(),
                code=row.code.decode()))
    return result
