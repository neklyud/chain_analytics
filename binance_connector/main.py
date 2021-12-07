from binance import AsyncClient, DepthCacheManager, BinanceSocketManager
import asyncio
import logging
import hmac
import hashlib

logger = logging.getLogger()

BINANCE_API_KEY = 'HQHAsCySvgb5orWiArQCi5y7I3AiYFG2AG3M3oWMjhyKHzNQiUYLVXprmXToIYUd'
BINANCE_API_SECRET = 'EFmLlHTJvEL2j8rx5CC4sijEzL2RoIRq9lTOn2zNf01zJ6UzAFuadPDkQygqVQDe'


class BinanceLoader:
    def __init__(self):
        self.client = None

    def get_signature(self, query_string, secret):
        return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    async def get_client(self, api_key: str, api_secret: str) -> AsyncClient:
        if not self.client:
            self.client = await AsyncClient.create(api_key=api_key, api_secret=api_secret)
        return self.client

    async def get_orders(self):
        client = await self.get_client(BINANCE_API_KEY, BINANCE_API_SECRET)
        params = {
            'symbol': "BNBUSDT",
            'timestamp': 1637699958246,
            "signature": self.get_signature("timestamp=1637699958246", BINANCE_API_SECRET)
        }
        orders = await client.get_open_orders(params=params)
        return orders

    async def get_orderbook_tickers(self):
        client = await self.get_client(BINANCE_API_KEY, BINANCE_API_SECRET)
        tickers = await client.get_orderbook_tickers()
        return tickers

    async def close(self):
        if self.client:
            await self.client.close_connection()


def print_over_collection(coll):
    for i_coll in coll:
        print(i_coll)

async def main():
    loader = BinanceLoader()
    try:
        orders = await loader.get_orders()
        print_over_collection(orders)
    except Exception as ex:
        logger.exception(ex)
    await loader.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
