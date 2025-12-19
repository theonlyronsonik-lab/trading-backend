import requests

def get_price():
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": "XAUUSD",
        "interval": "15min",
        "apikey": "YOUR_API_KEY",
        "outputsize": 100
    }
    r = requests.get(url).json()
    return r["values"]
