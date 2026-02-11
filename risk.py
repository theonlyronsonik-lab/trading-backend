def calculate_dynamic_sl(entry, swing, bias):
    if bias == "bullish":
        return swing - (entry * 0.001)

    if bias == "bearish":
        return swing + (entry * 0.001)


def calculate_tp(entry, sl, bias, target):
    return target
