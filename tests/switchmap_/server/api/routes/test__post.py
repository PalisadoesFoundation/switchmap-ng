#!/usr/bin/env python3
"""Unit tests for the API POST routes in the switchmap-ng application.

This module tests the functionality and behavior of the POST routes for the API,
ensuring correctness and expected behavior under different scenarios.
"""

import os
import sys
import unittest
import tempfile
import yaml
from flask import Flask
from unittest.mock import patch, MagicMock, mock_open

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
)

from switchmap.server.api.routes.post import (
    API_POST,
    API_POLLER_SEARCH_URI,
    API_POLLER_POST_URI,
)


class TestAPIRoutes(unittest.TestCase):
    """Test API routes functionality."""

    def setUp(self):
        """Setup test client."""
        self.app = Flask(__name__)
        self.app.register_blueprint(API_POST)
        self.client = self.app.test_client()

    @patch("switchmap.server.db.misc.search.search")
    def test_post_searchterm_success(self, mock_search):
        """Test searching with a valid search term."""
        mock_search.return_value = [{"id": 1, "name": "test_result"}]

        test_data = {"searchterm": "test", "idx_root": 1}
        response = self.client.post(API_POLLER_SEARCH_URI, json=test_data)

        self.assertEqual(response.json, [{"id": 1, "name": "test_result"}])
        mock_search.assert_called_once_with(1, "test")

    def test_post_searchterm_empty(self):
        """Test searching with an empty search term."""
        test_data = {"searchterm": "", "idx_root": 1}
        response = self.client.post(API_POLLER_SEARCH_URI, json=test_data)
        self.assertEqual(response.json, [])

    @patch("switchmap.server.db.misc.search.search")
    def test_post_searchterm_error(self, mock_search):
        """Test searching when database search raises an error."""
        mock_search.side_effect = Exception("Database error")
        test_data = {"searchterm": "test", "idx_root": 1}
        response = self.client.post(API_POLLER_SEARCH_URI, json=test_data)
        self.assertEqual(response.status_code, 500)

    @patch("switchmap.server.db.misc.search.search")
    def test_post_searchterm_special_chars(self, mock_search):
        """Test searching with special characters like (!@)."""
        mock_search.return_value = []
        test_data = {"searchterm": "test@#$%", "idx_root": 1}
        response = self.client.post(API_POLLER_SEARCH_URI, json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_post_searchterm_missing_data(self):
        """Test searching when data is missing."""
        response = self.client.post(API_POLLER_SEARCH_URI, json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    @patch("switchmap.server.api.routes.post.ConfigServer")
    @patch("builtins.open", new_callable=mock_open)
    @patch("switchmap.server.api.routes.post.os.path.exists")
    @patch("switchmap.server.api.routes.post.yaml.dump")
    def test_post_device_data_success(
        self, mock_yaml_dump, mock_exists, mock_file, mock_config
    ):
        """Test posting device data successfully."""
        mock_config_instance = MagicMock()
        mock_config_instance.cache_directory.return_value = "/tmp"
        mock_config.return_value = mock_config_instance
        mock_exists.return_value = False

        test_data = {
            "misc": {"host": "test-device", "zone": "test-zone"},
            "data": {"key": "value"},
        }

        response = self.client.post(API_POLLER_POST_URI, json=test_data)
        self.assertEqual(response.data.decode(), "OK")
        mock_file.assert_called_once()
        mock_yaml_dump.assert_called_once()

    @patch("switchmap.server.api.routes.post.ConfigServer")
    @patch("switchmap.server.api.routes.post.os.path.exists")
    def test_post_device_data_file_exists(self, mock_exists, mock_config):
        """Test posting device data when file already exists."""
        mock_config_instance = MagicMock()
        mock_config_instance.cache_directory.return_value = "/tmp"
        mock_config.return_value = mock_config_instance
        mock_exists.return_value = True

        test_data = {"misc": {"host": "test-device", "zone": "test-zone"}}

        response = self.client.post(API_POLLER_POST_URI, json=test_data)
        self.assertEqual(response.data.decode(), "OK")

    @patch("switchmap.server.api.routes.post.ConfigServer")
    def test_post_device_data_missing_hostname(self, mock_config):
        """Test posting device data without hostname."""
        mock_config_instance = MagicMock()
        mock_config_instance.cache_directory.return_value = "/tmp"
        mock_config.return_value = mock_config_instance

        test_data = {"misc": {"zone": "test-zone"}}

        response = self.client.post(API_POLLER_POST_URI, json=test_data)
        self.assertEqual(response.data.decode(), "OK")

    @patch("switchmap.server.api.routes.post.ConfigServer")
    def test_post_device_data_missing_misc(self, mock_config):
        """Test posting device data without misc section."""
        mock_config_instance = MagicMock()
        mock_config_instance.cache_directory.return_value = "/tmp"
        mock_config.return_value = mock_config_instance

        test_data = {}

        response = self.client.post(API_POLLER_POST_URI, json=test_data)
        self.assertEqual(response.data.decode(), "OK")


if __name__ == "__main__":
    unittest.main()
