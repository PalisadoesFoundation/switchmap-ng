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
        ),
        os.pardir,
    )
)
_EXPECTED = (
    "{0}switchmap-ng{0}tests{0}switchmap_{0}"
    "dashboard{0}net{0}html{0}pages".format(os.sep)
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

from switchmap.dashboard.net.html.pages import layouts as testimport


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

    def test_table_wrapper(self):
        """Testing function table_wrapper."""
        # Initialize key variables
        title = "akjdfsheww"
        table_html = "ewda233e5"
        expected = """\
<div class="row">
      <div class="col-lg-12">
          <div class="panel panel-default">
              <div class="panel-heading">
                {0}
              </div>
              <!-- /.panel-heading -->
              <div class="panel-body">
                {1}
              </div>
              <!-- /.panel-body -->
          </div>
          <!-- /.panel -->
      </div>
    </div>""".format(
            title, table_html
        ).strip()

        # Test
        result = testimport.table_wrapper(title, table_html)
        self.assertEqual(result, expected)

    def test_remove_thead(self):
        """Testing function remove_thead."""
        # Initialize key variables
        data = """\
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Curabitur thead in porta lorem. Vivamus tortor ligula, consectetur
dignissim a, malesuada non nisi. Sed vulputate gravida efficitur.\
"""
        expected = """\
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
dignissim a, malesuada non nisi. Sed vulputate gravida efficitur.\
"""
        # Test
        result = testimport.remove_thead(data)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
