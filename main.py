from structure import detect_market_structure

def run_bot():
    send_telegram("🟢 XAUUSD STRUCTURE BOT LIVE (H1 → M15)")

    while True:
        try:
            candles_htf = get_market_data("XAUUSD", "1H")

            structure = detect_market_structure(candles_htf)

            if structure and structure["bias"] != "Range":
                message = f"""
📊 XAUUSD MARKET STRUCTURE

Bias: {structure['bias']}
Event: {structure['BOS']}
TF: 1H
"""
                send_telegram(message)

            time.sleep(900)  # 15 minutes

        except Exception as e:
            print("Error:", e)
            time.sleep(60)

