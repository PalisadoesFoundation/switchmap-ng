#!/usr/bin/env python3
"""Test the files module."""

import unittest
import os
import tempfile
import shutil
import sys
import yaml


# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir
            )
        ),
        os.pardir,
    )
)
_EXPECTED = "{0}switchmap-ng{0}tests{0}switchmap_{0}core".format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)

from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()


from switchmap.core import files


class TestMoveYamlFiles(unittest.TestCase):
    """Test the move_yaml_files function."""

    def setUp(self):
        """Set up the test environment before each test."""
        # Create temporary source and destination directories
        self.src_dir = tempfile.mkdtemp()
        self.dst_dir = tempfile.mkdtemp()
        
        # Create test YAML files in source directory
        self.yaml_files = ['test1.yaml', 'test2.yaml', 'config.yaml']
        self.non_yaml_files = ['test.txt', 'test.json', 'data.csv']
        
        # Create YAML files
        for filename in self.yaml_files:
            filepath = os.path.join(self.src_dir, filename)
            with open(filepath, 'w') as f:
                f.write('key: value\n')
                
        # Create non-YAML files
        for filename in self.non_yaml_files:
            filepath = os.path.join(self.src_dir, filename)
            with open(filepath, 'w') as f:
                f.write('test content\n')

    def tearDown(self):
        """Clean up the test environment after each test."""
        # Remove temporary directories and their contents
        shutil.rmtree(self.src_dir)
        shutil.rmtree(self.dst_dir)

    def test_move_yaml_files(self):
        """Test moving YAML files from source to destination directory."""
        # Execute the function
        files.move_yaml_files(self.src_dir, self.dst_dir)
        
        # Check that YAML files were moved to destination
        for filename in self.yaml_files:
            src_path = os.path.join(self.src_dir, filename)
            dst_path = os.path.join(self.dst_dir, filename)
            
            # YAML file should not exist in source
            self.assertFalse(
                os.path.exists(src_path),
                f"YAML file {filename} still exists in source directory"
            )
            
            # YAML file should exist in destination
            self.assertTrue(
                os.path.exists(dst_path),
                f"YAML file {filename} not found in destination directory"
            )
        
        # Check that non-YAML files remain in source
        for filename in self.non_yaml_files:
            src_path = os.path.join(self.src_dir, filename)
            dst_path = os.path.join(self.dst_dir, filename)
            
            # Non-YAML file should still exist in source
            self.assertTrue(
                os.path.exists(src_path),
                f"Non-YAML file {filename} missing from source directory"
            )
            
            # Non-YAML file should not exist in destination
            self.assertFalse(
                os.path.exists(dst_path),
                f"Non-YAML file {filename} found in destination directory"
            )

    def test_move_yaml_files_empty_source(self):
        """Test moving YAML files from an empty source directory."""
        # Create new empty source directory
        empty_src = tempfile.mkdtemp()
        
        # Execute the function
        files.move_yaml_files(empty_src, self.dst_dir)
        
        # Verify destination directory is empty
        self.assertEqual(
            len(os.listdir(self.dst_dir)),
            0,
            "Destination directory should be empty"
        )
        
        # Cleanup
        shutil.rmtree(empty_src)

    def test_move_yaml_files_no_yaml(self):
        """Test moving YAML files when source has no YAML files."""
        # Create directory with only non-YAML files
        no_yaml_src = tempfile.mkdtemp()
        
        # Create some non-YAML files
        for filename in ['test.txt', 'data.json']:
            filepath = os.path.join(no_yaml_src, filename)
            with open(filepath, 'w') as f:
                f.write('test content\n')
        
        # Execute the function
        files.move_yaml_files(no_yaml_src, self.dst_dir)
        
        # Verify destination directory is empty
        self.assertEqual(
            len(os.listdir(self.dst_dir)),
            0,
            "Destination directory should be empty"
        )
        
        # Verify source files weren't moved
        self.assertEqual(
            len(os.listdir(no_yaml_src)),
            2,
            "Source directory should still contain its files"
        )
        
        # Cleanup
        shutil.rmtree(no_yaml_src)



