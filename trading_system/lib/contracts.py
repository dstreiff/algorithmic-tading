import ib_insync


class Stock:

    def __init__(self, symbol, order_tracker, trading_signals, data_proc):

        # Initialize an IBKR contract and set the symbol
        self.symbol = symbol
        self.contract_IBKR = ib_insync.Stock(symbol,'SMART','USD')

        # Obtain the historical data
        # self.all_Bars = data_processing.request_historical_data(ib,self.contract_IBKR,long_duration)
        self.bars = data_proc.read_csv_data(self.contract_IBKR)

        # Initializing various instance variables
        self.bought = False
        self.new_candle = True # The buy algorithm is only executed, if there is a new candle 

        self.buyorders = order_tracker['buy']
        self.sellorders = order_tracker['sell']
        self.trading_signals = trading_signals
 

class StockWithShortOption(Stock):
    def __init__(self, symbol, order_tracker, trading_signals, data_proc):
        super().__init__(symbol, order_tracker, trading_signals, data_proc)
        self.shortorders = order_tracker['short']