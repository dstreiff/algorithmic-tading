import logging
from ib_insync import LimitOrder
from lib.telegram.telegram_bot import TelegramBot
from parameters.config_tradingbot import allocation_of_funds, ten_am
import math

logger = logging.getLogger(__name__)


class OrderHandler:

    def __init__(self, contract, ib):
        self.contract = contract
        self.ib = ib
        self.order_IBKR = None

    def _place_order(self, order_type, number_of_shares, limit_price):
        self.order_IBKR = LimitOrder(order_type, int(number_of_shares), limit_price)
        self.order_IBKR.outsideRth=True
        self.order_IBKR.tif='GTC'
        return self.ib.placeOrder(self.contract.contract_IBKR, self.order_IBKR)

    def cancel_order(self):
        if(self.order_IBKR == None):
            return
        self.ib.cancelOrder(self.order_IBKR)
        self.ib.sleep(0.001)

    def _order_filled(self, trade, order_type):
        logger.info(f'{order_type}-Order has been filled.')
        logger.info(trade.contract.symbol)
        logger.info(trade.order.lmtPrice)
        TelegramBot.notify(trade.contract.symbol, f'{order_type} at price: {trade.order.lmtPrice}')

    @classmethod
    def rounddown(cls, x, roundNumber):
        return int(int(math.floor(x / roundNumber)) * roundNumber)


class BuyOrderHandler(OrderHandler):

    def __init__(self, contract, ib):
        super().__init__(contract, ib)

    def calculate_number_of_shares(self, limit_price):
        symbol = self.contract.symbol
        allocation = allocation_of_funds[symbol]
        number_of_shares = int( allocation/float(limit_price) )
        if(number_of_shares >= 100):
            number_of_shares = OrderHandler.rounddown(number_of_shares, 100.0)
        elif(number_of_shares < 100 and number_of_shares >= 50):
            number_of_shares = 50
        return number_of_shares

    def place_order(self, limit_price):
        logging.info("Placing buy order")
        number_of_shares = self.calculate_number_of_shares(limit_price)
        if(number_of_shares == 0):
            logging.info('number_of_shares == 0')
            raise SystemExit(0)
        if(self.contract.bars.iloc[-1]['date'] >=  ten_am):
            trade = self._place_order('Buy', number_of_shares, limit_price)
            trade.fillEvent += self.buy_order_filled
            self.contract.buyorders.add_order(self.order_IBKR) 

    def buy_order_filled(self, trade, fill):
        self._order_filled(trade, 'Buy')      
        self.contract.buyorders.add_buy(trade)
        self.contract.bought = True


class SellOrderHandler(OrderHandler):

    def __init__(self, contract, ib):
       super().__init__(contract, ib)

    def place_order(self, limit_price, number_of_shares):
        logging.info("Placing sell order")
        trade = self._place_order('Sell', number_of_shares, limit_price)
        trade.fillEvent += self.sell_order_filled
        self.contract.sellorders.add_order(self.order_IBKR)

    def sell_order_filled(self, trade, fill):
        self._order_filled(trade, 'Sell')
        self.contract.sellorders.add_sell(trade)
        self.contract.bought = False


class ShortOrderHandler(OrderHandler):

    def __init__(self, contract, ib):
       super().__init__(contract, ib)

    def short_order_filled(self, trade, fill):
        self.contract.shortorders.add_short(trade)
        self.contract.bought = False
        self._order_filled(trade, 'Short')  