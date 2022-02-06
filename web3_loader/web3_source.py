from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.net import AsyncNet
from core.models.web3.blocks import EthBlock
from core.tools.coro_rate_limiter import limiter
from limiter import infura_limiter
from core.models.web3.blocks import Hex
from core.components.loader.base_source import AsyncBaseWeb3
from inspect import getmembers, ismethod, isfunction
from aiolimiter import AsyncLimiter


class AsyncWeb3HTTPSource(AsyncBaseWeb3):
    def __init__(self, provider_address: str):
        self.provider = Web3(
            provider=AsyncHTTPProvider(endpoint_uri=provider_address),
            modules={"eth": (AsyncEth,), 'net': (AsyncNet,)},
            middlewares=[],
        )

    # @limiter(infura_limiter)
    async def get_block(self, block_number: int) -> EthBlock:
        block = await self.provider.eth.get_block(block_number)
        return EthBlock(**block)

    # @limiter(infura_limiter)
    async def latest_block(self) -> EthBlock:
        last_block = await self.provider.eth.get_block("latest")
        return EthBlock(**last_block)

    # @limiter(infura_limiter)
    async def get_transaction(self, trx_hash: Hex) -> dict:
        trx: dict = await self.provider.eth.get_transaction(trx_hash)
        return trx


if __name__ == '__main__':
    from config import config
    import asyncio
    from datetime import datetime
    cli = AsyncWeb3HTTPSource(provider_address=config.Providers.ropsten_infura)
    loop = asyncio.get_event_loop()
    ans = loop.run_until_complete(cli.get_block(11797417)) # 11797417
    print(datetime.fromtimestamp(ans.timestamp))
