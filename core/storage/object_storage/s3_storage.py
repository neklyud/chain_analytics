from config import config
from aiobotocore.session import AioSession, get_session
from contextlib import AsyncExitStack
from base import BaseS3Client, BaseS3Manager
import asyncio
import logging
from typing import List, Optional

logger = logging.Logger(name="S3StorageLogger")
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s'")
ch.setFormatter(formatter)
logger.addHandler(ch)


class S3Client(BaseS3Client):
    url: str = config.url
    login: str = config.login
    password: str = config.password

    def __init__(self):
        self._exit_stack: AsyncExitStack = AsyncExitStack()
        self._s3_client = None
        self.session = get_session()

    async def __aenter__(self):
        if not self._s3_client:
            self._s3_client = await self._exit_stack.enter_async_context(
                self.session.create_client(
                    's3',
                    endpoint_url=self.url,
                    aws_access_key_id=self.login,
                    aws_secret_access_key=self.password,
                )
            )
        return self._s3_client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.aclose()

    @property
    def client(self):
        if not self._s3_client:
            raise Exception("Client Not Started")
        return self._s3_client


class S3Manager(BaseS3Manager):
    def __init__(self):
        self.loop = loop
        self._s3 = S3Client()

    async def list_buckets(self):
        async with self._s3 as client:
            buckets = await client.list_buckets()
            return buckets

    async def list_objects(self, bucket_name: str, prefix: Optional[str] = None) -> List[str]:
        async with self._s3 as client:
            try:
                objects = await client.list_objects(Bucket=bucket_name, Prefix=prefix)
                return objects
            except Exception as ex:
                if "NoSuchBucket" in str(ex):
                    return []
                logger.exception(ex)

    async def get_object(self, bucket_name: str, object_name: str) -> bytes:
        async with self._s3 as client:
            try:
                s3_object = await client.get_object(Bucket=bucket_name, Key=object_name)
                return s3_object['Body']
            except Exception as ex:
                logger.exception(ex)

    async def put_object(self, bucket_name: str, object_name: str, bytes_object: bytes) -> None:
        async with self._s3 as client:
            try:
                await client.put_object(Bucket=bucket_name, Key=object_name, Body=bytes_object)
                logger.info(
                    msg="Object {object} was created in {bucket}.".format(object=object_name, bucket=bucket_name))
            except Exception as ex:
                if "NoSuchBucket" in str(ex):
                    await self.create_bucket(bucket_name=bucket_name)
                    await client.put_object(Bucket=bucket_name, Key=object_name, Body=bytes_object)
                    return
                logger.exception(ex)

    async def delete_bucket(self, bucket_name: str, recursive: bool = False):
        async with self._s3 as client:
            try:
                if recursive:
                    pass
                await client.delete_bucket(Bucket=bucket_name)
                logger.info(msg="Bucket {bucket} was deleted.".format(bucket=bucket_name))
            except Exception as ex:
                if "NoSuchBucket" in str(ex):
                    logger.warning(msg="Bucket {bucket} not found".format(bucket=bucket_name))
                    return
                logger.exception(ex)

    async def create_bucket(self, bucket_name: str) -> None:
        async with self._s3 as client:
            try:
                await client.create_bucket(Bucket=bucket_name)
                logger.info(msg="Bucket {bucket} was created.".format(bucket=bucket_name))
            except Exception as ex:
                if "BucketAlreadyOwnedByYou" in str(ex):
                    logger.warning(msg="Bucket {bucket} already created".format(bucket=bucket_name))
                    return
                logger.exception(ex)
