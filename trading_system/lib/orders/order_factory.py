from lib.orders.order_handler import BuyOrderHandler, SellOrderHandler, ShortOrderHandler


class OrderFactory:
    
    @staticmethod
    def create_orderhandler(order_type,contract,ib):
        if order_type == 'buy':
            return BuyOrderHandler(contract,ib)
        elif order_type == 'sell':
            return SellOrderHandler(contract,ib)
        elif order_type == 'short':
            return ShortOrderHandler(contract,ib)
        else:
            raise ValueError('Invalid order type')

