#!/usr/bin/env python3
"""Unit tests for the GraphQL API routes in the switchmap-ng application.

This module tests the functionality and behavior of the GraphQL routes for
the API.
"""

import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.."))
)

import unittest
from unittest.mock import patch
from flask import Flask
from switchmap.server.api.routes.graphql import API_GRAPHQL


class TestGraphQLRoutes(unittest.TestCase):
    """Test cases for GraphQL API routes."""

    def setUp(self):
        """Set up the test client and register the blueprint."""
        self.app = Flask(__name__)
        self.app.register_blueprint(API_GRAPHQL)
        self.client = self.app.test_client()

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_empty_graphql_query(self, mock_schema):
        """Test GraphQL route with an empty query."""
        mock_schema.return_value.execute.return_value = {"errors": ["Error"]}
        response = self.client.post("/graphql", json={"query": ""})
        self.assertEqual(response.status_code, 400)

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_graphql_route_with_invalid_json(self, mock_schema):
        """Test GraphQL route with invalid JSON."""
        mock_schema.return_value.execute.return_value = {"errors": ["Error"]}
        response = self.client.post(
            "/graphql", data="invalid json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_successful_graphql_query(self, mock_schema):
        """Test a successful GraphQL query."""
        mock_schema.return_value.execute.return_value = {
            "data": {"field": "value"}
        }
        response = self.client.post("/graphql", json={"query": "{ field }"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"data": {"field": "value"}})

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_successful_graphql_mutation(self, mock_schema):
        """Test a successful GraphQL mutation."""
        mock_schema.return_value.execute.return_value = {
            "data": {"mutateField": "mutatedValue"}
        }
        response = self.client.post(
            "/graphql", json={"query": "mutation { mutateField }"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"data": {"mutateField": "mutatedValue"}}
        )

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_large_graphql_query(self, mock_schema):
        """Test GraphQL route with a large query."""
        large_query = "{ " + " ".join([f"field{i}" for i in range(100)]) + " }"
        mock_schema.return_value.execute.return_value = {
            "data": {f"field{i}": f"value{i}" for i in range(100)}
        }
        response = self.client.post("/graphql", json={"query": large_query})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {"data": {f"field{i}": f"value{i}" for i in range(100)}},
        )

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_nested_graphql_query(self, mock_schema):
        """Test GraphQL route with a nested query."""
        nested_query = "{ parent { child { field } } }"
        mock_schema.return_value.execute.return_value = {
            "data": {"parent": {"child": {"field": "value"}}}
        }
        response = self.client.post("/graphql", json={"query": nested_query})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json, {"data": {"parent": {"child": {"field": "value"}}}}
        )


if __name__ == "__main__":
    unittest.main()
