# config.py

# ===== MARKET API =====
MARKET_API_KEY = "YOUR_API_KEY"

# ===== SYMBOLS (PAIRS TO ANALYZE) =====
SYMBOLS = [
    "XAUUSD",  # Gold
    "EURUSD",  # Euro / USD
    "GBPUSD",  # GBP / USD
    "USDJPY",  # USD / JPY
    # Add more pairs here
]

# ===== TIMEFRAMES =====
HTF = "1h"      # Higher Timeframe for structure bias (1H)
LTF = "15m"     # Lower Timeframe for entry confirmations (15m)

CANDLE_LIMIT = 200  # Number of candles to fetch

# ===== TELEGRAM =====
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
BOT_NAME = "Multi-Analyzer Bot"

# ===== RISK & SETTINGS =====
RISK_REWARD = 2  # Reward to risk ratio
COOLDOWN_SECONDS = 300  # Time between checks for each symbol (5 minutes)
