#!/usr/bin/env python3
"""Infoset queries."""

import time
from collections import defaultdict

from switchmap.snmp import jm_iana_enterprise
from switchmap.snmp import get_queries


class Query(object):
    """Class interacts with IfMIB devices.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, snmp_object):
        """Function for intializing the class.

        Args:
            snmp_object: SNMP Interact class object from snmp_manager.py

        Returns:
            None

        """
        # Define query object
        self.snmp_object = snmp_object

    def everything(self):
        """Get all information from device.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = {}

        # Append data
        data['misc'] = self.misc()
        data['layer1'] = self.layer1()
        data['layer2'] = self.layer2()
        data['layer3'] = self.layer3()
        data['system'] = self.system()

        # Return
        return data

    def misc(self):
        """Provide miscellaneous information about device and the poll.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize data
        data = defaultdict(lambda: defaultdict(dict))
        data['timestamp'] = int(time.time())
        data['host'] = self.snmp_object.hostname()

        # Get vendor information
        sysobjectid = self.snmp_object.sysobjectid()
        vendor = jm_iana_enterprise.Query(sysobjectid=sysobjectid)
        data['IANAEnterpriseNumber'] = vendor.enterprise()

        # Return
        return data

    def system(self):
        """Get all system information from device.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize data
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        # Get system information from SNMPv2-MIB, ENTITY-MIB, IF-MIB
        # Instantiate a query object for each system query
        for item in [
                Query(self.snmp_object)
                for Query in get_queries('system')]:

            if item.supported():
                processed = True
                data = _add_system(item, data)

        # Return
        if processed is True:
            return data
        else:
            return None

    def layer1(self):
        """Get all layer1 information from device.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize key values
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        # Get information layer1 queries

        for item in [
                Query(self.snmp_object)
                for Query in get_queries('layer1')]:
            if item.supported():
                processed = True
                data = _add_layer1(item, data)

        # Return
        if processed is True:
            return data
        else:
            return None

    def layer2(self):
        """Get all layer2 information from device.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        for item in [
                Query(self.snmp_object)
                for Query in get_queries('layer2')]:
            if item.supported():
                processed = True
                data = _add_layer2(item, data)

        # Return
        if processed is True:
            return data
        else:
            return None

    def layer3(self):
        """Get all layer3 information from device.

        Args:
            None

        Returns:
            data: Aggregated data

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        processed = False

        for item in [
                Query(self.snmp_object)
                for Query in get_queries('layer3')]:
            if item.supported():
                processed = True
                data = _add_layer3(item, data)

        # Return
        if processed is True:
            return data
        else:
            return None


def _add_data(source, target):
    """Add data from source to target dict. Both dicts must have two keys.

    Args:
        source: Source dict
        target: Target dict

    Returns:
        target: Aggregated data

    """
    # Process data
    for primary in source.keys():
        for secondary, value in source[primary].items():
            target[primary][secondary] = value

        # Return
    return target


def _add_layer1(query, original_data):
    """Add data from successful layer1 MIB query to original data provided.

    Args:
        query: MIB query object
        original_data: Two keyed dict of data

    Returns:
        new_data: Aggregated data

    """
    # Process query
    result = query.layer1()
    new_data = _add_data(
        result, original_data)

    # Return
    return new_data


def _add_layer2(query, original_data):
    """Add data from successful layer2 MIB query to original data provided.

    Args:
        query: MIB query object
        original_data: Two keyed dict of data

    Returns:
        new_data: Aggregated data

    """
    # Process query
    result = query.layer2()
    new_data = _add_data(
        result, original_data)

    # Return
    return new_data


def _add_layer3(query, original_data):
    """Add data from successful layer3 MIB query to original data provided.

    Args:
        query: MIB query object
        original_data: Two keyed dict of data

    Returns:
        new_data: Aggregated data

    """
    # Process query
    result = query.layer3()
    new_data = _add_data(
        result, original_data)

    # Return
    return new_data


def _add_system(query, data):
    """Add data from successful system MIB query to original data provided.

    Args:
        query: MIB query object
        data: Three keyed dict of data

    Returns:
        data: Aggregated data

    """
    # Process query
    result = query.system()

    # Add tag
    for primary in result.keys():
        for secondary in result[primary].keys():
            for tertiary, value in result[primary][secondary].items():
                data[primary][secondary][tertiary] = value

    # Return
    return data
