#!/usr/bin/env python3
"""Test the jm_general module."""

import unittest

from switchmap.db import db_agent
from switchmap.db.db_orm import Agent
from switchmap.db import db
from switchmap.utils import jm_general


class TestGetIDX(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_agent_good = 1
    good_agent = db_agent.GetIDX(idx_agent_good)

    # Get agent data using SQLalchemy directly
    database = db.Database()
    session = database.session()
    result = session.query(Agent).filter(
        Agent.idx == idx_agent_good).one()
    database.close()
    good_id = jm_general.decode(result.id)

    # Create a dict of all the expected values
    expected = {
        'uid': good_id,
        'last_timestamp': good_agent.last_timestamp(),
        'name': '_switchmap.,
        'enabled': True
    }

    def test_init_getidx(self):
        """Testing method init."""
        # Test with non existent AgentIDX
        with self.assertRaises(SystemExit):
            _ = db_agent.GetIDX(-1)

    def test_uid_getidx(self):
        """Testing method uid."""
        # Testing with known good value
        result = self.good_agent.uid()
        self.assertEqual(result, self.expected['uid'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.uid()
        self.assertNotEqual(result, expected)

    def test_name_getidx(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_enabled_getidx(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)

    def test_last_timestamp_getidx(self):
        """Testing method last_timestamp."""
        # Testing with known good value
        result = self.good_agent.last_timestamp()
        self.assertEqual(result, self.expected['last_timestamp'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.last_timestamp()
        self.assertNotEqual(result, expected)

    def test_everything_getidx(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_agent.everything()
        for key in self.expected.keys():
            self.assertEqual(result[key], self.expected[key])


class TestGetUID(unittest.TestCase):
    """Checks all functions and methods."""

    # Intstantiate a good agent
    idx_agent_good = 1

    # Get agent data using SQLalchemy directly
    database = db.Database()
    session = database.session()
    result = session.query(Agent).filter(
        Agent.idx == idx_agent_good).one()
    database.close()

    # Here's the data
    good_id = jm_general.decode(result.id)
    good_agent = db_agent.GetUID(good_id)

    # Create a dict of all the expected values
    expected = {
        'idx': 1,
        'name': '_switchmap.,
        'last_timestamp': good_agent.last_timestamp(),
        'enabled': True
    }

    def test_init_getuid(self):
        """Testing method __init__."""
        # Test with non existent AgentID
        with self.assertRaises(SystemExit):
            _ = db_agent.GetUID('bogus')

    def test_idx_getuid(self):
        """Testing method idx."""
        # Testing with known good value
        result = self.good_agent.idx()
        self.assertEqual(result, self.expected['idx'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx()
        self.assertNotEqual(result, expected)

    def test_name_getuid(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_enabled_getuid(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)

    def test_last_timestamp_getuid(self):
        """Testing method last_timestamp."""
        # Testing with known good value
        result = self.good_agent.last_timestamp()
        self.assertEqual(result, self.expected['last_timestamp'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.last_timestamp()
        self.assertNotEqual(result, expected)

    def test_everything_getuid(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_agent.everything()
        for key in self.expected.keys():
            self.assertEqual(result[key], self.expected[key])


class TestGetDataPoint(unittest.TestCase):
    """Checks all functions and methods."""

    def test_init_getdatapoint(self):
        """Testing method __init__."""
        pass

    def test_everything_getdatapoint(self):
        """Testing method everything."""
        pass


class Other(unittest.TestCase):
    """Checks all functions and methods."""

    # Intstantiate a good agent
    idx_agent_good = 1
    good_agent = db_agent.GetIDX(idx_agent_good)

    # Get agent data using SQLalchemy directly
    database = db.Database()
    session = database.session()
    result = session.query(Agent).filter(
        Agent.idx == idx_agent_good).one()
    database.close()
    good_id = jm_general.decode(result.id)

    def test_uid_exists(self):
        """Testing function uid_exists."""
        # Testing with known good value
        expected = True
        result = db_agent.uid_exists(self.good_id)
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agent.uid_exists('bogus')
        self.assertEqual(result, expected)

    def test_idx_exists(self):
        """Testing function idx_exists."""
        # Testing with known good value
        expected = True
        result = db_agent.idx_exists(self.idx_agent_good)
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agent.idx_exists(None)
        self.assertEqual(result, expected)


if __name__ == '__main__':

    # Do the unit test
    unittest.main()
