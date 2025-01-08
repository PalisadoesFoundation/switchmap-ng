#!/usr/bin/env python3
"""Script to check for docstrings."""

import os
import re
import sys
import argparse
from collections import namedtuple
from docstring_parser import parse

Violation = namedtuple("Violation", ["line", "function", "issue", "action"])


def validate_docstring(file_path):
    """Validate docstrings in a file for compliance with the Google style guide.

    Args:
        file_path (str): Path to the Python file to validate.

    Returns:
        list: List of violations found in the file, with details about
            the issue and corrective action.

    """
    # Initialize key variables
    violations = []

    # Read the file for processing
    try:
        with open(file_path, "r", encoding="utf-8") as fh_:
            lines = fh_.readlines()

    except Exception as _:
        return violations

    # Evaluate each line
    for line_number, line in enumerate(lines):

        # Identify sections of the file that are functions or methods
        if re.match(r"^\s*def ", line):
            # Get arguments
            function = extract_arguments(line_number, lines)

            # Get the docstring
            docstring = extract_docstring(function.name, line_number, lines)

            # Evaluate the
            if bool(docstring.violations) is False:
                # Check arguments arguments that are not None
                for argument in function.arguments:
                    # Track whether the argument is defined
                    # in the docstring parameters
                    found_in_params = False

                    if bool(argument) is True:
                        found_in_arguments = False
                        for parameter in docstring.parser.params:
                            if argument in parameter.arg_name:
                                found_in_params = True
                            if parameter.arg_name in function.arguments:
                                found_in_arguments = True

                        # Error if the parameter is not found
                        if bool(found_in_arguments) is False:
                            violations.append(
                                Violation(
                                    line=line_number + 1,
                                    function=function.name,
                                    issue=f"""\
Argument '{argument}' defined in the docstring is not an argument""",
                                    action=f"""\
Remove argument '{argument}' from the docstring""",
                                )
                            )

                        # Error if the argument is not found
                        if bool(found_in_params) is False:
                            violations.append(
                                Violation(
                                    line=line_number + 1,
                                    function=function.name,
                                    issue=f"""\
Argument '{argument}' not defined in docstring""",
                                    action=f"""\
Add argument '{argument}' to the docstring""",
                                )
                            )
                    else:
                        print(function.name)

            else:
                # Add the violation to the list
                violations.extend(docstring.violations)

    # Return
    return violations


def extract_arguments(start, lines):
    """Extract the docstring from a list of lines read from a file.

    Args:
        start: Starting line to process
        stop: Ending line to process
        lines: The file as a list of strings split by a new line separator

    Returns:
        result: Function object

    """
    # Initialize key variables
    func = ""
    possibles = lines[start:]
    arguments = []
    Function = namedtuple("Function", "name arguments")

    # Process the function
    for line in possibles:
        if bool(line) is False:
            continue
        elif ("'''" not in line) and ('"""' not in line):
            func = f"{func}{line.strip()}"
        else:
            break

    # Get the arguments
    items = func.split("(")[1].split(",")
    name = func.split()[1].split("(")[0].strip()
    for item in items:
        result = item.split(")")[0].split("=")[0].strip()
        arguments.append(result if bool(result) else None)

    # Fix arguments
    if bool(arguments) and ("self" in arguments):
        arguments.remove("self")

    # Return
    result = Function(name=name, arguments=arguments)
    return result


