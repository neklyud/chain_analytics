from datetime import datetime
import pandas as pd
from core.models.web3.blocks import EthBlockWithTrx
import asyncio
from loguru import logger
from core.http_client.async_tools import gather_with_concurrency
from web3_source import AsyncWeb3HTTPSource
from web3_target import AsyncWeb3S3Target
from config import config
from core.components.loader.base_loader import AsyncBaseLoader, BaseAsyncSource, BaseAsyncTarget
from core.models.web3.blocks import EthBlock
from typing import Optional
from datetime import timedelta
from aiolimiter import AsyncLimiter
from core.tools.inspection import decorate
from core.tools.coro_rate_limiter import limiter
from typing import Union, List, Callable


class AsyncWeb3BlocksExporter(object):
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

    async def get_trx_by_period(self, start_date: datetime, end_date: datetime) -> list:
        assert end_date > start_date
        start_block_number: int = await self.get_block_number_by_timestamp(
            start_date,
            start_date - timedelta(minutes=30),
            start_date + timedelta(minutes=30),
        )
        end_block_number: int = await self.get_block_number_by_timestamp(
            end_date,
            end_date - timedelta(minutes=30),
            end_date + timedelta(minutes=30),
        )
        logger.info(
            "Start block number: {}. End block number: {}. Num blocks: {}".format(
                start_block_number,
                end_block_number,
                end_block_number - start_block_number),
        )
        assert start_block_number < end_block_number
        blocks = []
        for i_block_num in range(start_block_number, end_block_number):
            blocks.append(await self.get_block_with_trx(i_block_num))
        return blocks


class AsyncWeb3Loader(AsyncBaseLoader):
    def __init__(
            self,
            source: Union[AsyncWeb3BlocksExporter],
            target: BaseAsyncTarget,
            before_handlers: Optional[List[Callable]] = None,
    ):
        self.source = source
        self.before = before_handlers
        self.target = target
        if not self.before:
            self.before = []

    async def load(self, dt_1: datetime, dt_2: datetime) -> None:
        """Load data from source and pack it to the target."""

        blocks: list = await self.source.get_trx_by_period(dt_1, dt_2)
        logger.info(f"From {dt_1} to {dt_2} finded {len(blocks)} blocks.")
        for i_before_handler in self.before:
            await i_before_handler(blocks)
        await self.target.push_data(blocks)



if __name__ == '__main__':
    infura = InfuraItem(provider_address=config.Providers.ropsten_infura, rate_limit=(10, 1))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        infura.get_trx_by_period(
            datetime(year=2021, month=11, day=1),
            datetime(year=2021, month=11, day=1) + timedelta(minutes=20)
        )
    )
    # loop.run_until_complete(
    #     loader.load(dt_1=datetime(year=2021, month=11, day=1), dt_2=datetime(year=2021, month=11, day=2)))
