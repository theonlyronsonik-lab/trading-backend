import requests
import time
from config import TWELVEDATA_API_KEY, HTF_CACHE

BASE_URL = "https://api.twelvedata.com/time_series"


def fetch_data(symbol, interval, outputsize=200):
    url = BASE_URL
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": TWELVEDATA_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "values" not in data:
        return None

    candles = data["values"]
    candles.reverse()
    return candles


def fetch_htf_cached(symbol, interval, htf_seconds):
    now = time.time()

    if symbol in HTF_CACHE:
        last_fetch = HTF_CACHE[symbol]["time"]
        if now - last_fetch < htf_seconds:
            return HTF_CACHE[symbol]["data"]

    data = fetch_data(symbol, interval)
    if data:
        HTF_CACHE[symbol] = {
            "time": now,
            "data": data
        }

    return data