def extract_docstring(func_name, line_number, lines):
    """Extract the docstring from a list of lines read from a file.

    Args:
        line_number: Line where the docstring starts
        lines: The file as a list of strings split by a new line separator
        func_name: Name of the function for the docstring

    Returns:
        result: namedtuple containing the docstring, and status

    """
    # Initialize key variables
    violations = []
    parser = None
    Docstring = namedtuple("Docstring", "violations docstring parser")
    docstring = ""

    # Process Docstring
    docstring_start = line_number + 1
    while (
        docstring_start < len(lines) and lines[docstring_start].strip() == ""
    ):
        docstring_start += 1

    # Identify the start of the Docstring
    if docstring_start < len(lines) and lines[
        docstring_start
    ].strip().startswith('"""'):

        # Identify the end of the docstring
        docstring_end = docstring_start + 1
        while docstring_end < len(lines) and not lines[
            docstring_end
        ].strip().endswith('"""'):
            docstring_end += 1

        # Extract lines within the docstring area
        if docstring_end < len(lines):
            # Swap "None" arguments with "None:" that can be parsed
            fixed_lines = lines[docstring_start : docstring_end + 1]
            for key, item in enumerate(fixed_lines):
                if item.strip == "None":
                    fixed_lines[key].replace("None", "None:")

            # Convert the docstring lines to a string
            docstring = "\n".join(
                fixed_lines[docstring_start : docstring_end + 1]
            )

            # Parse the docstring
            try:
                parser = parse(docstring)

            except Exception as e:
                violations.append(
                    Violation(
                        line=line_number + 1,
                        function=func_name,
                        issue="Docstring parsing error",
                        action=f"""\
Ensure the docstring is properly formatted: {e}""",
                    )
                )

            # Check for Args section
            if "Args:" not in docstring:
                violations.append(
                    Violation(
                        line=line_number + 1,
                        function=func_name,
                        issue="Missing 'Args' section",
                        action="""\
Add an 'Args' section listing the arguments this function accepts.""",
                    )
                )

            # Check for Returns section
            if "Returns:" not in docstring:
                violations.append(
                    Violation(
                        line=line_number + 1,
                        function=func_name,
                        issue="Missing 'Returns' section",
                        action="""\
Add a 'Returns' section describing the return value.""",
                    )
                )

            # Ensure there is an Args section
            if bool(parser.params) is False:
                violations.append(
                    Violation(
                        line=line_number + 1,
                        function=func_name,
                        issue="Docstring has no 'Args:' section",
                        action="""\
Add an 'Args:' section to the function docstring""",
                    )
                )

            # Ensure there is an Returns section
            if bool(parser.returns) is False:
                violations.append(
                    Violation(
                        line=line_number + 1,
                        function=func_name,
                        issue="Docstring has no 'Returns:' section",
                        action="""\
Add an 'Returns:' section to the function docstring""",
                    )
                )

        else:
            violations.append(
                Violation(
                    line=line_number + 1,
                    function=func_name,
                    issue="Unclosed docstring",
                    action="""\
Ensure the docstring is properly closed with triple quotes.""",
                )
            )

    else:
        violations.append(
            Violation(
                line=line_number + 1,
                function=func_name,
                issue="Missing docstring",
                action="""\
Add a Google-style docstring to describe this function.""",
            )
        )

    # Return result
    result = Docstring(
        docstring=docstring,
        violations=violations if bool(violations) else None,
        parser=parser,
    )
    return result


def check_directory(directory, exclude_dirs=None):
    """Check all Python files in a directory for docstring compliance.

    Specified directories are excluded.

    Args:
        directory (str): Directory to scan.
        exclude_dirs (list): List of directories to exclude.

    Returns:
        dict: Dictionary of file violations.
    """
    # Initialize key variables
    all_violations = {}
    _exclude_dirs = exclude_dirs if bool(exclude_dirs) else []

    # Recursive directory search for files
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [
            d for d in dirs if os.path.join(root, d) not in _exclude_dirs
        ]

        # Process files in each directory
        for file in files:
            if file.endswith(".py"):
                # Print start of processing
                file_path = os.path.join(root, file)

                # Identify violations in the file
                violations = validate_docstring(file_path)

                # Add any found violations
                if violations:
                    all_violations[file_path] = violations

    # Return
    return all_violations


def main():
    """Start checking the docstrings.

    Args:
        None

    Returns:
        None
    """
    # Header for the help menu of the application
    parser = argparse.ArgumentParser(
        description="""\
This script checks specified directories for compliance with the \
Google Docstring 'Args' and 'Returns' sections.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # CLI argument for starting
    parser.add_argument(
        "--directories",
        required=False,
        default=".",
        nargs="+",
        type=str,
        help="Directory where the cache files are located.",
    )
    args = parser.parse_args()

    # Process the directories
    for directory in args.directories:
        # Define excluded directories
        # (e.g., virtual environment or library folders)
        exclude_dirs = [
            os.path.join(directory, "venv"),
            os.path.join(directory, "lib"),
            os.path.join(directory, "venv/lib/python3.11/site-packages"),
            os.path.join(directory, "tests"),
            os.path.join(directory, "switchmap/poller/snmp"),
            os.path.join(directory, "switchmap/server/db/ingest"),
            os.path.join(directory, "switchmap/server/db/ingest/update"),
        ]

        # Identify violations
        violations = check_directory(directory, exclude_dirs=exclude_dirs)

        # Create a message for the violation
        if violations:
            for file, issues in violations.items():
                for issue in issues:
                    print(
                        f"""\
Error: {file}
Line : {issue.line}
Function: {issue.function}
Issue: {issue.issue}
Corrective Action: {issue.action}
"""
                    )
                    pass

            sys.exit(1)
        else:
            print(f"OK: Directory {directory}")


if __name__ == "__main__":
    main()
