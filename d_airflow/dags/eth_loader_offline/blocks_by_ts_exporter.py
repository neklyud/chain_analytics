from core.components.web3.base.base_exporter import BaseExporter
from core.components.web3.finder import AsyncWeb3BlocksFinder
from datetime import datetime, timedelta
from loguru import logger
from models import BlocksNumbersByPeriodParams


class BlocksNumbersByPeriodExporter(BaseExporter):
    def __init__(self, finder: AsyncWeb3BlocksFinder):
        self.finder: AsyncWeb3BlocksFinder = finder

    async def export(self, export_params: BlocksNumbersByPeriodParams) -> list:
        assert export_params.end_timestamp > export_params.start_timestamp
        start_block_number: int = await self.finder.get_block_number_by_timestamp(
            export_params.start_timestamp,
            export_params.start_timestamp - timedelta(minutes=30),
            export_params.start_timestamp + timedelta(minutes=30),
        )
        end_block_number: int = await self.finder.get_block_number_by_timestamp(
            export_params.end_timestamp,
            export_params.end_timestamp - timedelta(minutes=30),
            export_params.end_timestamp + timedelta(minutes=30),
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
            blocks.append(await self.finder.get_block_with_trx(i_block_num))
            with open('/home/semyon/1.json', 'w') as f:
                import json
                f.write(json.dumps(blocks[-1].dict()))

        return blocks
