import requests
from config import MARKET_API_KEY


def fetch_candles(symbol, interval, limit):
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": MARKET_API_KEY,
        "limit": limit,
        "format": "JSON",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if "values" not in data or not data["values"]:
            print(f"No candle data for {symbol} ({interval})")
            print(f"Response: {data}")
            return None

        return data["values"]

    except Exception as e:
        print(f"Market data error for {symbol}: {e}")
        return None
