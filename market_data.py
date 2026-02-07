import requests

API_KEY = "d143e9bb8b0c4d7487872fd699280bde"

def fetch_candles(symbol, interval):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": CANDLE_LIMIT,
        "apikey": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 🚨 STOP if API limit reached
    if response.status_code == 429 or data.get("status") == "error":
        print(f"❌ API issue for {symbol} ({interval})")
        print("Response:", data)
        return None

    return data.get("values", [])
