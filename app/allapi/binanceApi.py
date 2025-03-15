import aiohttp
import logging

from typing import Dict
from datetime import datetime, timedelta
from retry import retry


price_cache: Dict[str, tuple[float, datetime]] = {}
CACHE_DURATION = timedelta(minutes=1)


@retry(exceptions=(aiohttp.ClientError, Exception), tries=3, delay=2, backoff=2)
async def track_price() -> str:
    """
    Fetches the current price of cryptocurrencies from Binance API
    """

    try:
        now = datetime.utcnow()
        if price_cache and all(
            now - timestamp < CACHE_DURATION for _, timestamp in price_cache.values()
        ):
            prices = {sym: price for sym, (price, _) in price_cache.items()}
            return format_prices(prices)

        url = "https://api.binance.com/api/v3/ticker/price"
        symbols = [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT",
            "XRPUSDT",
            "ADAUSDT",
            "SOLUSDT",
            "DOTUSDT",
            "DOGEUSDT",
            "MATICUSDT",
            "LTCUSDT",
            "LINKUSDT",
            "BUSDUSDT",
            "VETUSDT",
            "XLMUSDT",
            "TRXUSDT",
        ]

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                if res.status != 200:
                    logging.error(f"Binance API error: Status {res.status}")
                    return "Error fetching price data"
                data = await res.json()

        prices = {}
        for sym in data:
            if sym["symbol"] in symbols:
                prices[sym["symbol"]] = float(sym["price"])
                price_cache[sym["symbol"]] = (float(sym["price"]), now)

        return format_prices(prices)

    except aiohttp.ClientError as e:
        logging.error(f"Network error in track_price: {e}")
        return "Network error while fetching prices"
    except Exception as e:
        logging.error(f"Unexpected error in track_price: {e}")
        return "Error fetching price data"


def format_prices(prices: Dict[str, float]) -> str:
    return "\n".join(
        [f"Price of {sym}: {price:.2f} USDT" for sym, price in prices.items()]
    )
