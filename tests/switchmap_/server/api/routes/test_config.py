#!/usr/bin/env python3
"""Unit tests for the API Config routes in the switchmap-ng application.

This module tests the functionality of the configuration management endpoints,
including reading, writing, and updating configuration files with proper
secret handling and validation.
"""

import json
import os
import sys
import tempfile
import unittest
import yaml
from unittest.mock import patch, mock_open, MagicMock
from flask import Flask

# Path setup for testing
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(
            os.path.join(
                os.path.abspath(
                    os.path.join(
                        os.path.abspath(
                            os.path.join(
                                os.path.abspath(
                                    os.path.join(EXEC_DIR, os.pardir)
                                ),
                                os.pardir,
                            )
                        ),
                        os.pardir,
                    )
                ),
                os.pardir,
            )
        ),
        os.pardir,
    )
)
_EXPECTED = """\
{0}switchmap-ng{0}tests{0}switchmap_{0}server{0}api{0}routes""".format(
    os.sep
)
if EXEC_DIR.endswith(_EXPECTED) is True:
    sys.path.insert(0, ROOT_DIR)
else:
    print(
        """This script is not installed in the "{0}" directory. Please fix.\
""".format(
            _EXPECTED
        )
    )
    sys.exit(2)

from switchmap.server.api.routes.config import (
    API_CONFIG,
    _is_secret_placeholder,
    merge_preserving_secrets,
    read_config,
    write_config,
    mask_secrets,
    deep_merge,
    PLACEHOLDER,
    SECRET_KEYS,
    CONFIG_PATH,
)


