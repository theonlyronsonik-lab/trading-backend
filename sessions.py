from datetime import datetime, timezone

def in_trading_session():
    """
    London: 07–11 UTC
    New York: 12–16 UTC
    """
    now = datetime.now(timezone.utc).hour

    london = 7 <= now <= 11
    new_york = 12 <= now <= 16

    return london or new_york
