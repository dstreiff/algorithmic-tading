from lib.telegram.telegram_bot import TelegramBot
import logging

logger = logging.getLogger(__name__)


class ExitHandler:

    def __init__(self,ib):
        self.ib = ib

    def at_exit(self):
        try:
            self.cancel_all_orders()
        except Exception as e:
            logging.error("Error cancelling orders:", e)

        try:
            TelegramBot.notify('No symbol', 'Application ending')
        except AttributeError as e:
            logger.error("AttributeError while notifying: %s", e)
        except ConnectionError as e:
            logger.error("ConnectionError while notifying: %s", e)

        try:
            self.ib.disconnect()
        except Exception as e:
            logger.error("Error while disconnecting from IB: %s", e)


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
            TelegramBot.notify('No symbol', 'Not all orders were cancelled.')
        except AttributeError as e:
            logger.error("AttributeError while notifying: %s", e)
        except ConnectionError as e:
            logger.error("ConnectionError while notifying: %s", e)      
            