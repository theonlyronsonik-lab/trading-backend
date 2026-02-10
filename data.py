import time
import requests
from config import TWELVE_DATA_API_KEY

LAST_API_CALL = 0
MIN_API_INTERVAL = 8  # seconds (8 calls/min max)

def get_candles(symbol, timeframe, limit=100):
    global LAST_API_CALL

    now = time.time()
    elapsed = now - LAST_API_CALL

    if elapsed < MIN_API_INTERVAL:
        time.sleep(MIN_API_INTERVAL - elapsed)

    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "limit": limit,
        "apikey": TWELVE_DATA_API_KEY
    }

    response = requests.get(url, params=params)
    LAST_API_CALL = time.time()

    data = response.json()

    if data.get("status") == "error":
        if data.get("code") == 429:
            print("⚠️ API limit hit. Sleeping 60 seconds...")
            time.sleep(60)
            return None
        raise Exception(f"TwelveData error: {data}")

    return data.get("values", [])
