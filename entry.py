from data import get_candles

def detect_market_structure(candles, bias): """ Confirms LTF pullback + continuation """ if len(candles) < 20: return False

last = candles[-1]
prev = candles[-5]

if bias == "BULLISH" and last['close'] > prev['high']:
    return True
if bias == "BEARISH" and last['close'] < prev['low']:
    return True

return False

def detect_supply_demand(candles, bias): """ Simple zone logic: Demand = last strong down candle before push up Supply = last strong up candle before drop """ for c in reversed(candles[-20:]): body = abs(c['close'] - c['open']) wick = c['high'] - c['low']

if wick == 0:
        continue

    if bias == "BULLISH" and c['close'] < c['open'] and body / wick > 0.6:
        return c['low']

    if bias == "BEARISH" and c['close'] > c['open'] and body / wick > 0.6:
        return c['high']

return None

def find_ltf_entry(symbol, bias): candles = get_candles(symbol, "15min", limit=100) if not candles: return None

if not detect_market_structure(candles, bias):
    return None

zone = detect_supply_demand(candles, bias)
if zone is None:
    return None

price = candles[-1]['close']

if bias == "BULLISH":
    sl = zone - (price - zone) * 0.2
    tp = price + (price - sl) * 3
else:
    sl = zone + (zone - price) * 0.2
    tp = price - (sl - price) * 3

rr = abs((tp - price) / (price - sl))
if rr < 3:
    return None

return (
    f"🚀 LTF ENTRY FOUND ({symbol})\n"
    f"Bias: {bias}\n"
    f"Entry: {price}\n"
    f"SL: {round(sl, 5)}\n"
    f"TP: {round(tp, 5)}\n"
    f"RR: 1:{round(rr, 2)}"
)
