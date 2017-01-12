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

# switchmap-ng libraries
try:
    from switchmap.utils import general
except:
    print('You need to set your PYTHONPATH to include the switchmap library')
    sys.exit(2)
from switchmap.test import unittest_setup


def main():
    """Test all the switchmap-ng modules with unittests.

    Args:
        None

    Returns:
        None

    """
    # Determine unittest directory
    root_dir = general.root_directory()
    test_dir = ('%s/switchmap/test') % (root_dir)

    # Get list of test files
    test_files = os.listdir(test_dir)
    for filename in sorted(test_files):
        full_path = ('%s/%s') % (test_dir, filename)

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
    slurpy_returncode = ('----- switchmap-ng Return Code '
                         '----------------------------------------')
    slurpy_stdoutdata = ('----- switchmap-ng Test Output '
                         '----------------------------------------')
    slurpy_stderrdata = ('----- switchmap-ng Test Error '
                         '-----------------------------------------')

    # Say what we are doing
    string2print = ('\nRunning Command: %s') % (cli_string)
    print(string2print)

    # Run update_devices script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    process = subprocess.Popen(
        do_command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdoutdata, stderrdata = process.communicate()
    returncode = process.returncode

    # Crash if the return code is not 0
    if returncode != 0:
        # Print the Return Code header
        string2print = ('\n%s') % (slurpy_returncode)
        print(string2print)

        # Print the Return Code
        string2print = ('\n%s') % (returncode)
        print(string2print)

        # Print the STDOUT header
        string2print = ('\n%s\n') % (slurpy_stdoutdata)
        print(string2print)

        # Print the STDOUT
        for line in stdoutdata.decode(encoding).split('\n'):
            string2print = ('%s') % (line)
            print(string2print)

        # Print the STDERR header
        string2print = ('\n%s\n') % (slurpy_stderrdata)
        print(string2print)

        # Print the STDERR
        for line in stderrdata.decode(encoding).split('\n'):
            string2print = ('%s') % (line)
            print(string2print)

        # All done
        sys.exit(2)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_setup.ready()

    # Do the unit test
    main()
