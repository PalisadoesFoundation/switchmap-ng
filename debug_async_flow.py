"""
Debug testing script to test the new async SNMP polling implementation of switchmap-ng
"""

import sys
import os
import asyncio


sys.path.insert(0,'/Users/imexyyyyy/files/gsoc/switchmap-ng');

# once i make polling async then will update this according to that to check if devices are being polled asynchronously
#for now for testing using cli_device to poll single device for debugging

from switchmap.poller import poll

def main():
    print("Switchmap polling flow debugger")

    try:

        hostname= "162.249.37.218"
        print(f"starting debug poll for hostname: {hostname}")

        poll.cli_device(hostname=hostname)
    
    except Exception as e:
        print(f"Error duing polling: {e}")

if __name__ == "__main__":
    main()

