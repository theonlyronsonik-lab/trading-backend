def score_setup(htf_bias, ltf_bos, liquidity, zone_ok, session_ok, rr_ok):
    score = 0
    if htf_bias == ltf_bos:
        score += 2
    if liquidity:
        score += 2
    if ltf_bos:
        score += 2
    if zone_ok:
        score += 2
    if session_ok:
        score += 1
    if rr_ok:
        score += 1
    return score
