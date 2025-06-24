"""
Debug testing script to test the new async SNMP polling implementation of switchmap-ng
"""

import sys
import os
import asyncio


sys.path.insert(0,'/Users/imexyyyyy/files/gsoc/switchmap-ng');

# once i make polling async then will update this according to that to check if devices are being polled asynchronously