# market_data.py

import requests
from config import MARKET_API_KEY

def fetch_candles(symbol, timeframe, limit=200):
    url = f"https://api.marketdata.com/candles"
    params = {
        "symbol": symbol,
        "timeframe": timeframe,
        "limit": limit,
        "apikey": MARKET_API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['candles']
    else:
        print(f"Error fetching {symbol} candles: {response.text}")
        return None

