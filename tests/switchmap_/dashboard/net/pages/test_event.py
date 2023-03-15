#!/usr/bin/env python3
"""Test the topology module."""

import os
import sys
import unittest

# Try to create a working PYTHONPATH
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
_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}dashboard{0}net{0}pages".format(
        os.sep
    )
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


# Create the necessary configuration to load the module
from tests.testlib_ import setup

CONFIG = setup.config()
CONFIG.save()

from switchmap.dashboard.net.pages import event as testimport
from switchmap.dashboard import EventMeta


class Test_RawCol(unittest.TestCase):
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

    def test_td_format(self):
        """Testing function td_format."""
        pass


class TestEventPage(unittest.TestCase):
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

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_html(self):
        """Testing function html."""
        # Initialize key variables
        expected = """<div class="row">
      <div class="col-lg-12">
          <div class="panel panel-default">
              <div class="panel-heading">
                  Polling Event Dates
              </div>
              <!-- /.panel-heading -->
              <div class="panel-body">
                  <div class="table-responsive table-bordered">
                      <table class="table">
<tbody>
<tr><td><a href="/switchmap/2">2023-03-13 23:09:07</a></td><td></td><td></td><td></td><td></td><td></td></tr>
</tbody>
</table>
                  </div>
                  <!-- /.table-responsive -->
              </div>
              <!-- /.panel-body -->
          </div>
          <!-- /.panel -->
      </div>
    </div>"""

        # Get arguments
        events = [
            {"event": {"tsCreated": "2023-03-14 16:56:01"}, "idxRoot": 1},
            {"event": {"tsCreated": "2023-03-13 23:09:07"}, "idxRoot": 2},
        ]
        class_obj = testimport.EventPage(events)

        # Test
        result = class_obj.html()
        self.assertEqual(result, expected)


class TestEventTable(unittest.TestCase):
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

    def test___init__(self):
        """Testing function __init__."""
        pass


class TestEventsRow(unittest.TestCase):
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

    def test___init__(self):
        """Testing function __init__."""
        pass


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

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_rows(self):
        """Testing function rows."""
        # Initialize key variables
        events = [
            {"event": {"tsCreated": "2023-03-14 16:56:01"}, "idxRoot": 1},
            {"event": {"tsCreated": "2023-03-13 23:09:07"}, "idxRoot": 2},
            {"event": {"tsCreated": "2023-03-13 23:25:51"}, "idxRoot": 3},
        ]
        rows = [
            EventMeta(
                date=_.get("event").get("tsCreated"), idx_root=_.get("idxRoot")
            )
            for _ in events
        ]

        # Test
        result = testimport.rows(rows)[0]
        self.assertEqual(
            result.col0,
            '<a href="/switchmap/3">2023-03-13 23:25:51</a>',
        )
        self.assertEqual(
            result.col1,
            '<a href="/switchmap/2">2023-03-13 23:09:07</a>',
        )


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
