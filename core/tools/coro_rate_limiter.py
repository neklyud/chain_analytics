from aiolimiter import AsyncLimiter
from typing import Callable
from aiohttp.client_exceptions import ClientConnectorError
import asyncio
from loguru import logger


NUM_RETRIES = 5


def limiter(async_limiter: AsyncLimiter):
    def outer(func: Callable):
        async def inner(*args: list, **kwargs: dict):
            async with async_limiter:
                for i_retry in range(NUM_RETRIES):
                    try:
                        response = await func(*args, **kwargs)
                        return response
                    except ClientConnectorError:
                        logger.info("Error occured while coro processed.")
                        await asyncio.sleep(5)
                        response = await func(*args, **kwargs)
                        return response
                    except Exception as ex:
                        logger.error("Error occured by response call. Retry number: {}".format(i_retry))
                        if i_retry == NUM_RETRIES - 1:
                            raise ex
        return inner
    return outer
