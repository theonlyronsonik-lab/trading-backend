from datetime import datetime

def get_session(timestamp):
    hour = int(timestamp.split(" ")[1].split(":")[0])

    if 0 <= hour < 7:
        return "ASIA"
    elif 7 <= hour < 15:
        return "LONDON"
    elif 15 <= hour < 22:
        return "NEW_YORK"
    else:
        return "OFF"

def session_valid(session):
    return session in ["LONDON", "NEW_YORK"]
