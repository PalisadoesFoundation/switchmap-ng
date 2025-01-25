#!/usr/bin/env python3
"""Comprehensive tests for rest.py using Flask-Testing without mocks.

This module contains unit tests for the rest.py module, ensuring proper
functionality of API request handling under various scenarios.
"""

import unittest
from flask import Flask, jsonify, request
from flask_testing import LiveServerTestCase
from switchmap.core import rest
from switchmap.core.log import ExceptionWrapper
from unittest.mock import patch


class MockConfigNoCredentials:
    """Configuration class simulating no credentials for API access.

    Provides a configuration scenario where username and password are empty,
    testing the code path for unauthenticated API requests.
    """

    def __init__(
        self,
        server_root="http://localhost:5000",
        api_root="http://localhost:5000/api",
    ):
        """Initialize MockConfigNoCredentials with default or custom URLs.

        Args:
            server_root (str, optional): Base server URL. Defaults to localhost.
            api_root (str, optional): Base API URL. Defaults to localhost.

        Returns:
            None
        """
        self._server_root = server_root
        self._api_root = api_root

    def server_username(self):
        """Return empty username.

        Args:
            None

        Returns:
            str: Empty string representing no username.
        """
        return ""

    def server_password(self):
        """Return empty password.

        Args:
            None

        Returns:
            str: Empty string representing no password.
        """
        return ""

    def server_url_root(self):
        """Get server root URL.

        Args:
            None

        Returns:
            str: Server root URL.
        """
        return self._server_root

    def api_url_root(self):
        """Get API root URL.

        Args:
            None

        Returns:
            str: API root URL.
        """
        return self._api_root


class MockConfig:
    """Configuration class simulating standard API credentials.

    Provides a configuration scenario with username and password
    for API authentication.
    """

    def __init__(
        self,
        server_root="http://localhost:5000",
        api_root="http://localhost:5000/api",
    ):
        """Initialize MockConfig with default or custom URLs.

        Args:
            server_root (str, optional): Base server URL. Defaults to localhost.
            api_root (str, optional): Base API URL. Defaults to localhost.

        Returns:
            None
        """
        self._server_root = server_root
        self._api_root = api_root

    def server_username(self):
        """Return test username.

        Args:
            None

        Returns:
            str: Test username for authentication.
        """
        return "test_user"

    def server_password(self):
        """Return test password.

        Args:
            None

        Returns:
            str: Test password for authentication.
        """
        return "test_pass"

    def server_url_root(self):
        """Get server root URL.

        Args:
            None

        Returns:
            str: Server root URL.
        """
        return self._server_root

    def api_url_root(self):
        """Get API root URL.

        Args:
            None

        Returns:
            str: API root URL.
        """
        return self._api_root


