from ib_insync import util
import logging
import parameters.config_tradingbot as config
import datetime
import pandas as pd
import math
import os

logger = logging.getLogger(__name__)


class DataProcessing():

    def __init__(self):
        self.tickers = []
        self.ticker_data = {}


    def request_historical_data(self, ib, contract, look_back):
        try:
            bars = ib.reqHistoricalData(
                contract,
                endDateTime = '',
                durationStr = look_back,
                barSizeSetting = '30 secs', 
                whatToShow = 'TRADES',
                useRTH = False,
                formatDate = 1,
                keepUpToDate = False)
        except ValueError as error: 
            logger.error(error)
        try:
            bars[0]
        except:     
            logger.error('Requesting historical data failed')
            return None
        data = util.df(bars)
        data = data.drop(data[data.barCount == 0].index) 
        return data


    def read_csv_data(self, contract):
        try:
            file_name = config.base_directory + "/historical_data/" + contract.symbol + ".txt"
            bars = pd.read_csv(file_name)
            for j in range(len(bars['open'])):
                bars['date'].iloc[j] = datetime.datetime.fromisoformat(bars['date'].iloc[j])
            logger.info(bars.iloc[0])
            logger.info(bars.iloc[-1])
        except ValueError as error: 
            logger.error(error)
        try:
            bars['open'][0]
        except:     
            logger.error('Requesting historical data failed')
            return None
        bars = bars.drop(bars[bars.barCount == 0].index) 
        return bars 


    def on_pending_tickers(self, tickers):
        for t in tickers:
            self.ticker_data[t.contract.symbol].loc[t.time] = [t.last, t.bid,t.ask]


    def make_candle(self,contract):
        symbol = contract.symbol
        contract.new_candle = False

        now = datetime.datetime.now(datetime.timezone.utc)
        recent_data = self.ticker_data[symbol].loc[
            (now - config.refresh_interval_inseconds):]
        # TODO: To reduce memory consumption, remove the previous entries in ticker_data
        logging.info(recent_data)
        logging.info(self.ticker_data)

     
        if(recent_data.empty):
            return    
                    
        open = recent_data['last'].iloc[0]
        close = recent_data['last'].iloc[-1]
        high = recent_data['last'].max()
        low = recent_data['last'].min()
        if(math.isnan(open) or open == -1.0 or
            math.isnan(close) or close == -1.0 or
            math.isnan(high) or high == -1.0 or
            math.isnan(low) or low == -1.0):

            logging.info('nan or -1 ' + str(symbol) + ' ' +str(recent_data['last'].iloc[0]) 
            + " " + str(recent_data['last'].max()) + " " + str(recent_data['last'].min()))
            return

        df2dict = {'date': [ datetime.datetime.now()],
                'open':[open],
                'high':[high],
                'low':[low],
                'close':[close],
                'volume':[recent_data['lastbid'].iloc[-1]],
                'average':[(high+low)/2],
                'barCount':[recent_data['lastask'].iloc[-1]]
            }

        df2 = pd.DataFrame(df2dict)

        bars = pd.concat([contract.bars, df2], ignore_index = True)
        bars.reset_index()

        contract.new_candle = True

        return


    def add_empty_dataframe(self,symbol):
        self.ticker_data[symbol] = pd.DataFrame({'last':[],'lastbid':[],'lastask':[]})


    def save_to_csv(self,contracts):
        for contract in contracts.values():
            folder = os.path.join(config.base_directory, "historical_data", contract.symbol)
            try:
                contract.bars.to_csv(folder+"/"+config.today+".csv",index=False)
            except Exception as e:
                os.mkdir(folder)
                contract.bars.to_csv(folder+"/"+config.today+".csv",index=False)