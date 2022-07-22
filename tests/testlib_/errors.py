"""Module for application test error management."""

from __future__ import print_function
import os
import inspect
import re
import sys
import collections


def check_source_code(root, minimum=0, maximum=0):
    """Get all the error codes.

    Args:
        root: Root directory from which to search for error codes
        minimum: Minimum error code value to be found
        maximum: Maximum error code value to be found

    Returns:
        None

    """
    # Make sure minimum < maximum
    if minimum > maximum:
        log_message = """\
Minimum value {} is greater than {}. Please fix.\
""".format(
            minimum, maximum
        )
        print(log_message)
        sys.exit(2)

    # Define where the application lives
    ignore_paths = [
        "{0}.git{0}".format(os.sep),
        "{0}__pycache__{0}".format(os.sep),
        ".egg",
        "{0}docs{0}".format(os.sep),
        "{0}var{0}".format(os.sep),
    ]
    error_functions = (
        "log2die_safe(",
        "log2warning(",
        "log2exception(",
        "log2exception_die(",
        "log2debug(",
        "log2live(",
        "log2warn(",
        "log2die(",
        "log2quiet(",
        "log2info(",
        "log2screen(",
        "log2see(",
        r".modify(",
        r".query(",
        r"db.replace(",
        ".add_all(",
        r".db_modify(",
        r".db_query(",
        r".db_commit(",
        r".db_replace(",
        r".db_add(",
        ".db_add_all(",
        r".db_select(",
        r".db_delete(",
        r".db_update(",
        ".db_select_row(",
        r".db_modify(",
        r".db_query(",
    )
    error_codes = []
    available_codes = []
    entries = 5
    status = {}

    # Get ready to ignore this script
    this_script = os.path.abspath(inspect.getfile(inspect.currentframe()))
    ignore_paths.append(this_script)

    # Compile regex to be used to find functions with error codes
    to_find = _wordlist_to_regex(error_functions)

    # Get a recursive listing of files
    python_files = _files(root, ignore_paths)

    # Read each file to find error codes
    for python_file in python_files:
        metadata = _codes(python_file, to_find)
        error_codes.extend([x.code for x in metadata])
        for item in metadata:
            line = [
                """\
    file: {}
    line: {}
    text: {}""".format(
                    item.filename, item.number, item.line
                )
            ]
            value = status.get(item.code)
            if value is None:
                status[item.code] = line
            else:
                status[item.code].extend(line)

    # Get duplicate codes
    _duplicates = [
        item for item, count in collections.Counter(error_codes).items() if count > 1
    ]
    _duplicates.sort()
    if len(_duplicates) > entries:
        duplicates = "{} plus {} more...".format(
            _duplicates[0:entries], len(_duplicates) - entries
        )
    else:
        duplicates = _duplicates

    # Determine whether codes are in range (MAX)
    code_max = max(error_codes)
    if int(code_max) > maximum:
        log_message = """\
Extremely large error code {} found. Must be less than {}. Please fix.
""".format(
            code_max, maximum
        )
        print(log_message)

        # Print line information
        for item in status[code_max]:
            print(item)
        sys.exit(2)

    # Determine whether codes are in range (MIN)
    code_min = min(error_codes)
    if int(code_min) < minimum:
        log_message = """\
Extremely small error code {} found. Must be greater than {}. Please fix.
""".format(
            code_min, minimum
        )
        print(log_message)

        # Print line information
        for item in status[code_min]:
            print(item)
        sys.exit(2)

    # Process error codes
    for next_code in range(min(error_codes), code_max):
        if next_code not in error_codes:
            available_codes.append(next_code)

    # Get available codes
    if bool(available_codes) is False:
        available_codes = list(range(max(error_codes), max(error_codes) + entries + 1))

    # Print report
    print(
        """
Application Logging Error Code Summary Report
---------------------------------------------
Starting Code              : {}
Ending Code                : {}
Duplicate Codes to Resolve : {}
Available Codes            : {}
Status                     : {}\
""".format(
            min(error_codes),
            max(error_codes),
            duplicates,
            available_codes[0:entries],
            "OK" if bool(duplicates) is False else "Error",
        )
    )

    # Exit with error if duplicate codes found
    if bool(_duplicates) is True:
        for next_duplicate in _duplicates:
            print(
                """
-----------------------------------
Duplicates for code        : {}
""".format(
                    next_duplicate
                )
            )
            for item in status[next_duplicate]:
                print("{}".format(item))
        sys.exit(1)

    # Exit with error if code values are out of range
    if (min(error_codes) < minimum) or (max(error_codes) > maximum):
        print(
            """

ERROR: Error codes values out of range {} to {}. Please resolve.

""".format(
                minimum, maximum
            )
        )
        sys.exit(1)


def _codes(filename, to_find):
    """Get a list of codes found in a file.

    Args:
        filename: Name of file
        to_find: Compiled list of functions to search for

    Returns:
        error_codes: List of error codes

    """
    # Initalize key variables
    digits = re.compile(r"^.*?(\d+).*?$")
    metadata = []
    Metadata = collections.namedtuple("Metadata", "filename, line, number, code")

    # Process file for codes
    with open(filename, "r") as lines:
        # Read each line of the file
        count = 0
        for line in lines:
            # Increment count
            count += 1

            # Ignore lines without a '(' in it
            if "(" not in line:
                continue

            # Ignore lines starting with comments
            if line.strip().startswith("#"):
                continue

            match_obj = to_find.search(line)
            if bool(match_obj) is True:
                # Search for digits in the arguments of the functions
                # in the error_functions
                components = line.split("(")
                arguments = " ".join(components[1:])
                found = digits.match(arguments)
                if bool(found) is True:
                    code_value = int(found.group(1))
                    metadata.append(
                        Metadata(
                            filename=filename, line=line, number=count, code=code_value
                        )
                    )

    # Return
    return metadata


def _wordlist_to_regex(words):
    """Convert word list to a regex expression, escaping characters if needed.

    Args:
        words: List of words

    Returns:
        result: Compiled regex

    """
    escaped = map(re.escape, words)
    combined = "|".join(sorted(escaped, key=len, reverse=True))
    result = re.compile(combined)
    return result


def _files(root, ignore_paths):
    """Get a recursive list of python files under a root directory.

    Args:
        root: Root directory
        ignore_paths: List of paths to ignore

    Returns:
        python_files: List of paths to python files

    """
    # Define where application lives
    python_files = []

    # Get a recursive listing of files
    for directory, _, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(directory, filename)

            # Ignore pre-defined file extensions
            if file_path.endswith(".py") is False:
                continue

            # Ignore pre-defined paths
            ignored = False
            for ignore_path in ignore_paths:
                if ignore_path in file_path:
                    ignored = True
            if ignored is False:
                python_files.append(file_path)

    # Return
    return python_files
