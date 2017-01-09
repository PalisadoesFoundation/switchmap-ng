#!/usr/bin/env python3
"""Test the general module."""

import unittest
import shutil
import random
import os
import string

from switchmap.utils import general as testimport


class KnownValues(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = ''.join([random.choice(
        string.ascii_letters + string.digits) for n in range(9)])

    def test_dict2yaml(self):
        """Testing method / function dict2yaml."""
        # Initializing key variables
        data_dict = {
            '1': 'test 1',
            'two': 'test 2'
        }
        data_yaml = """'1': test 1
two: test 2
"""
        # Do test with good dict
        yaml_result = testimport.dict2yaml(data_dict)
        self.assertEqual(yaml_result, data_yaml)

    def test_delete_files(self):
        """Testing function delete_files."""
        # Initialize key variables
        complete_filenames = {}

        #################################################
        # Test with invalid directory
        #################################################

        invalid_path = ('/tmp/%s.%s') % (
            self.random_string,
            self.random_string)

        with self.assertRaises(SystemExit):
            testimport.delete_files(invalid_path)

        #################################################
        # Test with valid directory
        #################################################

        # Create a test directory
        path = ('/tmp/%s') % (self.random_string)
        if os.path.exists(path) is False:
            os.makedirs(path)

        # Place files in the directory
        for count in range(0, 4):
            filename = ''.join([random.choice(
                string.ascii_letters + string.digits) for n in range(15)])
            complete_filenames[count] = ('%s/%s') % (path, filename)
            open(complete_filenames[count], 'a').close()

            # Check files in directory
            self.assertEqual(os.path.isfile(complete_filenames[count]), True)

        # Delete files in directory
        testimport.delete_files(path)

        # Check that files were deleted
        for filename in complete_filenames.values():
            self.assertEqual(os.path.isfile(filename), False)

        # Delete directory
        shutil.rmtree(path)

    def test_cleanstring(self):
        """Testing method / function cleanstring."""
        # Initializing key variables
        dirty_string = ('   %s\n   \r %s   \n %s  ') % (
            self.random_string, self.random_string, self.random_string)
        clean_string = ('%s %s %s') % (
            self.random_string, self.random_string, self.random_string)

        # Test result
        result = testimport.cleanstring(dirty_string)
        self.assertEqual(result, clean_string)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
