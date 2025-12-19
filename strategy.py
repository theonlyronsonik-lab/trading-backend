from data_feed import get_candles
from market_structure import detect_bos
from liquidity import detect_liquidity
from sessions import get_session, session_valid
from telegram import send_message
from config import SYMBOL, HTF, LTF

def run_strategy():
    htf = get_candles(SYMBOL, HTF)
    ltf = get_candles(SYMBOL, LTF)

    if not htf or not ltf:
        return

    bias = detect_bos(htf)
    if bias is None:
        return

    liquidity = detect_liquidity(ltf)
    if bias == "BULLISH" and liquidity != "sweep_low":
        return
    if bias == "BEARISH" and liquidity != "sweep_high":
        return

    session = get_session(ltf[-1]["time"])
    if not session_valid(session):
        return

    entry_price = ltf[-1]["close"]

    message = f"""
📊 XAUUSD SIGNAL
Bias: {bias}
Session: {session}
Liquidity: {liquidity}
Timeframe: 15M
Entry: {entry_price}
"""

    send_message(message)
