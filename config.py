# config.py

# -----------------------------
# SYMBOLS AND TIMEFRAMES
# -----------------------------
SYMBOLS = ["XAU/USD", "USD/JPY", "GBP/USD", "GBP/NZD"]  # add more symbols here
HTF = "1h"  # Higher Timeframe
LTF = "5min"  # Lower Timeframe
LOOP_DELAY = 120  # seconds between API calls to respect free plan limits

# -----------------------------
# TELEGRAM CONFIG
# -----------------------------
TELEGRAM_BOT_TOKEN = "8529456380:AAF2Ed2EoEtGRTfAX4a67Vd89KSnMUImdQc"
TELEGRAM_CHAT_ID = "6599172354"

# -----------------------------
# LTF ENTRY SETTINGS
# -----------------------------
MIN_CONFIRMATIONS = 2  # minimum confirmations for LTF signal
CONFIRMATIONS_TOTAL = 8  # total confirmations considered
