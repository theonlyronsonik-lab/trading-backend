import requests
from config import TWELVE_API_KEY

BASE_URL = "https://api.twelvedata.com/time_series"


def fetch_candles(symbol, timeframe, limit):
    params = {
        "symbol": symbol,
        "interval": timeframe,
        "apikey": TWELVE_API_KEY,
        "outputsize": limit
    }
    r = requests.get(BASE_URL, params=params).json()
    return r.get("values", [])


def get_swings(candles):
    highs = []
    lows = []

    for i in range(2, len(candles) - 2):
        h = float(candles[i]["high"])
        l = float(candles[i]["low"])

        if h > float(candles[i - 1]["high"]) and h > float(candles[i + 1]["high"]):
            highs.append(h)

        if l < float(candles[i - 1]["low"]) and l < float(candles[i + 1]["low"]):
            lows.append(l)

    return highs, lows


def analyse_htf_structure(candles):
    if len(candles) < 30:
        return "NO_DATA"

    highs, lows = get_swings(candles)

    if len(highs) < 2 or len(lows) < 2:
        return "NO_DATA"

    # last two swings
    h1, h2 = highs[-2], highs[-1]
    l1, l2 = lows[-2], lows[-1]

    # HH + HL
    if h2 > h1 and l2 > l1:
        return "BULLISH"

    # LH + LL
    if h2 < h1 and l2 < l1:
        return "BEARISH"

    return "RANGE"
