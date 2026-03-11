# config.py

# -----------------------------
# SYMBOLS AND TIMEFRAMES
# -----------------------------
SYMBOLS = ["XAU/USD", "GBP/USD","GBP/JPY", "USD/JPY", "XAU/AUD"]  # add more symbols here
HTF = "5min"  # Higher Timeframe
LTF = "1min"  # Lower Timeframe
LOOP_DELAY = 30  # seconds between API calls to respect free plan limits

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
