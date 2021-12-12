import aiohttp

from base_http import HTTPParameters
from aiohttp import ClientResponse


class AsyncHTTPClient(object):
    async def request(self, request_parameter: HTTPParameters) -> ClientResponse:
        async with aiohttp.ClientSession() as session:
            async with session.request(*request_parameter) as response:
                return response
