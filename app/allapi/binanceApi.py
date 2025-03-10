import aiohttp

async def track_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
                "SOLUSDT", "DOTUSDT", "DOGEUSDT", "MATICUSDT", "LTCUSDT",
                "LINKUSDT", "BUSDUSDT", "VETUSDT", "XLMUSDT", "TRXUSDT"]

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if (res.status != 200):
                return 'Ощибка получения данных'
            data = await res.json()
    
    prices = {sym["symbol"]: sym["price"] for sym in data if sym["symbol"] in symbols}
    return "\n".join([f'Цена {sym}: {price}' for sym, price in prices.items()])