class TestConfigHelperFunctions(unittest.TestCase):
    """Test helper functions in config module."""

    def test_is_secret_placeholder_dict_with_secret(self):
        """Test _is_secret_placeholder with dict containing secret."""
        secret_dict = {"isSecret": True, "value": PLACEHOLDER}
        self.assertTrue(_is_secret_placeholder(secret_dict))

    def test_is_secret_placeholder_dict_without_secret(self):
        """Test _is_secret_placeholder with dict not containing secret."""
        normal_dict = {"isSecret": False, "value": "test"}
        self.assertFalse(_is_secret_placeholder(normal_dict))

    def test_is_secret_placeholder_dict_missing_keys(self):
        """Test _is_secret_placeholder with dict missing required keys."""
        incomplete_dict = {"isSecret": True}
        self.assertFalse(_is_secret_placeholder(incomplete_dict))

    def test_is_secret_placeholder_string_placeholder(self):
        """Test _is_secret_placeholder with placeholder string."""
        self.assertTrue(_is_secret_placeholder(PLACEHOLDER))

    def test_is_secret_placeholder_string_normal(self):
        """Test _is_secret_placeholder with normal string."""
        self.assertFalse(_is_secret_placeholder("normal_string"))

    def test_is_secret_placeholder_other_types(self):
        """Test _is_secret_placeholder with other data types."""
        self.assertFalse(_is_secret_placeholder(123))
        self.assertFalse(_is_secret_placeholder([]))
        self.assertFalse(_is_secret_placeholder(None))

    def test_merge_preserving_secrets_dict_merge(self):
        """Test merge_preserving_secrets with dictionary merge."""
        current = {
            "db_pass": "current_password",
            "normal_key": "current_value",
            "nested": {"inner": "current_inner"}
        }
        incoming = {
            "db_pass": PLACEHOLDER,
            "normal_key": "new_value",
            "nested": {"inner": "new_inner"}
        }
        result = merge_preserving_secrets(current, incoming)
        
        self.assertEqual(result["db_pass"], "current_password")
        self.assertEqual(result["normal_key"], "new_value")
        self.assertEqual(result["nested"]["inner"], "new_inner")

    def test_merge_preserving_secrets_secret_dict_format(self):
        """Test merge_preserving_secrets with secret dict format."""
        current = {"db_pass": "current_password"}
        incoming = {"db_pass": {"isSecret": True, "value": "new_password"}}
        result = merge_preserving_secrets(current, incoming)
        
        self.assertEqual(result["db_pass"], "new_password")

    def test_merge_preserving_secrets_empty_values(self):
        """Test merge_preserving_secrets with empty/None values."""
        current = {"db_pass": "current_password"}
        incoming = {"db_pass": ""}
        result = merge_preserving_secrets(current, incoming)
        
        self.assertEqual(result["db_pass"], "current_password")

        incoming = {"db_pass": None}
        result = merge_preserving_secrets(current, incoming)
        
        self.assertEqual(result["db_pass"], "current_password")

    def test_merge_preserving_secrets_list_merge(self):
        """Test merge_preserving_secrets with list merge."""
        current = ["item1", "item2"]
        incoming = ["new_item1", "new_item2", "new_item3"]
        result = merge_preserving_secrets(current, incoming)
        
        self.assertEqual(result, ["new_item1", "new_item2", "new_item3"])

    def test_merge_preserving_secrets_non_dict_list(self):
        """Test merge_preserving_secrets with non-dict/non-list values."""
        current = "current_value"
        incoming = "new_value"
        result = merge_preserving_secrets(current, incoming)
        
        self.assertEqual(result, "new_value")

    def test_mask_secrets_dict(self):
        """Test mask_secrets with dictionary containing secrets."""
        config = {
            "db_pass": "secret_password",
            "snmp_community": "public",
            "normal_key": "normal_value",
            "nested": {
                "snmp_authpassword": "auth_secret",
                "regular": "value"
            }
        }
        result = mask_secrets(config)
        
        self.assertEqual(result["db_pass"], {"isSecret": True, "value": PLACEHOLDER})
        self.assertEqual(result["snmp_community"], {"isSecret": True, "value": PLACEHOLDER})
        self.assertEqual(result["normal_key"], "normal_value")
        self.assertEqual(result["nested"]["snmp_authpassword"], {"isSecret": True, "value": PLACEHOLDER})
        self.assertEqual(result["nested"]["regular"], "value")

    def test_mask_secrets_empty_secret(self):
        """Test mask_secrets with empty secret values."""
        config = {"db_pass": "", "normal_key": "value"}
        result = mask_secrets(config)
        
        self.assertEqual(result["db_pass"], "")
        self.assertEqual(result["normal_key"], "value")

    def test_mask_secrets_list(self):
        """Test mask_secrets with list containing secrets."""
        config = [
            {"db_pass": "secret"},
            {"normal": "value"}
        ]
        result = mask_secrets(config)
        
        self.assertEqual(result[0]["db_pass"], {"isSecret": True, "value": PLACEHOLDER})
        self.assertEqual(result[1]["normal"], "value")

    def test_mask_secrets_non_dict_list(self):
        """Test mask_secrets with non-dict/non-list values."""
        self.assertEqual(mask_secrets("string"), "string")
        self.assertEqual(mask_secrets(123), 123)
        self.assertEqual(mask_secrets(None), None)

    def test_deep_merge_dicts(self):
        """Test deep_merge with dictionaries."""
        dst = {"a": 1, "b": {"c": 2, "d": 3}}
        src = {"b": {"c": 4, "e": 5}, "f": 6}
        result = deep_merge(dst, src)
        
        expected = {"a": 1, "b": {"c": 4, "d": 3, "e": 5}, "f": 6}
        self.assertEqual(result, expected)

    def test_deep_merge_non_dicts(self):
        """Test deep_merge with non-dictionary values."""
        self.assertEqual(deep_merge("old", "new"), "new")
        self.assertEqual(deep_merge(123, 456), 456)
        self.assertEqual(deep_merge([], [1, 2, 3]), [1, 2, 3])


