from lib.telegram.telegram_bot import TelegramBot
import logging

logger = logging.getLogger(__name__)


class ExitHandler:

    def __init__(self,ib):
        self.ib = ib

    def at_exit(self):
        try:
            TelegramBot.notify('No symbol','Application ending')
        except Exception as e:
            pass

        try:
            self.cancel_all_orders()
            self.ib.disconnect()
        except Exception as e:
            pass


    def cancel_all_orders(self):
        for i in range(5):
            orders = self.ib.openOrders()
            self.ib.sleep(0.01)
            for order in orders:
                self.ib.cancelOrder(order)
                self.ib.sleep(0.05)    
            self.ib.sleep(0.2)
            if(len(self.ib.openOrders()) == 0):
                return
        try:
            logging.info('Not all orders were cancelled.') 
            TelegramBot.notify('No symbol','Not all orders were cancelled.')
        except Exception as e:
            pass        
            