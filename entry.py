# entry.py

def confirm_entry(bias, candles):
    """Define entry strategy based on market bias and lower timeframe analysis"""
    # For example: entry confirmation if price goes above/below a moving average or liquidity zone
    if bias == "BULLISH" and candles[-1]['close'] > candles[-2]['close']:  # Example: simple uptrend
        return True
    elif bias == "BEARISH" and candles[-1]['close'] < candles[-2]['close']:
        return True
    return False

