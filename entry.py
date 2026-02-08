def confirm_entry(bias, entry_price, sl, tp):
    """
    Returns True only if RR >= 1:3
    """

    risk = abs(entry_price - sl)
    reward = abs(tp - entry_price)

    if risk == 0:
        return False

    rr = reward / risk

    if rr >= 3:
        return True

    return False
