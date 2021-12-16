from core.components.loader.base_loader import BaseSource
from web3 import Web3, HTTPProvider
from datetime import datetime
from core.models.web3.blocks import EthBlock


class Web3HttpSource(BaseSource):
    def __init__(self, provider_address: str):
        self.provider = Web3(HTTPProvider(provider_address))

    @property
    def block_number(self) -> int:
        return self.provider.eth.block_number

    @property
    def latest_block(self) -> EthBlock:
        return EthBlock(**self.provider.eth.get_block("latest"))

    def get_block(self, block_number: int) -> EthBlock:
        return EthBlock(**self.provider.eth.get_block(block_number))

    def get_data(self, start_date: datetime, end_time: datetime) -> EthBlock:
        pass


def get_block_number_by_timestamp(web3_source: Web3HttpSource, timestamp: float, depth_speed_estimate: int):
    current_block: EthBlock = web3_source.latest_block
    print(f"Current block: {current_block.number}")
    print(datetime.fromtimestamp(current_block.timestamp), datetime.fromtimestamp(timestamp))
    if current_block.timestamp < timestamp:
        raise Exception("Your timestamp in future, stupid!")

    if depth_speed_estimate > current_block.timestamp - timestamp:
        raise Exception("Depth of estimation is too big")

    num_blocks = 0

    for i_depth in range(1, depth_speed_estimate):
        block_ = web3_source.get_block(current_block.number - depth_speed_estimate)
        if block_.number == current_block.number:
            continue
        num_blocks += 1

    speed = float(num_blocks) / depth_speed_estimate
    estimated_block_number = round(speed * (current_block.timestamp - timestamp))
    print(
        f"Speed: {speed}, estimate: {estimated_block_number}, num_blocks: {current_block.number - estimated_block_number}")
    source.provider.eth.get_block(current_block.number - estimated_block_number)
    return current_block.number - estimated_block_number


if __name__ == '__main__':
    from config import config

    source = Web3HttpSource(config.Providers.mainnet_infura)
    print(f"Requested date: {datetime.fromtimestamp(datetime.utcnow().timestamp() - 5000)}")
    est = get_block_number_by_timestamp(source, datetime.now().timestamp() - 50000, 10)
    print(datetime.fromtimestamp(source.provider.eth.get_block(est)['timestamp']))
