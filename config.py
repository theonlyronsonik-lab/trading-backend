# config.py

# ===== MARKET API =====
MARKET_API_KEY = "d143e9bb8b0c4d7487872fd699280bde"

# ===== SYMBOLS (PAIRS TO ANALYZE) =====
SYMBOLS = [
    "XAU/USD",  # Gold
    "EUR/USD",  # Euro / USD
    "GBP/USD",  # GBP / USD
    "USD/JPY",  # USD / JPY
    # Add more pairs here
]

# ===== TIMEFRAMES =====
HTF = "1h"       # NOT 60m
LTF = "15min"    # or "5min" if you want faster entries

CANDLE_LIMIT = 200

# ===== TELEGRAM =====
TELEGRAM_BOT_TOKEN = "8529456380:AAF2Ed2EoEtGRTfAX4a67Vd89KSnMUImdQc"
TELEGRAM_CHAT_ID = "6599172354"
BOT_NAME = "Multi-Analyzer Bot"

# ===== RISK & SETTINGS =====
RISK_REWARD = 5  # Reward to risk ratio
COOLDOWN_SECONDS = 300  # Time between checks for each symbol (5 minutes)
