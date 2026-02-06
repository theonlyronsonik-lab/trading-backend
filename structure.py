# structure.py

def get_structure_bias(candles):
    """Simple logic to define market structure bias"""
    # Here, add your logic for higher timeframe analysis.
    # For simplicity, let's say the market is in a bullish bias if the close is higher than open.
    
    if candles[-1]['close'] > candles[-1]['open']:  # Just an example for bullish
        return "BULLISH"
    elif candles[-1]['close'] < candles[-1]['open']:
        return "BEARISH"
    else:
        return "NEUTRAL"

