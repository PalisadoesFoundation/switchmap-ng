# Create test_all_devices.py
import sys
sys.path.insert(0,'/Users/imexyyyyy/files/gsoc/switchmap-ng')

from switchmap.poller import async_poll

def main():
    print("Testing ALL devices async polling...")
    
    # Test with lower concurrency first
    async_poll.run_devices(max_concurrent_devices=3)

if __name__ == "__main__":
    main()