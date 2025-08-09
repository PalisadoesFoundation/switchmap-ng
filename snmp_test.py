#!/usr/bin/env python3
"""Test async_snmp_info.everything() using proper credential validation."""

import asyncio
import sys
import traceback
import time

sys.path.insert(0, ".")

from switchmap.poller.snmp.async_snmp_info import Query
from switchmap.poller.snmp import async_snmp_manager
from switchmap.poller.configuration import ConfigPoller
from switchmap.poller import POLLING_OPTIONS, POLL


async def test_everything():
    """Test everything() method with proper SNMP credential validation."""
    print("Testing async_snmp_info.everything()")

    hostname = "162.249.37.218"

    try:
        # SNMP configuration
        print(f"Getting SNMP configuration...")
        config = ConfigPoller()

        print(f"Validating SNMP credentials for {hostname}...")
        validate = async_snmp_manager.Validate(
            POLLING_OPTIONS(
                hostname=hostname, authorizations=config.snmp_auth()
            )
        )

        # Get valid authorization
        authorization = await validate.credentials()
        if not authorization:
            print(f"Failed to get valid SNMP credentials for {hostname}")
            return None

        snmp_object = async_snmp_manager.Interact(
            POLL(hostname=hostname, authorization=authorization)
        )

        print(f"Testing device connectivity...")
        is_contactable = await snmp_object.contactable()
        if not is_contactable:
            print(f"device {hostname} is not contactable via SNMP")
            return None

        print(f"device {hostname} is contactable!")

        # Get basic device info
        sysobjectid = await snmp_object.sysobjectid()
        enterprise_no = await snmp_object.enterprise_number()
        print(f"Device info:")
        print(f"SysObjectID: {sysobjectid}")
        print(f"Enterprise: {enterprise_no}")

        query_obj = Query(snmp_object)

        print(f"Calling everything() method...")
        print(f"wait a little...")

        start_time = time.time()
        everything_data = await query_obj.everything()
        end_time = time.time()

        print(f"Completed in {end_time - start_time:.2f} seconds")

        # Display results
        if everything_data:
            print(f"\nSUCCESS! everything() returned data :)))))))")
            print(f"Data str:")
            for key, value in everything_data.items():
                if isinstance(value, dict) and value:
                    print(f" {key}: {len(value)} items")
                    # Show sample of nested data
                    sample_key = list(value.keys())[0]
                    sample_value = value[sample_key]
                    if isinstance(sample_value, dict):
                        print(
                            f"Sample {sample_key}: {len(sample_value)} sub-items"
                        )
                    else:
                        print(f"Sample {sample_key}: {type(sample_value)}")
                elif isinstance(value, dict):
                    print(f" {key}: empty dict")
                else:
                    print(f" {key}: {type(value)} = {value}")
        else:
            print(f"everything() returned nonee result")

        return everything_data

    except Exception as e:
        print(f"ERROR: :(((((({e}")
        print(f"Full traceback:")
        traceback.print_exc()
        return None


async def main():
    """Main test function."""
    print("Async SNMP Info Test (Proper Credentials)")
    print("=" * 50)

    result = await test_everything()

    if result is not None:
        print(f"\nTest completed successfully!")
        return True
    else:
        print(f"\nTest failed!")
        return False


if __name__ == "__main__":
    print(" Running Async SNMP Test with Proper Credentials...")
    success = asyncio.run(main())

    if success:
        print("Test completed!")
        sys.exit(0)
    else:
        print("Test failed!")
        sys.exit(1)
