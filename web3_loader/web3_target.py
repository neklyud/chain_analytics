import asyncio

from core.components.loader.base_loader import BaseAsyncTarget
from core.storage.object_storage.s3_storage import S3Manager
from config import config
import pandas as pd


class AsyncS3Target(BaseAsyncTarget):
    s3_manager = S3Manager()
    web3_bucket = config.S3

    async def push_data(self, csv: bytes, filename: str):
        await self.s3_manager.put_object(bucket_name=self.web3_bucket, object_name=filename, bytes_object=csv)


if __name__ == '__main__':
    csv_file = pd.read_csv('1.csv')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AsyncS3Target.push_data())