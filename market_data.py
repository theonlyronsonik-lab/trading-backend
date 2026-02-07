import requests
from config import TWELVE_DATA_API_KEY, CANDLE_LIMIT

BASE_URL = "https://api.twelvedata.com/time_series"


def fetch_candles(symbol: str, interval: str):
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": CANDLE_LIMIT,
        "apikey": TWELVE_DATA_API_KEY,
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") == "error":
        print(f"No candle data for {symbol} ({interval})")
        print("Response:", data)
        return None

    candles = data.get("values")
    if not candles:
        return None

    candles.reverse()  # oldest → newest
    return candles
