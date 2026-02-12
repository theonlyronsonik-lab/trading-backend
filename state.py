# state.py

class BotState:
    def __init__(self):
        self.direction = None
        self.range_low = None
        self.range_high = None
        self.supply_zone = None
        self.demand_zone = None
        self.trade_taken = False
        self.waiting_for_htf_retest = False
        self.waiting_for_choch = False
        self.choch_level = None
        self.last_bos_time = None
