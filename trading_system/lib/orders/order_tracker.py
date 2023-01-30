import datetime


class OrderTracker:

    def __init__(self):
        self._orders = []

    def add_order(self, order_IBKR):
        self._orders.append({
            'time': datetime.datetime.now(),
            'price': order_IBKR.lmtPrice,
            'order_id': order_IBKR.orderId            
        })

    def get_orders(self):
        return self._orders


class BuyOrderTracker(OrderTracker):

    def __init__(self):
        self._buys = []
        super().__init__()

    def add_buy(self, trade):
        self._buys.append({
            'time': datetime.datetime.now(),
            'price': trade.order.lmtPrice      
        })

    def get_buys(self):
        return self._buys


class ShortOrderTracker(OrderTracker):

    def __init__(self):
        self._short_sells = []
        super().__init__()

    def add_short(self, trade):
        self._short_sells.append({
            'time': datetime.datetime.now(),
            'price': trade.order.lmtPrice         
        })

    def get_short_sells(self):
        return self._short_sells


class SellOrderTracker(OrderTracker):

    def __init__(self):
        self._sells = []
        self._submitted = False
        super().__init__()

    def add_sell(self, trade):
        self._orders.append({
            'time': datetime.datetime.now(),
            'price': trade.order.lmtPrice    
        })
    
    def add_order(self, order_IBKR):
        super().add_order(order_IBKR)
        self._submitted = True        

    def get_sells(self):
        return self._sells
        
    def get_submitted(self):
        return self._submitted