class TestConfigFileOperations(unittest.TestCase):
    """Test file operations for config module."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_config = {
            "server": {
                "db_host": "localhost",
                "db_pass": "secret_password"
            },
            "polling": {
                "interval": 300
            }
        }

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/test_config.yaml')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.safe_load')
    def test_read_config_success(self, mock_yaml_load, mock_file, mock_exists):
        """Test successful config file reading."""
        mock_exists.return_value = True
        mock_yaml_load.return_value = self.test_config
        
        result = read_config()
        
        self.assertEqual(result, self.test_config)
        mock_exists.assert_called_once_with('/tmp/test_config.yaml')
        mock_file.assert_called_once_with('/tmp/test_config.yaml', 'r')

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/nonexistent_config.yaml')
    @patch('os.path.exists')
    def test_read_config_file_not_exists(self, mock_exists):
        """Test reading config when file doesn't exist."""
        mock_exists.return_value = False
        
        result = read_config()
        
        self.assertEqual(result, {})

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/test_config.yaml')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.safe_load')
    def test_read_config_yaml_error(self, mock_yaml_load, mock_file, mock_exists):
        """Test reading config with YAML error."""
        mock_exists.return_value = True
        mock_yaml_load.side_effect = yaml.YAMLError("Invalid YAML")
        
        result = read_config()
        
        self.assertEqual(result, {})

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/test_config.yaml')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.safe_load')
    def test_read_config_os_error(self, mock_yaml_load, mock_file, mock_exists):
        """Test reading config with OS error."""
        mock_exists.return_value = True
        mock_file.side_effect = OSError("Permission denied")
        
        result = read_config()
        
        self.assertEqual(result, {})

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/test_config.yaml')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    @patch('yaml.safe_load')
    def test_read_config_empty_file(self, mock_yaml_load, mock_file, mock_exists):
        """Test reading empty config file."""
        mock_exists.return_value = True
        mock_yaml_load.return_value = None
        
        result = read_config()
        
        self.assertEqual(result, {})

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/test_config.yaml')
    @patch('os.makedirs')
    @patch('tempfile.mkstemp')
    @patch('os.fdopen')
    @patch('os.replace')
    @patch('os.chmod')
    @patch('os.open')
    @patch('os.fsync')
    @patch('os.close')
    def test_write_config_success(self, mock_close, mock_fsync, mock_open_dir, 
                                 mock_chmod, mock_replace, mock_fdopen, 
                                 mock_mkstemp, mock_makedirs):
        """Test successful config file writing."""
        mock_mkstemp.return_value = (1, '/tmp/.config.tmp123')
        mock_file = MagicMock()
        mock_fdopen.return_value.__enter__.return_value = mock_file
        mock_open_dir.return_value = 3
        
        write_config(self.test_config)
        
        mock_makedirs.assert_called_once()
        mock_mkstemp.assert_called_once()
        mock_replace.assert_called_once_with('/tmp/.config.tmp123', '/tmp/test_config.yaml')
        mock_chmod.assert_called_once_with('/tmp/test_config.yaml', 0o600)

    @patch('switchmap.server.api.routes.config.CONFIG_PATH', '/tmp/test_config.yaml')
    @patch('os.makedirs')
    @patch('tempfile.mkstemp')
    @patch('os.fdopen')
    @patch('os.unlink')
    def test_write_config_exception_cleanup(self, mock_unlink, mock_fdopen, 
                                          mock_mkstemp, mock_makedirs):
        """Test config writing with exception and cleanup."""
        mock_mkstemp.return_value = (1, '/tmp/.config.tmp123')
        mock_fdopen.side_effect = Exception("Write error")
        
        with self.assertRaises(Exception):
            write_config(self.test_config)
        
        mock_unlink.assert_called_once_with('/tmp/.config.tmp123')


