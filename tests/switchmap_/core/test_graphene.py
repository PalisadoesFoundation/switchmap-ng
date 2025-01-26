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

    #########################################################################
    # General object setup
    #########################################################################

    @classmethod
    def setUpClass(cls):
        """Execute these steps before starting tests."""
        # Load the configuration in case it's been deleted after loading the
        # configuration above. Sometimes this happens when running
        # `python3 -m unittest discover` where another the tearDownClass of
        # another test module prematurely deletes the configuration required
        # for this module
        config = setup.config()
        config.save()

    @classmethod
    def tearDownClass(cls):
        """Execute these steps when all tests are completed."""
        # Cleanup the
        CONFIG.cleanup()

    def test_normalize(self):
        """Testing function normalize."""
        # Initialize key variables
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
        # Convert data to dict
        data = json.loads(data_string).get("data")

        # Test
        result = testimport.normalize(data)
        self.assertEqual(result, expected)

    def test_nodes(self):
        """Testing function nodes."""
        # Initialize key variables
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
        # Convert data to dict
        data = json.loads(data_string).get("edges")

        # Test
        result = testimport.nodes(data)
        self.assertEqual(result, expected)

    def test_normalize_return_data(self):
        """Test normalize when input is not a dict and is directly returned."""
        input_data = "simple string"
        result = testimport.normalize(input_data)
        self.assertEqual(result, input_data)

    def test_nodes_append_node(self):
        """Test nodes appending non-dict node values."""
        input_data = [
            {"node": "simple string"},
            {"node": 42},
        ]
        expected_output = ["simple string", 42]
        result = testimport.nodes(input_data)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
