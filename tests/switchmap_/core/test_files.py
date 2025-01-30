#!/usr/bin/env python3
"""Test the general module."""

import unittest
import random
import os
import sys
import string
import tempfile
import yaml
import shutil


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


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()


# Import switchmap libraries
from switchmap.core import files


class TestFiles(unittest.TestCase):
    """Test suite for the files module."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(9)]
    )

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above.
        config = setup.config()
        config.save()

        # Create temporary test directory that persists for all tests
        cls.class_temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Remove the temporary directory and its contents
        shutil.rmtree(cls.class_temp_dir)

        # Cleanup config
        CONFIG.cleanup()

    def setUp(self):
        """Setup the test case."""
        # Create a temporary directory for each test
        self.temp_dir = tempfile.mkdtemp()

        # Setup the configuration
        self.config = CONFIG

        # Create test directories
        self.system_dir = os.path.join(self.temp_dir, "system")
        self.daemon_dir = os.path.join(self.temp_dir, "daemon")

        # Mock the config methods
        self.config.system_directory = lambda: self.system_dir
        self.config.daemon_directory = lambda: self.daemon_dir

    def tearDown(self):
        """Cleanup after each test."""
        # Remove the temporary directory and its contents
        shutil.rmtree(self.temp_dir)

    def test_move_yaml_files(self):
        """Test moving YAML files between directories."""
        # Create source and destination directories
        src_dir = os.path.join(self.temp_dir, "source")
        dst_dir = os.path.join(self.temp_dir, "destination")
        os.makedirs(src_dir)
        os.makedirs(dst_dir)

        # Create test YAML files
        test_files = {
            "test1.yaml": {"key1": "value1"},
            "test2.yaml": {"key2": "value2"},
            "not_yaml.txt": "not a yaml file",
        }

        # Create the test files in source directory
        for filename, content in test_files.items():
            filepath = os.path.join(src_dir, filename)
            with open(filepath, "w") as f:
                if filename.endswith(".yaml"):
                    yaml.dump(content, f)
                else:
                    f.write(content)

        # Move YAML files
        files.move_yaml_files(src_dir, dst_dir)

        # Verify YAML files were moved
        src_files = os.listdir(src_dir)
        dst_files = os.listdir(dst_dir)

        # Only non-YAML files should remain in source
        self.assertEqual(src_files, ["not_yaml.txt"])

        # Only YAML files should be in destination
        self.assertEqual(sorted(dst_files), ["test1.yaml", "test2.yaml"])

        # Verify content of moved files
        for yaml_file in ["test1.yaml", "test2.yaml"]:
            with open(os.path.join(dst_dir, yaml_file), "r") as f:
                content = yaml.safe_load(f)
                self.assertEqual(content, test_files[yaml_file])

    def test_read_yaml_files(self):
        """Test reading multiple YAML files from directories."""
        # Create test directories
        dir1 = os.path.join(self.temp_dir, "config1")
        dir2 = os.path.join(self.temp_dir, "config2")
        os.makedirs(dir1)
        os.makedirs(dir2)

        # Create test YAML files in first directory
        yaml_content1 = {
            "server": {"host": "localhost", "port": 8080},
            "database": {"name": "testdb", "user": "admin"},
        }
        yaml_content2 = {
            "logging": {"level": "INFO", "file": "app.log"},
            "cache": {"enabled": True, "timeout": 300},
        }

        with open(os.path.join(dir1, "config1.yaml"), "w") as f:
            yaml.dump(yaml_content1, f)
        with open(os.path.join(dir1, "config2.yaml"), "w") as f:
            yaml.dump(yaml_content2, f)

        # Create test YAML file in second directory
        yaml_content3 = {
            "security": {"ssl": True, "key_file": "server.key"},
            "api": {"version": "1.0", "endpoints": ["/v1", "/v2"]},
        }
        with open(os.path.join(dir2, "config3.yaml"), "w") as f:
            yaml.dump(yaml_content3, f)

        # Test reading from both directories
        directories = [dir1, dir2]
        result = files.read_yaml_files(directories)

        # Verify all content was merged correctly
        self.assertIn("server", result)
        self.assertIn("logging", result)
        self.assertIn("security", result)
        self.assertEqual(result["server"]["host"], "localhost")
        self.assertEqual(result["logging"]["level"], "INFO")
        self.assertEqual(result["security"]["ssl"], True)

        # Test with non-existent directory
        with self.assertRaises(SystemExit):
            files.read_yaml_files(["/nonexistent/directory"])

        # Test with directory containing no YAML files
        empty_dir = os.path.join(self.temp_dir, "empty")
        os.makedirs(empty_dir)
        with self.assertRaises(SystemExit):
            files.read_yaml_files([empty_dir])

        # Test with mixed valid and non-YAML files
        mixed_dir = os.path.join(self.temp_dir, "mixed")
        os.makedirs(mixed_dir)
        with open(os.path.join(mixed_dir, "config.yaml"), "w") as f:
            yaml.dump({"key": "value"}, f)
        with open(os.path.join(mixed_dir, "not_yaml.txt"), "w") as f:
            f.write("plain text")

        result = files.read_yaml_files([mixed_dir])
        self.assertIn("key", result)

    def test_read_yaml_file(self):
        """Test reading YAML file as dictionary."""
        # Create test YAML file with various data types
        test_data = {
            "string": "value",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "null": None,
        }

        filepath = os.path.join(self.temp_dir, "test.yaml")
        with open(filepath, "w") as f:
            yaml.dump(test_data, f)

        # Test reading as dictionary
        result = files.read_yaml_file(filepath)
        self.assertEqual(result, test_data)

        # Test with non-existent file
        with self.assertRaises(SystemExit):
            files.read_yaml_file("nonexistent.yaml")

        # Test with invalid YAML syntax
        invalid_filepath = os.path.join(self.temp_dir, "invalid.yaml")
        with open(invalid_filepath, "w") as f:
            f.write("invalid: yaml: [}}")

        with self.assertRaises(SystemExit):
            files.read_yaml_file(invalid_filepath)

    def test_mkdir(self):
        """Test directory creation function."""
        # Test 1: Create new directory
        new_dir = os.path.join(self.temp_dir, "new_directory")
        files.mkdir(new_dir)
        self.assertTrue(os.path.isdir(new_dir))

        # Test 2: Create nested directory
        nested_dir = os.path.join(
            self.temp_dir, "parent", "child", "grandchild"
        )
        files.mkdir(nested_dir)
        self.assertTrue(os.path.isdir(nested_dir))

        # Test 3: Create existing directory (should not raise error)
        files.mkdir(new_dir)
        self.assertTrue(os.path.isdir(new_dir))

        # Test 4: Try to create directory in read-only location (if not root)
        if os.getuid() != 0:
            with self.assertRaises(SystemExit):
                files.mkdir("/root/test_dir")

        # Test 5: Try to create directory when a file exists with same name
        file_path = os.path.join(self.temp_dir, "file_exists")
        with open(file_path, "w") as f:
            f.write("test")

        with self.assertRaises(SystemExit):
            files.mkdir(file_path)

    def test_pid_file(self):
        """Test pid_file function behavior."""
        # Test with string agent name
        agent_name = "test_agent"
        expected = os.path.join(self.daemon_dir, "pid", "test_agent.pid")
        result = files.pid_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Test with lowercase conversion
        agent_name = "TestAgent"
        expected = os.path.join(self.daemon_dir, "pid", "testagent.pid")
        result = files.pid_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Test with numeric agent name
        agent_name = 123
        expected = os.path.join(self.daemon_dir, "pid", "123.pid")
        result = files.pid_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Verify directory creation
        self.assertTrue(os.path.isdir(os.path.dirname(result)))

        # Test with special characters
        agent_name = "test-agent_123"
        expected = os.path.join(self.daemon_dir, "pid", "test-agent_123.pid")
        result = files.pid_file(agent_name, self.config)
        self.assertEqual(result, expected)

    def test_lock_file(self):
        """Test lock_file function behavior."""
        # Test with string agent name
        agent_name = "test_agent"
        expected = os.path.join(self.daemon_dir, "lock", "test_agent.lock")
        result = files.lock_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Test with lowercase conversion
        agent_name = "TestAgent"
        expected = os.path.join(self.daemon_dir, "lock", "testagent.lock")
        result = files.lock_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Test with numeric agent name
        agent_name = 123
        expected = os.path.join(self.daemon_dir, "lock", "123.lock")
        result = files.lock_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Verify directory creation
        self.assertTrue(os.path.isdir(os.path.dirname(result)))

        # Test with empty string
        agent_name = ""
        expected = os.path.join(self.daemon_dir, "lock", ".lock")
        result = files.lock_file(agent_name, self.config)
        self.assertEqual(result, expected)

    def test_skip_file(self):
        """Test skip_file function behavior."""
        # Test with string agent name
        agent_name = "test_agent"
        expected = os.path.join(self.daemon_dir, "lock", "test_agent.skip")
        result = files.skip_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Test with lowercase conversion
        agent_name = "TestAgent"
        expected = os.path.join(self.daemon_dir, "lock", "testagent.skip")
        result = files.skip_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Test with numeric agent name
        agent_name = 123
        expected = os.path.join(self.daemon_dir, "lock", "123.skip")
        result = files.skip_file(agent_name, self.config)
        self.assertEqual(result, expected)

        # Verify directory creation
        self.assertTrue(os.path.isdir(os.path.dirname(result)))

        # Test with special characters and spaces
        agent_name = "test agent-123_456"
        expected = os.path.join(
            self.daemon_dir, "lock", "test agent-123_456.skip"
        )
        result = files.skip_file(agent_name, self.config)
        self.assertEqual(result, expected)

    def test_snmp_file(self):
        """Test snmp_file function behavior."""
        # Test with basic hostname
        hostname = "test-host"
        expected = os.path.join(self.system_dir, "snmp", "test-host.snmp")
        result = files.snmp_file(hostname, self.config)
        self.assertEqual(result, expected)

        # Test with FQDN
        hostname = "test-host.example.com"
        expected = os.path.join(
            self.system_dir, "snmp", "test-host.example.com.snmp"
        )
        result = files.snmp_file(hostname, self.config)
        self.assertEqual(result, expected)

        # Test with IP address format
        hostname = "192.168.1.1"
        expected = os.path.join(self.system_dir, "snmp", "192.168.1.1.snmp")
        result = files.snmp_file(hostname, self.config)
        self.assertEqual(result, expected)

        # Verify directory creation
        self.assertTrue(os.path.isdir(os.path.dirname(result)))

        # Test with uppercase hostname (should preserve case)
        hostname = "TEST-HOST"
        expected = os.path.join(self.system_dir, "snmp", "TEST-HOST.snmp")
        result = files.snmp_file(hostname, self.config)
        self.assertEqual(result, expected)
    
    def test_execute(self):
        """Test the execute function for command execution."""
        # Test successful command
        command = "echo 'test message'"
        result = files.execute(command)
        self.assertEqual(result, 0)

        # Test successful command with space in arguments
        command = "echo 'test message with spaces'"
        result = files.execute(command)
        self.assertEqual(result, 0)

        # Test failing command with die=False
        command = "ls /nonexistent_directory"
        result = files.execute(command, die=False)
        self.assertNotEqual(result, 0)

        # Test command with stdout
        command = "echo 'test stdout'"
        result = files.execute(command)
        self.assertEqual(result, 0)

        # Test command with stderr
        command = "ls /nonexistent_directory 2>&1"
        try:
            result = files.execute(command, die=False)
            self.assertNotEqual(result, 0)
        except SystemExit:
            pass

        # Test invalid command
        command = "invalid_command_123"
        try:
            result = files.execute(command, die=False)
            self.assertNotEqual(result, 0)
        except SystemExit:
            pass

        # Test command with multiple arguments
        command = "ls -la /tmp"
        result = files.execute(command)
        self.assertEqual(result, 0)

        # Test empty command
        command = ""
        try:
            result = files.execute(command, die=False)
            self.assertNotEqual(result, 0)
        except (SystemExit, ValueError):
            pass

    def test_execute_with_output(self):
        """Test the execute function output handling."""
        # Create a temporary file for testing
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")

        # Test command with both stdout and stderr
        command = f"cat {test_file} && ls /nonexistent_directory"
        try:
            files.execute(command, die=False)
        except SystemExit:
            pass

        # Test command with large output
        large_text = "x" * 10000
        command = f"echo '{large_text}'"
        result = files.execute(command)
        self.assertEqual(result, 0)

        # Test command with special characters
        command = "echo 'test@#$%^&*()'"
        result = files.execute(command)
        self.assertEqual(result, 0)

        # Test command with environment variables
        os.environ["TEST_VAR"] = "test_value"
        command = "echo $TEST_VAR"
        result = files.execute(command)
        self.assertEqual(result, 0)

    def test_execute_error_handling(self):
        """Test error handling in execute function."""
        # Test with None command
        with self.assertRaises((SystemExit, AttributeError, TypeError)):
            files.execute(None)

        # Test with integer command
        with self.assertRaises((SystemExit, AttributeError, TypeError)):
            files.execute(123)

        # Test with very long command
        long_command = "echo " + "x" * 10000
        try:
            files.execute(long_command, die=False)
        except SystemExit:
            pass

        # Test with malformed command
        command = "ls | | ls"
        try:
            files.execute(command, die=False)
        except SystemExit:
            pass

    def test_config_filepath(self):
        """Test the config_filepath function."""
        # Get the result from the function
        result = files.config_filepath()

        # Basic assertions about the result
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith("config.yaml"))
        self.assertTrue(os.sep in result)

        # Test if the directory exists
        directory = os.path.dirname(result)
        self.assertTrue(os.path.exists(directory))


if __name__ == "__main__":
    unittest.main()
