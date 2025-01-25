#!/usr/bin/env python3
import os
import sys
import unittest
from flask import Flask
from unittest.mock import patch, MagicMock

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
)

from switchmap.server.api.routes.post import API_POST, API_POLLER_SEARCH_URI


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
        """Test searching with special characters."""
        mock_search.return_value = []
        test_data = {"searchterm": "test@#$%", "idx_root": 1}
        response = self.client.post(API_POLLER_SEARCH_URI, json=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])


if __name__ == "__main__":
    unittest.main()
