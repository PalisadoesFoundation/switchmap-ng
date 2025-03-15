#!/usr/bin/env python3
"""Unittests for the API Graphql routes.

This module tests the functionality in the Graphql endpoint.
"""

import json
import os
import random
import sys
import unittest

from flask import Flask

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

from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.server.api.routes.graphql import API_GRAPHQL
from switchmap.server.db import models
from switchmap.server.db.table import IDevice
from switchmap.server.db.table import device as testimport
from tests.testlib_ import data, db


class TestGraphqlAPIRoute(unittest.TestCase):
    """Test graphql route."""

    @classmethod
    def setUpClass(cls) -> None:
        """Start up resources for class."""
        config = setup.config()
        config.save()

        models.create_all_tables()

        db.populate()

    @classmethod
    def tearDownClass(cls) -> None:
        """Cleanup class resources."""
        from switchmap.server.db import SCOPED_SESSION

        if (
            SCOPED_SESSION is not None
        ):  # makes sure no session is active before dropping connection
            SCOPED_SESSION.remove()

        database = db.Database()
        database.drop()

        CONFIG.cleanup()

    def setUp(self) -> None:
        """Start up resources for each test."""
        self.app = Flask(__name__)
        self.app.register_blueprint(API_GRAPHQL)

        self.client = self.app.test_client()

    def test_graphql_no_query(self) -> None:
        """Test providing no query returns errors."""
        resp = self.client.get("/graphql")

        data = resp.json
        self.assertEqual(resp.status_code, 400)
        self.assertGreater(len(data), 0)
        self.assertIn("errors", data)
        self.assertDictEqual(
            data["errors"][0], {"message": "Must provide query string."}
        )

    def test_graphql_query(self) -> None:
        """Test valid query returns correct response."""
        query = """
            {
              devices{
                edges {
                  node {
                    sysName
                    name
                    hostname
                    sysObjectid
                    sysDescription
                    sysUptime
                    enabled
                    lastPolled
                  }
                }
              }
            }
        """

        new_device = IDevice(
            idx_zone=1,
            sys_name=data.random_string(),
            hostname=data.random_string(),
            name=data.random_string(),
            sys_description=data.random_string(),
            sys_objectid=data.random_string(),
            sys_uptime=random.randint(0, 1000000),
            last_polled=random.randint(0, 1000000),
            enabled=1,
        )

        testimport.insert_row(new_device)

        response = self.client.post(
            "/graphql",
            data=json.dumps({"query": query}),
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json)

        sys_names = [
            res["node"]["sysName"]
            for res in response.json["data"]["devices"]["edges"]
        ]
        self.assertIn(new_device.sys_name, sys_names)

    def test_graphql_invalid_query(self) -> None:
        """Test invalid query returns correct error response."""
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
            headers={"Content-Type": "application/json"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.json)
        self.assertEqual(
            response.json["errors"][0]["message"],
            "Cannot query field 'NoneExistentField' on type 'Query'.",
        )


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
