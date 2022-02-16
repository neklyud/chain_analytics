from datetime import datetime
from core.models.web3.blocks import EthBlockWithTrx
import asyncio
from loguru import logger
from core.components.web3.source import AsyncWeb3HTTPSource
from core.models.web3.blocks import EthBlock
from typing import Optional
from aiolimiter import AsyncLimiter
from core.tools.inspection import decorate
from core.tools.coro_rate_limiter import limiter


class AsyncWeb3BlocksFinder(object):
    def __init__(self, provider_address: str, rate_limit: Optional[tuple] = None):
        self.source: AsyncWeb3HTTPSource = AsyncWeb3HTTPSource(provider_address=provider_address)
        if rate_limit:
            self.source = decorate(self.source, limiter(AsyncLimiter(*rate_limit)))

    async def get_block_number_by_timestamp(
            self,
            target_ts: datetime,
            lower_ts: datetime,
            higher_ts: datetime,
            average_block_time: int = 17 * 3.5
    ) -> int:
        target_timestamp = target_ts.timestamp()
        higher_limit_stamp = higher_ts.timestamp()
        lower_limit_stamp = lower_ts.timestamp()
        block: EthBlock = await self.source.latest_block()
        requests_made = 0
        block_number = block.number
        while block.timestamp >= target_timestamp:
            decrease_blocks = int((block.timestamp - target_timestamp) / average_block_time)
            block_number -= decrease_blocks
            block = await self.source.get_block(block_number)
            logger.info(f"{datetime.fromtimestamp(block.timestamp)}")
            requests_made += 1
            if not decrease_blocks:
                break

        logger.info(
            f"Block number of first approximation: {block.number}. Timestamp: {datetime.fromtimestamp(block.timestamp)}")
        logger.info(f"{higher_limit_stamp}, {lower_limit_stamp}")
        if lower_limit_stamp and block.timestamp < lower_limit_stamp:
            while block.timestamp < lower_limit_stamp:
                block_number += 1
                block = await self.source.get_block(block_number)
                logger.info(f"{datetime.fromtimestamp(block.timestamp)}")
                requests_made += 1

        if higher_limit_stamp:
            if block.timestamp >= higher_limit_stamp:
                while block.timestamp >= higher_limit_stamp:
                    block_number -= 1
                    block = self.source.get_block(block_number)
                    logger.info(f"{datetime.fromtimestamp(block.timestamp)}")
                    requests_made += 1

        logger.info(f"{block.timestamp}, {higher_limit_stamp}")
        logger.info(f"Block number: {block.number}; block timestamp: {block.timestamp}")
        return block.number

    async def get_block_with_trx(self, block_number: int) -> EthBlockWithTrx:
        logger.info("Request for get block with trx with block number: {}".format(block_number))
        eth_block: EthBlock = await self.source.get_block(block_number)
        get_trx_tasks: list = []
        transactions_in_block: list = []
        for i_trx in eth_block.transactions:
            get_trx_tasks.append(asyncio.create_task(self.source.get_transaction(i_trx)))
        response = await asyncio.gather(*get_trx_tasks)
        for i_resp in response:
            transactions_in_block.append(i_resp)
        dict_block = eth_block.dict()
        dict_block["transactions"] = transactions_in_block
        return EthBlockWithTrx(**dict_block)
