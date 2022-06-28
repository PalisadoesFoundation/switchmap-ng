#!/usr/bin/env python3
"""Script to test all the switchmap-ng unittests.

1)  This script runs each unittest script in switchmap-ng's
    switchmap.test module.

2)  The only scripts run in the module are those whose names
    start with 'test_'

3)  The unittests will only run on a test database whose name
    starts with 'test_'

4)  All unittest scripts must be able to successfully run independently
    of all others.

"""

import locale
import os
import sys
import subprocess
import argparse

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}switchmap-ng{0}tests{0}bin'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)


# Import application libraries
from tests.testlib_ import setup


def main():
    """Test all the switchmap-ng modules with unittests.

    Args:
        None

    Returns:
        None

    """
    # Determine unittest directory
    test_dir = '{0}{1}tests{1}switchmap_'.format(ROOT_DIR, os.sep)

    # Set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', help='', action='store_true')
    args = parser.parse_args()

    # Check error codes
    command = (
        '{1}{0}tests{0}bin{0}error_code_report.py'.format(os.sep, ROOT_DIR))
    run_script(command)

    # Run the test
    command = '''\
python3 -m unittest discover --verbose --start {}'''.format(test_dir)
    if args.verbose is True:
        command = '{} --verbose'.format(command)
    run_script(command)

    # Get list of test files
    test_files = os.listdir(test_dir)
    for filename in sorted(test_files):
        full_path = '{}/{}'.format(test_dir, filename)

        # Run the test
        if filename.startswith('test_'):
            run_script(full_path)

    # Print
    message = ('\nHooray - All Done OK!\n')
    print(message)


def run_script(cli_string):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    encoding = locale.getdefaultlocale()[1]
    test_returncode = (
        '----- Test Error Return Code -----------------------------')
    test_stdoutdata = (
        '----- Test Output ----------------------------------------')
    test_stderrdata = (
        '----- Test Error -----------------------------------------')

    # Say what we are doing
    string2print = '\nRunning Command: {}'.format(cli_string)
    print(string2print)

    # Run update_devices script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    with subprocess.Popen(
            do_command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE) as process:
        stdoutdata, stderrdata = process.communicate()
        returncode = process.returncode

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        string2print = '\n{}'.format(test_returncode)
        print(string2print)

        # Print the Return Code
        string2print = '\n{}'.format(returncode)
        print(string2print)

        # Print the STDOUT header
        string2print = '\n{}\n'.format(test_stdoutdata)
        print(string2print)

        # Print the STDOUT
        for line in stdoutdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # Print the STDERR header
        string2print = '\n{}\n'.format(test_stderrdata)
        print(string2print)

        # Print the STDERR
        for line in stderrdata.decode(encoding).split('\n'):
            string2print = '{}'.format(line)
            print(string2print)

        # All done
        sys.exit(2)


if __name__ == '__main__':
    # Create configuration
    config = setup.config()
    config.save()

    # Do the unit test
    main()

    # Cleanup
    config.cleanup()
