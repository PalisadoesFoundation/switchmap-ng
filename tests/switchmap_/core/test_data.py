#!/usr/bin/env python3
"""Test the general module."""

import getpass
import unittest
import random
import os
import sys
import string


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

from switchmap import IP
from switchmap.core import data


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Required
    maxDiff = None

    random_string = "".join(
        [random.choice(string.ascii_letters + string.digits) for n in range(9)]
    )

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

    def test_check_hashstring(self):
        """Testing function check_hashstring."""
        # Initializing key variables
        _string = (
            "f5rAwrU@Rop=Op-1QE$?yOs&@phit-=swoP*lqo6T!iwlcUthE2PistA7Re-"
        )
        shas = [1, 224, 384, 256, 512]
        expecteds = [
            "f53766caaf3a1f567c6013ecafb840818eee2901",
            "1ca8f5952d077dc378ae02deb6cec31587d3e6c064c51923e2ddde5c",
            "30b7c3d10960bfa47d304d3503bd247277aad3d145c135254e19f7b755806a7073af64e608a604595797d35136cb74fa",
            "4aeedc4229622c1724f7be54ad8f48ae748dc52b4bf14aadac50fc77a757fb01",
            "8bd7add2b47e3ad2e352d75a9392404e6b56bf2f91bddf092ceb0006a6097323b9dffd813f16aebc1c0f3b8f2e722d7ad5c2800c0930937bea62d7afb61bec95",
        ]

        # Test
        for key, sha in enumerate(shas):
            result = data.hashstring(_string, sha=sha)
            self.assertEqual(result, expecteds[key])

        for key, sha in enumerate(shas):
            result = data.hashstring(_string, sha=sha, utf8=True)
            self.assertEqual(result, expecteds[key].encode())

    def test_check_dictify(self):
        """Testing method / function check_dictify."""
        # Initializing key variables
        pass


if __name__ == "__main__":

    # Do the unit test
    unittest.main()
