import requests
from config import TWELVE_DATA_API_KEY, CANDLE_LIMIT


def fetch_candles(symbol, timeframe):
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": TWELVE_DATA_API_KEY,
        "outputsize": CANDLE_LIMIT,
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        print(f"No candle data for {symbol} ({timeframe})")
        print("Response:", data)
        return None

    candles = []
    for c in reversed(data["values"]):
        candles.append({
            "open": float(c["open"]),
            "high": float(c["high"]),
            "low": float(c["low"]),
            "close": float(c["close"])
        })

    return candles