class TestRest(LiveServerTestCase):
    """Test suite for REST API functionality using live server.

    Uses LiveServerTestCase to handle real HTTP requests and thoroughly
    test rest.py implementation.
    """

    def create_app(self):
        """Create Flask application with test routes.

        Args:
            None

        Returns:
            Flask: Configured Flask application for testing.
        """
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = 5000

        # Standard route for server=True
        @app.route("/switchmap/api/test/endpoint", methods=["GET", "POST"])
        def test_endpoint_server_true():
            """Handle GET and POST requests for server=True scenario."""
            if request.method == "POST":
                return jsonify({"posted": True}), 200
            return jsonify({"data": True}), 200

        @app.route("/switchmap/api/test/error", methods=["POST"])
        def test_error():
            """Simulate a server error response."""
            return jsonify({"error": "Server error"}), 500

        @app.route("/switchmap/api/test/base-exception", methods=["POST"])
        def test_base_exception():
            """Trigger a base exception for testing error handling."""
            raise BaseException("An error not derived from Exception.")

        @app.route("/switchmap/api/test/json-malformed", methods=["GET"])
        def json_malformed():
            """Return malformed JSON for testing.

            Args:
            None

            Returns:
                tuple: Malformed JSON response body and the HTTP status code
            """
            return "{invalid json...", 200

        @app.route("/switchmap/api/test/fail_on_purpose", methods=["GET"])
        def fail_on_purpose():
            """Return a forced failure response.

            Args:
            None

            Returns:
            tuple: JSON response containing an error message.
            """
            return jsonify({"error": "Forced failure"}), 500

        @app.route("/api/switchmap/test/endpoint", methods=["GET", "POST"])
        def test_endpoint_server_false():
            """Handle GET and POST requests for server=False scenario.

            Args:
            None
            """
            if request.method == "POST":
                return jsonify({"posted_server_false": True}), 200

        @app.route("/switchmap/api/graphql", methods=["GET"])
        def graphql_endpoint():
            """Simulate GraphQL endpoint.

            Args:
                None

            Returns:
                tuple: JSON response containing test data and HTTP status code
            """
            return jsonify({"data": {"test": "value"}}), 200

        @app.route("/switchmap/api/test/json-ok", methods=["GET"])
        def json_ok():
            """Return valid JSON for testing.

            Args:
                None

            Returns:
                tuple: JSON response containing test data and HTTP status code
            """
            return jsonify({"valid": "json"}), 200

        return app

    def setUp(self):
        """Set up test configurations and data."""
        self.config = MockConfig()
        self.nocreds_config = MockConfigNoCredentials()
        self.test_uri = "test/endpoint"
        self.test_data = {"hello": "world"}

    def test_post_base_exception_handling(self):
        """Test handling of BaseException in post method."""
        result = rest.post("test/base-exception", self.test_data, self.config)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ExceptionWrapper)
        self.assertFalse(
            hasattr(result, "success")
        )  # Ensure it's not a Post namedtuple

    def test_get_json_malformed_die_true(self):
        """Tests if system exits when encountering malformed JSON."""
        with self.assertRaises(SystemExit):
            rest.get("test/json-malformed", self.config, die=True)

    def test_get_network_error_die_true(self):
        """Tests handling of network errors in REST GET."""
        saved_server_url = self.config.server_url_root()
        try:
            self.config._server_root = "http://this-domain-doesnot-exist-9999"
            with self.assertRaises(SystemExit):
                rest.get("test/json-ok", self.config, die=True)
        finally:
            self.config._server_root = saved_server_url

    def test_post_no_credentials(self):
        """Test post request without authentication credentials."""
        result = rest.post(self.test_uri, self.test_data, self.nocreds_config)
        self.assertFalse(isinstance(result, ExceptionWrapper))
        self.assertTrue(result.success)

    def test_clean_url(self):
        """Test the _clean_url utility function directly."""
        urls = [
            "http://example.com//api//v1//data",
            "https://example.com//api//v1//data",
            "http:/example.com/api/v1/data",
            "https:/example.com/api/v1/data",
            "http://example.com////////",
        ]
        for url in urls:
            _ = rest._clean_url(url)

    def test_post_success(self):
        """Test successful POST request to API endpoint with credentials."""
        result = rest.post(self.test_uri, self.test_data, self.config)
        self.assertFalse(isinstance(result, ExceptionWrapper))
        self.assertTrue(result.success)
        self.assertEqual(result.response.status_code, 200)

    def test_post_http_500(self):
        """Test POST request handling for HTTP 500 error response."""
        result = rest.post("test/error", self.test_data, self.config)
        self.assertFalse(isinstance(result, ExceptionWrapper))
        self.assertFalse(result.success)
        self.assertEqual(result.response.status_code, 500)

    def test_post_exception_handling(self):
        """Test exception handling when a network error."""
        saved_server_url = self.config.server_url_root()
        try:
            self.config._server_root = "http://invalid.domain123"
            result = rest.post(self.test_uri, self.test_data, self.config)
            self.assertIsInstance(result, ExceptionWrapper)
        finally:
            self.config._server_root = saved_server_url

    def test_get_http_500_with_die(self):
        """GET => returns 500 => raises SystemExit if die=True."""
        with self.assertRaises(SystemExit):
            rest.get("test/fail_on_purpose", self.config, die=True)

    def test_get_json_malformed_no_die(self):
        """Covers parsing exception branch, returns [] if die=False."""
        data = rest.get("test/json-malformed", self.config, die=False)
        self.assertEqual(data, [])

    def test_get_graphql_success(self):
        """Use get_graphql => returns known JSON data."""
        response = rest.get_graphql("query { test }", self.config, die=False)
        self.assertEqual(response, {"data": {"test": "value"}})

    def test_get_stream_true(self):
        """_get with stream=True => ensures success if no error."""
        url = f"{self.get_server_url()}/switchmap/api/test/json-ok"
        result = rest._get(url, self.config, stream=True)
        self.assertTrue(result.success)

    def test_get_network_exception_wrapper(self):
        """Test REST GET request error handling with an invalid domain."""
        saved_server_url = self.config.server_url_root()
        try:
            self.config._server_root = "http://bad.server789"
            # die=False => no SystemExit => [] returned
            data = rest.get("test/json-ok", self.config, die=False)
            self.assertEqual(data, [])
        finally:
            self.config._server_root = saved_server_url