class TestConfigAPIRoutes(unittest.TestCase):
    """Test API routes for config module."""

    def setUp(self):
        """Set up test client."""
        self.app = Flask(__name__)
        self.app.register_blueprint(API_CONFIG)
        self.client = self.app.test_client()
        
        self.test_config = {
            "server": {
                "db_host": "localhost",
                "db_pass": "secret_password"
            },
            "polling": {
                "interval": 300
            }
        }

    @patch('switchmap.server.api.routes.config.read_config')
    def test_get_config_success(self, mock_read_config):
        """Test successful GET /config."""
        mock_read_config.return_value = self.test_config
        
        response = self.client.get('/config')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["polling"]["interval"], 300)
        self.assertEqual(data["server"]["db_pass"], {"isSecret": True, "value": PLACEHOLDER})

    @patch('switchmap.server.api.routes.config.read_config')
    @patch('switchmap.server.api.routes.config.write_config')
    def test_post_config_success(self, mock_write_config, mock_read_config):
        """Test successful POST /config."""
        mock_read_config.return_value = self.test_config
        
        new_config = {
            "server": {
                "db_host": "newhost",
                "db_pass": "new_password"
            }
        }
        
        response = self.client.post('/config', 
                                  data=json.dumps(new_config),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        mock_write_config.assert_called_once()

    def test_post_config_invalid_json(self):
        """Test POST /config with invalid JSON."""
        response = self.client.post('/config', 
                                  data='invalid json',
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid or missing JSON")

    def test_post_config_non_dict_json(self):
        """Test POST /config with non-dictionary JSON."""
        response = self.client.post('/config', 
                                  data=json.dumps(["not", "a", "dict"]),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Expected JSON object")

    @patch('switchmap.server.api.routes.config.read_config')
    @patch('switchmap.server.api.routes.config.write_config')
    def test_patch_config_db_pass_success(self, mock_write_config, mock_read_config):
        """Test successful PATCH /config for db_pass."""
        mock_read_config.return_value = self.test_config
        
        patch_data = {
            "db_pass": {
                "new": "updated_password"
            }
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        mock_write_config.assert_called_once()

    @patch('switchmap.server.api.routes.config.read_config')
    def test_patch_config_db_pass_invalid_format(self, mock_read_config):
        """Test PATCH /config with invalid db_pass format."""
        mock_read_config.return_value = self.test_config
        
        patch_data = {
            "db_pass": "invalid_format"
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid db_pass format")

    @patch('switchmap.server.api.routes.config.read_config')
    def test_patch_config_db_pass_missing_new(self, mock_read_config):
        """Test PATCH /config with db_pass missing 'new' key."""
        mock_read_config.return_value = self.test_config
        
        patch_data = {
            "db_pass": {
                "old": "old_password"
            }
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid db_pass format")

    @patch('switchmap.server.api.routes.config.read_config')
    @patch('switchmap.server.api.routes.config.write_config')
    def test_patch_config_db_pass_empty_value(self, mock_write_config, mock_read_config):
        """Test PATCH /config with empty db_pass value."""
        mock_read_config.return_value = self.test_config
        
        patch_data = {
            "db_pass": {
                "new": ""
            }
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        # Should not update the password with empty value
        mock_write_config.assert_called_once()

    @patch('switchmap.server.api.routes.config.read_config')
    @patch('switchmap.server.api.routes.config.write_config')
    def test_patch_config_db_pass_placeholder_value(self, mock_write_config, mock_read_config):
        """Test PATCH /config with placeholder db_pass value."""
        mock_read_config.return_value = self.test_config
        
        patch_data = {
            "db_pass": {
                "new": PLACEHOLDER
            }
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        mock_write_config.assert_called_once()

    @patch('switchmap.server.api.routes.config.read_config')
    @patch('switchmap.server.api.routes.config.write_config')
    def test_patch_config_other_fields(self, mock_write_config, mock_read_config):
        """Test PATCH /config with other configuration fields."""
        mock_read_config.return_value = self.test_config
        
        patch_data = {
            "polling": {
                "interval": 600
            },
            "new_section": {
                "new_key": "new_value"
            }
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        mock_write_config.assert_called_once()

    @patch('switchmap.server.api.routes.config.read_config')
    @patch('switchmap.server.api.routes.config.write_config')
    def test_patch_config_no_server_section(self, mock_write_config, mock_read_config):
        """Test PATCH /config when current config has no server section."""
        config_without_server = {
            "polling": {
                "interval": 300
            }
        }
        mock_read_config.return_value = config_without_server
        
        patch_data = {
            "db_pass": {
                "new": "new_password"
            }
        }
        
        response = self.client.patch('/config',
                                   data=json.dumps(patch_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        mock_write_config.assert_called_once()

    def test_patch_config_invalid_json(self):
        """Test PATCH /config with invalid JSON."""
        response = self.client.patch('/config',
                                   data='invalid json',
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid JSON")

    def test_patch_config_no_data(self):
        """Test PATCH /config with no data."""
        response = self.client.patch('/config',
                                   data='',
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "Invalid JSON")


class TestConfigConstants(unittest.TestCase):
    """Test constants and module-level configurations."""

    def test_secret_keys_defined(self):
        """Test that SECRET_KEYS contains expected keys."""
        expected_keys = {
            "db_pass",
            "snmp_authpassword", 
            "snmp_privpassword",
            "snmp_community",
        }
        self.assertEqual(SECRET_KEYS, expected_keys)

    def test_placeholder_defined(self):
        """Test that PLACEHOLDER is properly defined."""
        self.assertEqual(PLACEHOLDER, "********")

    def test_config_path_defined(self):
        """Test that CONFIG_PATH is properly defined."""
        self.assertIsInstance(CONFIG_PATH, str)
        self.assertTrue(CONFIG_PATH.endswith('config.yaml'))


if __name__ == "__main__":
    unittest.main()