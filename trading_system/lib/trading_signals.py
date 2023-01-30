
import datetime

class TradingSignals:

    def __init__(self):
        self.up_spikes = []
        self.significant_price_drops = []

    def add_spike(self, price, is_small):
        self.up_spikes.append({
            'time': datetime.datetime.now(),
            'price': price,
            'is_small': is_small,           
            'resolved': False
        })

    def resolve_current_spike(self):
        if(len(self.up_spikes) == 0):
            return
        self.up_spikes[-1]['resolved'] = True

    def add_dip(self, price):
        self.significant_price_drops.append({
            'time': datetime.datetime.now(),
            'price': price         
        })