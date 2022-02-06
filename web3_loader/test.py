from web3 import Web3, HTTPProvider
import time
from config import config
from datetime import datetime


def estimate_block_height_by_timestamp(web3, timestamp):
    block_found = False
    last_block_number = web3.eth.getBlock('latest')['number']
    close_in_seconds = 600

    while not block_found:
        try:
            block = web3.eth.getBlock(last_block_number)
        except Exception:
            last_block_number = last_block_number//2
            print(last_block_number)
            continue
        block_time = datetime.fromtimestamp(block.timestamp)
        difference_in_seconds = int((timestamp - block_time).total_seconds())
        print(difference_in_seconds)
        block_found = abs(difference_in_seconds) < close_in_seconds

        if block_found:
            return last_block_number

        if difference_in_seconds < 0:
            last_block_number //= 2
        else:
            last_block_number = int(last_block_number * 1.5) + 1


def main():
    w3 = Web3(
        provider=HTTPProvider(endpoint_uri=config.Providers.ropsten_infura)
    )
    estimate_block_height_by_timestamp(w3, timestamp=datetime(day=10, month=10, year=2020))


if __name__ == '__main__':
    main()
