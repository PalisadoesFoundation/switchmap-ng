#!/usr/bin/env python3
"""Unittests for the API Graphql routes.

This module tests the functionaliity in the qraphql endpoint.
"""

import json
import os
import sys
import unittest
from unittest.mock import patch

from flask import Flask

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
)

from switchmap.server.api.routes.graphql import API_GRAPHQL


class TestGraphqlAPIRoute(unittest.TestCase):
    """Test graphql route."""

    def setUp(self) -> None:
        """Start up resources for test."""
        super().setUp()

        self.app = Flask(__name__)
        self.app.register_blueprint(API_GRAPHQL)

        self.client = self.app.test_client()

    def test_graphql_no_query(self) -> None:
        """Test providing no query returns errors."""
        resp = self.client.get("/graphql")

        data: dict = resp.get_json()

        self.assertGreater(len(data), 0)
        self.assertIn("errors", data)
        self.assertDictEqual(
            data["errors"][0], {"message": "Must provide query string."}
        )

    @patch("flask.testing.FlaskClient.post")
    def test_graphql_query(self, mock_post) -> None:
        """Test valid query returns correct response."""
        query = """
        query GetDevice($id: ID!) {
          device(id: $id) {
            id
            name
            type
          }
        }
        """
        result = {
            "data": {
                "device": {"id": "device-123", "name": "Router A", "type": "ROUTER"}
            }
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.get_json.return_value = result

        response = self.client.post(
            "/graphql",
            data=json.dumps({"query": query, "variables": {"id": "device-123"}}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.get_json())
        self.assertDictEqual(result, response.get_json())

    @patch("flask.testing.FlaskClient.post")
    def test_graphql_invalid_query(self, mock_post) -> None:
        """Test invalid query returns correct error response."""
        result = {
            "errors": [
                {
                    "message": "Syntax Error: Unexpected Name 'NoneExistentField'",
                    "locations": [{"line": 2, "column": 3}],
                }
            ]
        }
        mock_post.return_value.status_code = 400
        mock_post.return_value.get_json.return_value = result

        query = """
        query InvalidQuery {
          NoneExistentField {
            id
            name
          }
        }
        """
        response = self.client.post(
            "/graphql",
            data=json.dumps({"query": query}),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.get_json())
        self.assertEqual(
            response.get_json()["errors"][0]["message"],
            "Syntax Error: Unexpected Name 'NoneExistentField'",
        )
