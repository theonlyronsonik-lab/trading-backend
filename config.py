import os

# ==============================
# API CONFIG
# ==============================
API_KEY = "d143e9bb8b0c4d7487872fd699280bde"

# ==============================
# SYMBOLS
# ==============================
SYMBOLS = [
    "EUR/USD",
    "GBP/USD",
    "XAU/USD",
    "AUD/CAD"
]

# ==============================
# TIMEFRAMES
# ==============================
HTF = "1h"
LTF = "5min"

HTF_SECONDS = 3600  # 4H

# ==============================
# SCANNING CONTROL
# ==============================
SCAN_INTERVAL = 60  # seconds between scans
HTF_CACHE = {}      # stores last HTF fetch time per pair

# ==============================
# TRADING SETTINGS
# ==============================
RISK_PER_TRADE = 0.01
RR_MIN = 2

# ==============================
# TELEGRAM
# ==============================
TELEGRAM_BOT_TOKEN = "8529456380:AAF2Ed2EoEtGRTfAX4a67Vd89KSnMUImdQc"
TELEGRAM_CHAT_ID = "6599172354"
PAIR_STATE = {}
