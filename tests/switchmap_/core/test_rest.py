#!/usr/bin/env python3
"""Test the rest module."""

import os
import sys
import unittest
from unittest.mock import Mock, patch

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

from switchmap.core import rest
from switchmap.core.log import ExceptionWrapper


class MockConfig:
    """Mock configuration class for testing."""

    def server_username(self):
        """Return mock username."""
        return "test_user"

    def server_password(self):
        """Return mock password."""
        return "test_pass"

    def server_url_root(self):
        """Return mock server URL."""
        return "http://localhost:5000"

    def api_url_root(self):
        """Return mock API URL."""
        return "http://localhost:5000/api"


class TestREST(unittest.TestCase):
    """Checks all REST functions and methods."""

    def setUp(self):
        """Setup the test case."""
        self.config = MockConfig()
        self.test_url = "http://localhost:5000"
        self.test_uri = "test/endpoint"
        self.test_data = {"key": "value"}

    def test_clean_url(self):
        """Testing function _clean_url."""
        urls = [
            "http://example.com//api//v1//data",
            "https://example.com//api//v1//data",
            "http:/example.com/api/v1/data",
            "https:/example.com/api/v1/data",
        ]
        expected = [
            "http://example.com/api/v1/data",
            "https://example.com/api/v1/data",
            "http://example.com/api/v1/data",
            "https://example.com/api/v1/data",
        ]

        for i, url in enumerate(urls):
            result = rest._clean_url(url)
            self.assertEqual(result, expected[i])

    def test_post_success_no_auth(self):
        """
        Testing function post with successful response
        when no authentication is used.
        """
        mock_config = MockConfig()
        mock_config.server_username = lambda: ""
        mock_config.server_password = lambda: ""

        mock_response = Mock()
        mock_response.status_code = 200

        with patch("requests.Session") as mock_session:
            mock_session_instance = (
                mock_session.return_value.__enter__.return_value
            )
            mock_session_instance.post.return_value = mock_response
            result = rest.post(self.test_uri, self.test_data, mock_config)
            self.assertTrue(result.success)
            self.assertEqual(result.response.status_code, 200)

    def test_post_external_api(self):
        """Testing function post with API server flag set to False."""
        mock_response = Mock()
        mock_response.status_code = 200

        with patch("requests.Session") as mock_session:
            mock_session_instance = (
                mock_session.return_value.__enter__.return_value
            )
            mock_session_instance.post.return_value = mock_response
            result = rest.post(
                self.test_uri, self.test_data, self.config, server=False
            )
            self.assertTrue(result.success)
            self.assertEqual(result.response.status_code, 200)

    def test_get_success_with_graphql(self):
        """Testing get_graphql function with successful response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"test": "value"}}

        with patch("switchmap.core.rest._get") as mock_get:
            mock_get.return_value = type(
                "obj",
                (object,),
                {"success": True, "response": mock_response},
            )()
            result = rest.get_graphql("query { test }", self.config)
            self.assertEqual(result, {"data": {"test": "value"}})

    def test_get_json_failure(self):
        """Testing _get_json method with JSON parsing failure."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")

        with patch("switchmap.core.rest._get") as mock_get, patch(
            "switchmap.core.log.log2info"
        ) as mock_log:
            mock_get.return_value = type(
                "obj",
                (object,),
                {"success": True, "response": mock_response},
            )()
            result = rest.get("test/uri", self.config, die=False)
            self.assertEqual(result, [])
            mock_log.assert_called_once()

    def test_get_successful_with_streaming(self):
        """Testing _get method with streaming enabled."""
        mock_response = Mock()
        mock_response.ok = True

        with patch("requests.Session") as mock_session:
            mock_session_instance = mock_session.return_value.__enter__()
            mock_session_instance.get.return_value = mock_response
            result = rest._get("http://test.com", self.config, stream=True)
            self.assertTrue(result.success)
            self.assertEqual(result.response, mock_response)

    def test_get_with_query_parameter(self):
        """Testing _get method with query parameter."""
        mock_response = Mock()
        mock_response.ok = True

        with patch("requests.Session") as mock_session:
            mock_session_instance = mock_session.return_value.__enter__()
            mock_session_instance.get.return_value = mock_response
            result = rest._get(
                "http://test.com", self.config, query="test query"
            )
            self.assertTrue(result.success)
            self.assertEqual(result.response, mock_response)
            mock_session_instance.get.assert_called_with(
                "http://test.com",
                stream=False,
                auth=(
                    self.config.server_username(),
                    self.config.server_password(),
                ),
                params={"query": "test query"},
            )


