from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet
from core.models.web3.blocks import EthBlock, Hex
from core.components.web3.base.base_source import AsyncBaseWeb3


class AsyncWeb3HTTPSource(AsyncBaseWeb3):
    def __init__(self, provider_address: str):
        self.provider = Web3(
            provider=AsyncHTTPProvider(endpoint_uri=provider_address),
            modules={"eth": (AsyncEth,), 'net': (AsyncNet,)},
            middlewares=[],
        )

    async def get_block(self, block_number: int) -> EthBlock:
        block = await self.provider.eth.get_block(block_number)
        return EthBlock(**block)

    async def latest_block(self) -> EthBlock:
        last_block = await self.provider.eth.get_block("latest")
        return EthBlock(**last_block)

    async def get_transaction(self, trx_hash: Hex) -> dict:
        trx: dict = await self.provider.eth.get_transaction(trx_hash)
        return trx
