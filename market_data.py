import requests
from config import MARKET_API_KEY, SYMBOLS

def fetch_candles(symbol, timeframe, limit):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={timeframe}&apikey={MARKET_API_KEY}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "values" in data:
            return data["values"]
        else:
            print(f"Error: No data found for {symbol}.")
            return None
    else:
        print(f"Error fetching {symbol} candles: {response.text}")
        return None

