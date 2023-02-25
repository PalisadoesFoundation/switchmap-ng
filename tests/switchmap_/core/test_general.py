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
            "0JlUPySw1VLuphGkVJjhZmPxnEEu8eihywTciZTNaOD7tHCTit52Deao1PTSWNYYpzoojux89E6FAEJCMUgwC71G3mpzRPu6udE1",
            "w69AybQFfgLkXtm8u9I99GCMX2CbKOVL8FvtrfaGgxsfOsvv5DNyzFkg9W7v66L4feSJrLIBNkAGePp8Px8iDH5elyoqcA33Wi8D",
            "UN6RV2vJPJIUeaZCq2zgCwDS8nxPCj5NyCTEdd3agWpN0T98efeLnW4zTb6OjXqBCuFOR6K8k9JazewFidyKYV9hMZVwLcqVt3rC",
            "opQahEmXLaLp34fcb5QqUBAvMXqqcXvQd3FPks5Vy5vUmT8JCfRAvYukomSFueZlRbfROsJ30a12QiUzb25MPCE5gR3furDNcWKa",
            "7ZE9EDOn2HgX7t7ILJzzZjAFFoZUcpXy4Acwfar2oahOASBO43CiBQNMDIi5sA0YBUJTSaUhmQQGPSOEkuQr8ul2bHAGw5czz3Fq",
            "Ycl1W8yAXe1yDBBtj9GqE59ub2zKVouX49UqGGQDM4bReajWy41WaW6FEnN7yKtgkCx9ZgtSeLuXqx1srB5QHvoCmkeVRtjRE6o6",
            "Pn67lJ9iUktjHB6eBHIQDM4bReajWy41WaW6FEnBrMAcWWS56vkDWzxgsAiPp6jPf9BgagxYIviUbf7Zsj6O913CcIjdPOKCOsb9",
            "ymWHSh8Algz1kCDe0jjXHFmzwfAeEfkFgWDUANDZ4YwnskjhOLUDXy5TTvGjzGI9aZsLGj2jis9dvLqBzGI9aZsLGj2jis9dvLqB",
            "41V1HBtDgR3G1lsvKXcTP9qgael8VXRhpVzs3p5azGI9aZsLGj2jis9dvLqBrH8WeTCg4yxr720v3Gxw3TQDMZA36pnnM1TrosDE",
            "1yq3IkESIJHtCmd4DU5bcgA65KCu53QWVGffPfSnFzn1FlfBtmNZqcGCcskbJjbp7rfFF1tuavZuAq9Igh0CxsXJCZTXLqqlq4MB",
            "gNeubyGzheQqKRUy6auYvmPh1RYZDM5mQQKmTG1HbjxtHBqvMq4NQuKgMMjPEnqfFWSvuqAD2klELXh7oT83z1uxPagj223xyqKB",
            "Vlux8kE8QKGYC7YanvEggutKQAJt8r3wtPQEGwk9leqxdctCijjMsnNIp4TFTMsvEkuMXGtwg3nJXRLcYy0Q4CWhTCZrZdecEPY2",
        ]
        expected = [
            "01ee8ecad7c5",
            "69abff8999c2",
            "62eac2cd8c5c",
            "aea34fcb5bac",
            "7e9ed277affc",
            "c18ae1dbb9e5",
            "679b6ebd4bea",
            "8a1cde0ffaee",
            "411bd31c9ae8",
            "13ecd4d5bca6",
            "ebe6a1d51bb4",
            "8e8c7aea83e9",
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


if __name__ == "__main__":
    # Do the unit test
    unittest.main()
