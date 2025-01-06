import os
import re
import sys
from docstring_parser import parse


def validate_docstring(file_path):
    """
    Validate docstrings in a file for compliance with the Google style guide.
    Args:
        file_path (str): Path to the Python file to validate.
    Returns:
        list: List of violations found in the file, with details about the issue and corrective action.
    """
    print(f"Validating file: {file_path}")
    violations = []

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Failed to read file {file_path}: {e}")
        return violations

    for i, line in enumerate(lines):
        if re.match(r"^\s*def ", line):
            func_name = line.strip()
            print(f"Found function definition at line {i + 1}: {func_name}")

            docstring_start = i + 1
            while (
                docstring_start < len(lines)
                and lines[docstring_start].strip() == ""
            ):
                docstring_start += 1

            if docstring_start < len(lines) and lines[
                docstring_start
            ].strip().startswith('"""'):
                print(f"Docstring starts at line {docstring_start + 1}")
                docstring_end = docstring_start + 1
                while docstring_end < len(lines) and not lines[
                    docstring_end
                ].strip().endswith('"""'):
                    docstring_end += 1

                if docstring_end < len(lines):
                    docstring = "\n".join(
                        lines[docstring_start : docstring_end + 1]
                    )
                    print(
                        f"Extracted docstring from lines {docstring_start + 1} to {docstring_end + 1}"
                    )

                    try:
                        parsed = parse(docstring)
                        print("Parsed docstring successfully")

                        # Check for Args section
                        if not parsed.params and "Args:" not in docstring:
                            print("Missing 'Args' section")
                            violations.append(
                                {
                                    "line": i + 1,
                                    "function": func_name,
                                    "issue": "Missing 'Args' section",
                                    "action": "Add an 'Args' section listing the arguments this function accepts, their types, and descriptions.",
                                }
                            )

                        # Check for Returns section
                        if not parsed.returns and "Returns:" not in docstring:
                            print("Missing 'Returns' section")
                            violations.append(
                                {
                                    "line": i + 1,
                                    "function": func_name,
                                    "issue": "Missing 'Returns' section",
                                    "action": "Add a 'Returns' section describing the return value, its type, and meaning.",
                                }
                            )

                        # Treat explicit None as compliant
                        if (
                            parsed.returns
                            and parsed.returns.type == "None"
                            and parsed.returns.description == "None"
                        ):
                            violations = [
                                v
                                for v in violations
                                if v.get("issue")
                                != "Missing 'Returns' section"
                            ]
                        if all(
                            p.type == "None" and p.description == "None"
                            for p in parsed.params
                        ):
                            violations = [
                                v
                                for v in violations
                                if v.get("issue") != "Missing 'Args' section"
                            ]

                    except Exception as e:
                        print(f"Error parsing docstring: {e}")
                        violations.append(
                            {
                                "line": i + 1,
                                "function": func_name,
                                "issue": "Docstring parsing error",
                                "action": f"Ensure the docstring is properly formatted: {e}",
                            }
                        )
                else:
                    print("Docstring does not close properly")
                    violations.append(
                        {
                            "line": i + 1,
                            "function": func_name,
                            "issue": "Unclosed docstring",
                            "action": "Ensure the docstring is properly closed with triple quotes.",
                        }
                    )
            else:
                print("Missing docstring for function")
                violations.append(
                    {
                        "line": i + 1,
                        "function": func_name,
                        "issue": "Missing docstring",
                        "action": "Add a Google-style docstring to describe this function.",
                    }
                )

    print(f"Found {len(violations)} violations in file: {file_path}")
    return violations


def check_directory(directory, exclude_dirs=None):
    """
    Check all Python files in a directory for docstring compliance, excluding specified directories.

    Args:
        directory (str): Directory to scan.
        exclude_dirs (list): List of directories to exclude.

    Returns:
        dict: Dictionary of file violations.
    """
    if exclude_dirs is None:
        exclude_dirs = []

    all_violations = {}
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [
            d for d in dirs if os.path.join(root, d) not in exclude_dirs
        ]

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                violations = validate_docstring(file_path)
                if violations:
                    all_violations[file_path] = violations

    print(f"Completed scanning directory: {directory}")
    return all_violations


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    # Define excluded directories (e.g., virtual environment or library folders)
    exclude_dirs = [
        os.path.join(directory, "venv"),
        os.path.join(directory, "lib"),
        os.path.join(directory, "venv/lib/python3.11/site-packages"),
        os.path.join(directory, "tests"),
    ]
    violations = check_directory(directory, exclude_dirs=exclude_dirs)
    if violations:
        print("Docstring violations found:")
        for file, issues in violations.items():
            for issue in issues:
                print(
                    f"{file}:{issue['line']}: {issue['function']}: {issue['issue']}"
                )
                print(f"  Corrective Action: {issue['action']}")
        sys.exit(1)
    else:
        print("All docstrings are compliant.")


if __name__ == "__main__":
    main()