class TestYamlReading(unittest.TestCase):
    """Test the YAML file reading functions."""

    def setUp(self):
        """Set up the test environment before each test."""
        # Create temporary test directory
        self.test_dir = tempfile.mkdtemp()
        self.test_dir_2 = tempfile.mkdtemp()
        
        # Sample YAML contents
        self.yaml_content1 = {
            'server': {
                'host': 'localhost',
                'port': 8080
            },
            'database': {
                'name': 'testdb',
                'user': 'admin'
            }
        }
        
        self.yaml_content2 = {
            'logging': {
                'level': 'INFO',
                'file': '/var/log/app.log'
            },
            'cache': {
                'enabled': True,
                'timeout': 300
            }
        }
        
        # Create test YAML files
        self.yaml_file1 = os.path.join(self.test_dir, 'config1.yaml')
        with open(self.yaml_file1, 'w') as f:
            yaml.dump(self.yaml_content1, f)
            
        self.yaml_file2 = os.path.join(self.test_dir, 'config2.yaml')
        with open(self.yaml_file2, 'w') as f:
            yaml.dump(self.yaml_content2, f)

    def tearDown(self):
        """Clean up the test environment after each test."""
        # Remove temporary directories and their contents
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.test_dir_2)

    def test_read_yaml_file_as_dict(self):
        """Test reading a single YAML file as dictionary."""
        # Test reading valid YAML file
        result = files.read_yaml_file(self.yaml_file1)
        self.assertEqual(result, self.yaml_content1)
        
        # Verify the structure
        self.assertIn('server', result)
        self.assertIn('database', result)
        self.assertEqual(result['server']['port'], 8080)

    def test_read_yaml_file_as_string(self):
        """Test reading a single YAML file as string."""
        result = files.read_yaml_file(self.yaml_file1, as_string=True)
        self.assertIsInstance(result, str)
        
        # Verify content can be parsed back to original dict
        parsed_result = yaml.safe_load(result)
        self.assertEqual(parsed_result, self.yaml_content1)

    def test_read_yaml_file_nonexistent(self):
        """Test reading a non-existent YAML file."""
        nonexistent_file = os.path.join(self.test_dir, 'nonexistent.yaml')
        
        # Test with die=False
        result = files.read_yaml_file(nonexistent_file, die=False)
        self.assertEqual(result, {})
        
        # Test with die=True
        with self.assertRaises(SystemExit):
            files.read_yaml_file(nonexistent_file, die=True)

    def test_read_yaml_file_invalid_extension(self):
        """Test reading a file with invalid extension."""
        # Create a text file
        invalid_file = os.path.join(self.test_dir, 'config.txt')
        with open(invalid_file, 'w') as f:
            f.write('invalid: yaml: content')
        
        # Test with die=False
        result = files.read_yaml_file(invalid_file, die=False)
        self.assertEqual(result, {})
        
        # Test with die=True
        with self.assertRaises(SystemExit):
            files.read_yaml_file(invalid_file, die=True)

    def test_read_yaml_files_multiple_directories(self):
        """Test reading YAML files from multiple directories."""
        # Create additional YAML file in second directory
        yaml_file3 = os.path.join(self.test_dir_2, 'config3.yaml')
        yaml_content3 = {'api': {'key': 'secret', 'timeout': 60}}
        with open(yaml_file3, 'w') as f:
            yaml.dump(yaml_content3, f)
        
        # Read from both directories
        result = files.read_yaml_files([self.test_dir, self.test_dir_2])
        
        # Verify all content is merged
        self.assertIn('server', result)
        self.assertIn('logging', result)
        self.assertIn('api', result)

    def test_read_yaml_files_empty_directory(self):
        """Test reading from directory with no YAML files."""
        empty_dir = tempfile.mkdtemp()
        
        # Should raise exception when no YAML files found
        with self.assertRaises(SystemExit):
            files.read_yaml_files([empty_dir])
        
        # Cleanup
        shutil.rmtree(empty_dir)

    def test_read_yaml_files_invalid_directory(self):
        """Test reading from non-existent directory."""
        invalid_dir = '/nonexistent/directory'
        
        # Should raise exception for invalid directory
        with self.assertRaises(SystemExit):
            files.read_yaml_files([invalid_dir])

    def test_read_yaml_file_invalid_content(self):
        """Test reading YAML file with invalid content."""
        # Create YAML file with invalid content
        invalid_yaml = os.path.join(self.test_dir, 'invalid.yaml')
        with open(invalid_yaml, 'w') as f:
            f.write('invalid: : yaml: content')
        
        # Test with die=False
        result = files.read_yaml_file(invalid_yaml, die=False)
        self.assertEqual(result, {})
        
        # Test with die=True
        with self.assertRaises(SystemExit):
            files.read_yaml_file(invalid_yaml, die=True)



if __name__ == '__main__':
    unittest.main()
    