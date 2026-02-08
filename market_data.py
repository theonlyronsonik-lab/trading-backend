import requests
from config import TWELVE_DATA_API_KEY


BASE_URL = "https://api.twelvedata.com/time_series"


def fetch_candles(symbol, interval, limit=200):
    """
    symbol: e.g. 'XAU/USD', 'EUR/USD'
    interval: '15min', '1h', '4h'
    """

    params = {
        "symbol": symbol,
        "interval": interval,
        "apikey": TWELVE_DATA_API_KEY,
        "outputsize": limit,
        "format": "JSON"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print(f"HTTP error for {symbol}: {response.text}")
        return None

    data = response.json()

    if data.get("status") == "error":
        print(f"No candle data for {symbol} ({interval})")
        print("Response:", data)
        return None

    candles = data.get("values", [])

    if not candles:
        print(f"Empty candles for {symbol}")
        return None

    # Convert to chronological order
    candles.reverse()

    return candles