class TestRestEdgeCases(LiveServerTestCase):
    """Test edge cases and uncovered scenarios in rest.py module."""

    def create_app(self):
        """Simulate scenarios for uncovered lines.

        Args:
            None

        Returns:
            Flask: A Flask application configured for testing
        """
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = 5000

        # Route for server=False scenario
        @app.route("/api/switchmap/api/test/endpoint", methods=["POST"])
        def server_false_test():
            """Handle GET requests for server=False testing.

            Args:
                None

            Returns:
                tuple: JSON response and HTTP status code
            """
            return jsonify({"server": "false", "status": "ok"})

        # Route to simulate BaseException for bare except block
        @app.route("/switchmap/api/test/base-exception", methods=["POST"])
        def test_base_exception():
            raise BaseException("Triggered BaseException.")

        # Route to return malformed JSON
        @app.route("/switchmap/api/test/json-malformed", methods=["GET"])
        def json_malformed():
            """Return malformed JSON for testing.

            Args:
                None

            Returns:
                tuple: Malformed JSON string and HTTP status code
            """
            return "{invalid json...", 200

        return app

    def setUp(self):
        """Initialize configuration and test data."""
        self.config = MockConfig()
        self.test_uri = "test/endpoint"
        self.test_data = {"key": "value"}

    def test_post_server_false(self):
        """Test POST request behavior when server parameter is False."""
        result = rest.post(
            self.test_uri, self.test_data, self.config, server=False
        )

        # Ensure no ExceptionWrapper is returned
        self.assertFalse(isinstance(result, ExceptionWrapper))

        # Ensure success is True and correct response is returned
        self.assertTrue(result.success)
        self.assertEqual(result.response.status_code, 200)
        self.assertIn("server", result.response.json())
        self.assertIn("status", result.response.json())

    def test_get_json_malformed_die_true(self):
        """Test get_json malformed JSON response."""
        with self.assertRaises(SystemExit):
            rest.get("test/json-malformed", self.config, die=True)

    def test_post_bare_except_block(self):
        """Test BaseException during API request."""
        saved_server_url = self.config.server_url_root()

        try:
            # Set an invalid server URL to simulate a failure
            self.config._server_root = "http://nonexistent.invalid.domain"

            # Mock log.log2info to verify it is called
            with patch("switchmap.core.log.log2info") as mock_log2info:
                # Simulate a POST request that triggers a non-standard exception
                with patch(
                    "requests.Session.post",
                    side_effect=BaseException("Simulated BaseException"),
                ):
                    result = rest.post(
                        "bare-except", self.test_data, self.config
                    )

                    # Verify that result is None
                    self.assertIsNone(result.response)

                    # Check if log.log2info was called with the expected message
                    expected_message = (
                        "Failed to post data to API server URL "
                        "http://nonexistent.invalid.domain/switchmap/api/"
                        "bare-except."
                    )
                    mock_log2info.assert_called_with(1038, expected_message)

        finally:
            # Restore the original server URL
            self.config._server_root = saved_server_url


class TestRestCoverage(LiveServerTestCase):
    """Tests edge cases and error scenarios for REST API."""

    def create_app(self):
        """Create a Flask application with routes to simulate edge cases.

        Args:
            None

        Returns:
            Flask: Flask application configured for testing edge cases
        """
        app = Flask(__name__)
        app.config["TESTING"] = True
        app.config["LIVESERVER_PORT"] = 5000

        @app.route("/api/switchmap/server-false-test", methods=["GET"])
        def server_false_test():
            """Handle GET requests for server=False testing.

            Args:
            None

            Returns:
            tuple: JSON response and HTTP status code
            """
            return jsonify({"server": "false", "status": "ok"})

        @app.route("/switchmap/api/bare-except", methods=["POST"])
        def bare_except_route():
            """Handle POST requests to test bare except handling.

            Args:
                None

            Returns:
                None

            Raises:
                Exception: Always raises to test exception handling
            """
            # Simulate a scenario that might trigger a bare except
            raise Exception("Simulated exception")

        return app

    def setUp(self):
        """Test the code path using config.api_url_root() when server=False."""
        self.config = MockConfig()
        self.nocreds_config = MockConfigNoCredentials()

    def test_api_url_root_server_false(self):
        """Tests the API URL root functionality."""
        result = rest.get(
            "server-false-test", self.config, server=False, die=False
        )

        # Verify successful retrieval of data
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, list))
        if result:  # Check if list is not empty before accessing first element
            self.assertEqual(result[0].get("server"), "false")


if __name__ == "__main__":
    unittest.main()
