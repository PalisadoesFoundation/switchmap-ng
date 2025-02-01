#!/usr/bin/env python3
"""
Unit tests for the GraphQL API routes in the switchmap-ng application.
This module tests the functionality and behavior of the GraphQL routes for the API.
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
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(API_GRAPHQL)
        self.client = self.app.test_client()

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_empty_graphql_query(self, mock_schema):
        mock_schema.return_value.execute.return_value = {"errors": ["Error"]}
        response = self.client.post("/graphql", json={"query": ""})
        self.assertEqual(response.status_code, 400)

    @patch("switchmap.server.api.routes.graphql.SCHEMA.graphql_schema")
    def test_graphql_route_with_invalid_json(self, mock_schema):
        mock_schema.return_value.execute.return_value = {"errors": ["Error"]}
        response = self.client.post(
            "/graphql", data="invalid json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
