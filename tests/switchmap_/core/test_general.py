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
from switchmap import MacAddress
from switchmap.core import general


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

    def test_check_sudo(self):
        """Testing function check_sudo."""
        # Test with sudo variable set
        result = "SUDO_UID" in os.environ
        self.assertEqual(result, False)

        # Test with sudo variable set
        os.environ["SUDO_UID"] = getpass.getuser()
        with self.assertRaises(SystemExit):
            general.check_sudo()

    def test_check_user(self):
        """Testing function check_user."""
        pass

    def test_cleanstring(self):
        """Testing method / function cleanstring."""
        # Initializing key variables
        dirty_string = "   {}\n   \r {}   \n {}  ".format(
            self.random_string, self.random_string, self.random_string
        )
        clean_string = "{} {} {}".format(
            self.random_string, self.random_string, self.random_string
        )

        # Test result
        result = general.cleanstring(dirty_string)
        self.assertEqual(result, clean_string)

    def test_octetstr_2_string(self):
        """Testing function octetstr_2_string."""
        pass

    def test_random_hash(self):
        """Testing function random_hash."""
        # Test result
        result = general.random_hash()
        self.assertEqual(len(result), 32)
        self.assertTrue(bool(int(result, 16)))

    def test_root_directory(self):
        """Testing function root_directory."""
        # Test result
        result = general.root_directory()
        self.assertTrue(result.endswith("{}switchmap-ng".format(os.sep)))

    def test_mac(self):
        """Testing function mac."""
        # Initializing key variables
        macs = [
            "01ee.8eca.d7c5",
            "69ab.ff89.99c2",
            "62:ea:c2:cd:8c:5c",
            "ae.a3.4f.cb.5b.ac",
            "7e-9e-d2-77-af-fc",
            "c18ae1dbb9e5",
            "679b6ebd4bea",
            "8a1cde0ffaee",
            "411bd31c9ae8",
            "13ecd4d5bca6",
            "000000000000",
            "Titanic was a ship",
            None,
            False,
            True,
            [1],
            {1: 2},
            (1, 2),
            "13ecd4d5bca613ecd4d5bca6",
            "1234",
            1234,
            "zyxwvut",
        ]
        expected = [
            MacAddress(valid=True, mac="01ee8ecad7c5"),
            MacAddress(valid=True, mac="69abff8999c2"),
            MacAddress(valid=True, mac="62eac2cd8c5c"),
            MacAddress(valid=True, mac="aea34fcb5bac"),
            MacAddress(valid=True, mac="7e9ed277affc"),
            MacAddress(valid=True, mac="c18ae1dbb9e5"),
            MacAddress(valid=True, mac="679b6ebd4bea"),
            MacAddress(valid=True, mac="8a1cde0ffaee"),
            MacAddress(valid=True, mac="411bd31c9ae8"),
            MacAddress(valid=True, mac="13ecd4d5bca6"),
            MacAddress(valid=True, mac="000000000000"),
            MacAddress(valid=False, mac="Titanic was a ship"),
            MacAddress(valid=False, mac=None),
            MacAddress(valid=False, mac=False),
            MacAddress(valid=False, mac=True),
            MacAddress(valid=False, mac=[1]),
            MacAddress(valid=False, mac={1: 2}),
            MacAddress(valid=False, mac=(1, 2)),
            MacAddress(valid=False, mac="13ecd4d5bca613ecd4d5bca6"),
            MacAddress(valid=False, mac="1234"),
            MacAddress(valid=False, mac=1234),
            MacAddress(valid=False, mac="zyxwvut"),
        ]

        # Test
        for index, mac in enumerate(macs):
            result = general.mac(mac)
            self.assertEqual(result, expected[index])

    def test_ipaddress(self):
        """Testing function ipaddress."""
        # Initializing key variables
        expected = [
            IP(address="192.168.1.1", version=4),
            None,
            IP(address="0000:0000:0000:0000:0000:0abc:0007:0def", version=6),
        ]
        inputs = ["192.168.1.1", "abcdefghijklmnopqrstuvwxyz", "::abc:7:def"]

        # Test
        for index, item in enumerate(inputs):
            result = general.ipaddress(item)
            self.assertEqual(expected[index], result)

    def test_make_bool(self):
        """Testing function make_bool."""
        # Initializing key variables
        inputs = [
            -1,
            1,
            "akjdfk",
            "True",
            "true",
            "tRUe",
            "false",
            "False",
            "FalsE",
            None,
            "NoNe",
            "none",
            "",
            0,
        ]
        expected = [
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

        # Test
        for index, item in enumerate(inputs):
            result = general.make_bool(item)
            self.assertEqual(expected[index], result)

    def test_consistent_keys(self):
        """Testing function consistent_keys."""
        # Initializing key variables
        input_dict = {}
        _data = {1: True, "1": True, "ABC": True, False: True}
        expected = {
            0: {1: True, "ABC": True, 0: True},
            1: {1: True, "ABC": True, 0: True},
            2: {1: True, "ABC": True, 0: True},
        }

        # Test
        for _ in range(3):
            input_dict[_] = _data
        result = general.consistent_keys(input_dict)
        self.assertEqual(result, expected)

    def test_group_consecutive(self):
        """Testing function group_consecutive."""
        # Initializing key variables
        items = [
            [
                1,
                2,
                3,
                4,
                5,
                12,
                13,
                14,
                15,
                20,
                21,
                22,
                23,
                30,
                35,
                36,
                37,
                38,
                39,
                40,
            ],
            [2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20],
            [2, 3, 4, 17, 20, 5, 12, 13, 14, 15, 16],
            [
                2,
                3,
                4,
                15,
                16,
                15,
                16,
                15,
                16,
                17,
                20,
                5,
                12,
                13,
                14,
                15,
                16,
                15,
                16,
            ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [],
        ]
        expected = [
            [(1, 5), (12, 15), (20, 23), 30, (35, 40)],
            [(2, 5), (12, 17), 20],
            [(2, 5), (12, 17), 20],
            [(2, 5), (12, 17), 20],
            [0],
            [],
        ]

        # Test
        for key, value in enumerate(items):
            result = general.group_consecutive(value)
            self.assertEqual(result, expected[key])

    def test_human_readable(self):
        """Testing function human_readable."""
        # Initializing key variables
        items = [
            100,
            1000,
            10000,
            100000,
            1000000000,
            1000000000000,
            1000000000000000,
        ]
        expecteds = [
            "100.0",
            "100.0Z",
            "100.0Z",
            "1000.0",
            "1.0KZ",
            "1000.0Z",
            "9.8K",
            "10.0KZ",
            "9.8KZ",
            "97.7K",
            "100.0KZ",
            "97.7KZ",
            "953.7M",
            "1.0GZ",
            "953.7MZ",
            "931.3G",
            "1.0TZ",
            "931.3GZ",
            "909.5T",
            "1.0PZ",
            "909.5TZ",
        ]
        results = []
        arguments = [
            {"storage": True, "suffix": ""},
            {"storage": False, "suffix": "Z"},
            {"storage": True, "suffix": "Z"},
        ]
        for item in items:
            for argument in arguments:
                results.append(
                    general.human_readable(
                        item,
                        storage=argument.get("storage"),
                        suffix=argument.get("suffix"),
                    )
                )
        # Test
        for key, expected in enumerate(expecteds):
            self.assertEqual(results[key], expected)

    def test_padded_list_of_lists(self):
        """Testing function padded_list_of_lists."""
        # Initializing key variables
        expecteds = [
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
                [9, 10, 11],
                [12, 13, 14],
                [15, 16, 17],
                [18, 19, None],
            ],
            [
                [0, 1, 2, 3],
                [4, 5, 6, 7],
                [8, 9, 10, 11],
                [12, 13, 14, 15],
                [16, 17, 18, 19],
                [20, "", "", ""],
            ],
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
                [20, 21, 0, 0, 0],
            ],
            [
                [0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17],
                [18, 19, 20, 21, 22, [0]],
            ],
        ]
        data = [
            list(range(20)),
            list(range(21)),
            list(range(22)),
            list(range(23)),
        ]
        pads = [None, "", 0, [0]]
        widths = list(range(3, 7))

        # Test
        for key, value in enumerate(data):
            result = general.padded_list_of_lists(
                data[key], width=widths[key], pad=pads[key]
            )
            self.assertEqual(result, expecteds[key])


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
