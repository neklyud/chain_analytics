from core.components.web3.finder import AsyncWeb3BlocksFinder
from d_airflow.dags.eth_loader_offline.blocks_by_ts_exporter import BlocksNumbersByPeriodExporter
from models import BlocksNumbersByPeriodParams
import asyncio


def run(export_params: BlocksNumbersByPeriodParams, provider_address: str, num_tasks: int = 10,
        task_run_window: int = 1):
    finder = AsyncWeb3BlocksFinder(provider_address=provider_address, rate_limit=(num_tasks, task_run_window))
    exporter = BlocksNumbersByPeriodExporter(finder=finder)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(exporter.export(export_params))


if __name__ == '__main__':
    from datetime import datetime

    run(
        export_params=BlocksNumbersByPeriodParams(
            start_timestamp=datetime(year=2021, month=10, day=1),
            end_timestamp=datetime(year=2021, month=10, day=2)
        ),
        provider_address="https://ropsten.infura.io/v3/64df41bec1504ebc9dea88b8f4c595a7",
    )
