#!/usr/bin/env python3
"""Test the jm_general module."""

import unittest
import shutil
import random
import os
import string

from switchmap.utils import jm_general as testimport


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

    def test_move_files(self):
        """Testing function move_files."""
        # Initialize key variables
        source_filenames = {}
        target_filenames = {}

        #################################################
        # Test with invalid source directory
        #################################################

        invalid_path = ('/tmp/%s.%s') % (
            self.random_string,
            self.random_string)

        with self.assertRaises(SystemExit):
            testimport.move_files(invalid_path, '/tmp')

        #################################################
        # Test with invalid destination directory
        #################################################

        invalid_path = ('/tmp/%s.%s') % (
            self.random_string,
            self.random_string)

        with self.assertRaises(SystemExit):
            testimport.move_files('/tmp', invalid_path)

        #################################################
        # Test with valid directory
        #################################################

        # Create a source directory
        source_dir = ('/tmp/%s.1') % (self.random_string)
        if os.path.exists(source_dir) is False:
            os.makedirs(source_dir)

        # Create a target directory
        target_dir = ('/tmp/%s.2') % (self.random_string)
        if os.path.exists(target_dir) is False:
            os.makedirs(target_dir)

        # Place files in the directory
        for count in range(0, 4):
            filename = ''.join([random.choice(
                string.ascii_letters + string.digits) for n in range(15)])
            source_filenames[count] = ('%s/%s') % (source_dir, filename)
            target_filenames[count] = ('%s/%s') % (target_dir, filename)
            open(source_filenames[count], 'a').close()

            # Check files in directory
            self.assertEqual(os.path.isfile(source_filenames[count]), True)

        # Delete files in directory
        testimport.move_files(source_dir, target_dir)

        # Check that files are not in source_dir
        for filename in source_filenames.values():
            self.assertEqual(os.path.isfile(filename), False)

        # Check that files are in in target_dir
        for filename in target_filenames.values():
            self.assertEqual(os.path.isfile(filename), True)

        # Delete directory
        shutil.rmtree(source_dir)

        # Delete directory
        shutil.rmtree(target_dir)

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
