#!/usr/bin/env python3
"""Test the general module."""

import unittest
import os
import sys
import json

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

from switchmap.core import graphene as testimport


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        CONFIG.cleanup()

    def test_normalize(self):
        """Testing function normalize with standard input."""
        expected = {
            "roots": [
                {
                    "event": {
                        "zones": [
                            {
                                "devices": [
                                    {
                                        "hostname": "device01.example.org",
                                        "idxDevice": 27,
                                    },
                                    {
                                        "hostname": "device02.example.org",
                                        "idxDevice": 28,
                                    },
                                ],
                                "name": "TEST",
                            }
                        ]
                    }
                }
            ]
        }

        data_string = """
        {
          "data": {
            "roots": {
              "edges": [
                {
                  "node": {
                    "event": {
                      "zones": {
                        "edges": [
                          {
                            "node": {
                              "name": "TEST",
                              "devices": {
                                "edges": [
                                  {
                                    "node": {
                                      "hostname": "device01.example.org",
                                      "idxDevice": 27
                                    }
                                  },
                                  {
                                    "node": {
                                      "hostname": "device02.example.org",
                                      "idxDevice": 28
                                    }
                                  }
                                ]
                              }
                            }
                          }
                        ]
                      }
                    }
                  }
                }
              ]
            }
          }
        }
        """
        data = json.loads(data_string).get("data")
        result = testimport.normalize(data)
        self.assertEqual(result, expected)

    def test_normalize_empty(self):
        """Test normalize with empty input."""
        self.assertEqual(testimport.normalize({}), {})
        self.assertEqual(testimport.normalize(None), None)

    def test_normalize_no_edges(self):
        """Test normalize with no 'edges' key in the input."""
        data = {
            "roots": {
                "event": {"zones": {"devices": [{"hostname": "device01"}]}}
            }
        }
        expected = data
        self.assertEqual(testimport.normalize(data), expected)

    def test_nodes(self):
        """Testing function nodes with standard input."""
        expected = [
            {
                "name": "TEST",
                "devices": [
                    {"hostname": "device01.example.org", "idxDevice": 27},
                    {"hostname": "device02.example.org", "idxDevice": 28},
                ],
            }
        ]

        data_string = """
        {
          "edges": [
            {
              "node": {
                "name": "TEST",
                "devices": {
                  "edges": [
                    {
                      "node": {
                        "hostname": "device01.example.org",
                        "idxDevice": 27
                      }
                    },
                    {
                      "node": {
                        "hostname": "device02.example.org",
                        "idxDevice": 28
                      }
                    }
                  ]
                }
              }
            }
          ]
        }
        """
        data = json.loads(data_string).get("edges")
        result = testimport.nodes(data)
        self.assertEqual(result, expected)

    def test_nodes_empty(self):
        """Test nodes with empty input."""
        self.assertEqual(testimport.nodes([]), [])

    def test_nodes_no_node_key(self):
        """Test nodes with missing 'node' key."""
        data = [{"no_node": {"name": "TEST"}}]
        self.assertEqual(testimport.nodes(data), [None])

    def test_normalize_deeply_nested(self):
        """Test normalize with deeply nested input."""
        data = {
            "outer": {
                "edges": [
                    {"node": {"inner": {"edges": [{"node": {"value": 1}}]}}},
                    {"node": {"inner": {"edges": [{"node": {"value": 2}}]}}},
                ]
            }
        }
        expected = {
            "outer": [{"inner": [{"value": 1}]}, {"inner": [{"value": 2}]}]
        }
        self.assertEqual(testimport.normalize(data), expected)

    def test_nodes_deeply_nested(self):
        """Test nodes with deeply nested input."""
        data = [
            {
                "node": {
                    "inner": {
                        "edges": [
                            {"node": {"value": 1}},
                            {"node": {"value": 2}},
                        ]
                    }
                }
            }
        ]
        expected = [{"inner": [{"value": 1}, {"value": 2}]}]
        self.assertEqual(testimport.nodes(data), expected)


if __name__ == "__main__":
    unittest.main()