class TestPostFunction(unittest.TestCase):
    """Test cases specifically for the post function."""

    def setUp(self):
        """Set up mock configuration and test data."""
        self.mock_config = MockConfig()
        self.test_uri = "test/endpoint"
        self.test_data = {"key": "value"}

    @patch("requests.Session")
    @patch("switchmap.core.log.log2warning")
    @patch("switchmap.core.log.log2exception")
    def test_post_exception_handling_block(
        self, mock_log_exception, mock_log_warning, mock_session
    ):
        """Test post function exception block."""
        mock_session.return_value.__enter__.return_value.post.side_effect = (
            Exception("Custom Exception")
        )

        result = rest.post(self.test_uri, self.test_data, self.mock_config)

        mock_log_warning.assert_called_once()
        mock_log_exception.assert_called_once()
        self.assertIsInstance(result, ExceptionWrapper)

    @patch("requests.Session")
    def test_post_api_url_root(self, mock_session):
        """Test post uses api_url_root when server=False."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.return_value.__enter__.return_value.post.return_value = (
            mock_response
        )

        result = rest.post(
            self.test_uri, self.test_data, self.mock_config, server=False
        )
        self.assertTrue(result.success)
        self.assertEqual(result.response.status_code, 200)

    @patch("requests.Session")
    def test_post_error_logging(self, mock_session):
        """Test logging when POST response has an error status code."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_session.return_value.__enter__.return_value.post.return_value = (
            mock_response
        )
        result = rest.post(self.test_uri, self.test_data, self.mock_config)
        self.assertFalse(result.success)
        self.assertEqual(result.response.status_code, 500)

    @patch("requests.Session")
    def test_post_successful_request(self, mock_session):
        """Test a 200 OK response for post."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session.return_value.__enter__.return_value.post.return_value = (
            mock_response
        )

        result = rest.post(self.test_uri, self.test_data, self.mock_config)
        self.assertTrue(result.success)
        self.assertEqual(result.response.status_code, 200)


class TestRESTAdditional(unittest.TestCase):
    """Additional tests to cover `_get_json` and `_get` exception handling."""

    def setUp(self):
        """Shared mock config for these tests."""
        self.mock_config = MockConfig()
        self.test_uri = "test/endpoint"
        self.test_data = {"key": "value"}

    @patch("switchmap.core.rest._get")
    @patch("switchmap.core.log.log2die")
    def test_get_json_failure_with_die(self, mock_log_die, mock_get):
        """Test JSON parsing fails with die=True."""
        mock_log_die.side_effect = lambda *args, **kwargs: sys.exit()
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Bad JSON")
        mock_get.return_value = type(
            "obj",
            (object,),
            {"success": True, "response": mock_response},
        )()

        with self.assertRaises(SystemExit):
            rest._get_json("http://test.com", self.mock_config, die=True)

        mock_log_die.assert_called_once()

    @patch("requests.Session")
    def test_get_exception_handling(self, mock_session):
        """Test `_get` exception handling with die=False."""
        mock_session.return_value.__enter__.return_value.get.side_effect = (
            Exception("Test Exception")
        )

        result = rest._get("http://test.com", self.mock_config, die=False)
        self.assertFalse(result.success)
        self.assertEqual(result.response, [])


class TestMissingCoverage(unittest.TestCase):
    """Tests covering code paths not hit in standard scenarios."""

    def setUp(self):
        self.config = MockConfig()
        self.test_uri = "test/endpoint"
        self.test_data = {"key": "value"}

    @patch("requests.Session")
    def test_post_bare_except_block(self, mock_session):
        """
        Force the bare `except:` block in `post` (lines 73-77)
        by raising a non-`Exception` error.
        """
        mock_session.return_value.__enter__.return_value.post.side_effect = (
            BaseException("Generic BaseException")
        )
        with self.assertRaises(UnboundLocalError):
            rest.post(self.test_uri, self.test_data, self.config)

    @patch("requests.Session")
    @patch("switchmap.core.log.log2info")
    def test_post_server_false_line_119(self, mock_log_info, mock_session):
        """
        Covers line 119 by calling post(..., server=False).
        Confirms api_url_root usage.
        """
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_session.return_value.__enter__.return_value.post.return_value = (
            mock_response
        )
        result = rest.post(
            self.test_uri, self.test_data, self.config, server=False
        )
        self.assertTrue(result.success)

        expected_fragment = (
            "http://localhost:5000/api/switchmap/api/test/endpoint"
        )
        found_attempt_log = any(
            expected_fragment in str(call_args)
            for call_args in mock_log_info.call_args_list
        )
        self.assertTrue(found_attempt_log)

    @patch("requests.Session")
    def test_get_exception_die_true_line_233(self, mock_session):
        """
        Covers line 233 in `_get` by forcing an exception
        and leaving die=True.
        """
        mock_session.return_value.__enter__.return_value.get.side_effect = (
            Exception("Simulated GET failure")
        )

        with self.assertRaises(SystemExit):
            rest._get("http://test.com", self.config, die=True)

    def test_get_with_external_api_server_false(self):
        """Test get(...) with server=False picks api_url_root."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        with patch("requests.Session") as mock_session:
            ((mock_session.return_value.__enter__().get.return_value)) = (
                mock_response
            )
            result = rest.get("external/endpoint", self.config, server=False)
            self.assertIsInstance(result, list)
            self.assertEqual(
                mock_session.return_value.__enter__.return_value.get.call_count,
                1,
            )


if __name__ == "__main__":
    unittest.main()
