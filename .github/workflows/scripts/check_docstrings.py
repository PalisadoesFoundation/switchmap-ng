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
    violations = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if re.match(r'^\\s*def ', line):
            func_name = line.strip()
            docstring_start = i + 1
            while docstring_start < len(lines) and lines[docstring_start].strip() == '':
                docstring_start += 1

            if docstring_start < len(lines) and lines[docstring_start].strip().startswith('\"\"\"'):
                docstring_end = docstring_start + 1
                while docstring_end < len(lines) and not lines[docstring_end].strip().endswith('\"\"\"'):
                    docstring_end += 1

                docstring = '\\n'.join(lines[docstring_start:docstring_end + 1])
                try:
                    parsed = parse(docstring)
                    # Check for Raises section
                    if not parsed.raises:
                        violations.append({
                            "line": i + 1,
                            "function": func_name,
                            "issue": "Missing 'Raises' section",
                            "action": "Add a 'Raises' section detailing the exceptions this function may raise."
                        })
                    # Check for Args section
                    if not parsed.params:
                        violations.append({
                            "line": i + 1,
                            "function": func_name,
                            "issue": "Missing 'Args' section",
                            "action": "Add an 'Args' section listing the arguments this function accepts, their types, and descriptions."
                        })
                except Exception as e:
                    violations.append({
                        "line": i + 1,
                        "function": func_name,
                        "issue": "Docstring parsing error",
                        "action": f"Ensure the docstring is properly formatted: {e}"
                    })
            else:
                violations.append({
                    "line": i + 1,
                    "function": func_name,
                    "issue": "Missing docstring",
                    "action": "Add a Google-style docstring to describe this function."
                })
    return violations

def check_directory(directory):
    """
    Check all Python files in a directory for docstring compliance.
    
    Args:
        directory (str): Directory to scan.

    Returns:
        dict: Dictionary of file violations.
    """
    all_violations = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                violations = validate_docstring(file_path)
                if violations:
                    all_violations[file_path] = violations
    return all_violations

def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    violations = check_directory(directory)
    if violations:
        print("Docstring violations found:")
        for file, issues in violations.items():
            for issue in issues:
                print(f"{file}:{issue['line']}: {issue['function']}: {issue['issue']}")
                print(f"  Corrective Action: {issue['action']}")
        sys.exit(1)
    else:
        print("All docstrings are compliant.")

if __name__ == "__main__":
    main()
