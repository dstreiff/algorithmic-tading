
import datetime
import time
import os
import atexit
import logging
from ib_insync import IB

import parameters.config_tradingbot as config
from lib import contracts
from lib import DataProcessing
from lib import TelegramBot
from lib import plot_data
from lib import BuyOrderTracker, SellOrderTracker, ShortOrderTracker
from lib.exit_handler import ExitHandler
from lib.trading_signals import TradingSignals
from algorithms.buy_algorithms import buy_algorithm1_realTime
from algorithms.sell_algorithms import sell_algorithm1_realTime


def create_the_logFile():
    logging.basicConfig(
        filename=os.path.join(config.base_directory,"event_log.log"), 
        level=logging.INFO)
    logging.info('Script started.')


def connect_to_IBKR():
    # First open IB Gateway or TWS
    ib = IB()
    ib.disconnect()
    ib.connect('127.0.0.1', config.ibkr_port, clientId= config.client_id)
    for order in ib.openOrders():
        ib.cancelOrder(order)
        ib.sleep(0.001)
    ib.sleep(0.1)
    if(len(ib.openOrders()) != 0):
        logging.info('Not all orders got cancelled.')
        raise SystemExit(0)
    return ib


def initialize_tickers_and_contracts(data_proc, ib):
    # There are two type of contracts in this program:
    # The first one is defined in trading_system.lib.contracts.
    # The second one is programmed by ib_insync and in this program
    # referenced as "contract_IBKR".
    
    all_contracts = {}

    # Instantiate empty data structures
    order_history = {'buy':  BuyOrderTracker(),
                     'sell': SellOrderTracker(),
                     'short':ShortOrderTracker()}
    trading_signals = TradingSignals()

    for symbol in config.symbols:
        all_contracts[symbol] = contracts.Stock(symbol, order_history,trading_signals, data_proc)
        if(symbol != all_contracts[symbol].symbol):
            raise SystemExit(0)

        # Qualifying the IBKR contract
        ib.qualifyContracts(all_contracts[symbol].contract_IBKR)
        
        # Creating the tickers
        data_proc.tickers.append(ib.ticker(all_contracts[symbol]))
        data_proc.add_empty_dataframe(symbol) 

    ib.sleep(5)
    ib.pendingTickersEvent += data_proc.on_pending_tickers
    
    return all_contracts


def every_n_seconds(ib, contracts, data_proc):
    timer_start = time.time()
    now = datetime.datetime.now()
    logging.info(str(now))

    if(now > config.exit_time):
        data_proc.save_to_csv(contracts)
        ib.pendingTickersEvent -= data_proc.on_pending_tickers
        for contract in contracts:
            ib.cancelMktData(contract)
        raise SystemExit(0)
  
    for symbol in contracts:
        logging.info(symbol)
        contract = contracts[symbol]

        data_proc.make_candle(contract)
        # logging.info(contract.bars)

        if(not contract.bought):
            buy_algorithm1_realTime(contracts[symbol],ib)
        else:
            positions = ib.positions()
            number_of_shares = 0
            for k in range(len(positions)): 
                if(symbol == positions[k].contract.symbol):
                    number_of_shares += positions[k].position
            if(number_of_shares <= 0):
                logging.info('numberofshares <= 0')
                raise SystemExit(0)
            contract.sellorders.submitted = sell_algorithm1_realTime(contract,number_of_shares,ib)

        # To separate the heavy computation of plotting the data from the main trading process, 
        # a better solution would be to use a task queue such as Celery or RabbitMQ to handle 
        # the plotting task asynchronously. This way, the trading bot can add the plotting task 
        # to the queue, and the task will be executed by a separate worker process without blocking 
        # the main trading process.
        if(len(contract.bars.index) % 60 == 1):
            plot_data(contract)

    iteration_duration = time.time()-timer_start 
    if(iteration_duration > config.refresh_interval - 0.001):
        logging.info('Iteration took too long.')
        TelegramBot.notify("No symbol","Iteration took " + str(iteration_duration) + " seconds.") 
        raise SystemExit(0)                   
    logging.info("The iteration took " + str(iteration_duration) + " seconds.")
    

def run_the_trading_system():

    # Setup:
    create_the_logFile()
    ib = connect_to_IBKR()
    atexit.register(ExitHandler(ib).at_exit)
    TelegramBot.start()

    # Instantiate the DataProcessing object
    data_proc = DataProcessing()

    # Initializing the contracts and the data stream:
    all_contracts  = initialize_tickers_and_contracts(data_proc, ib)

    initial_time = datetime.datetime.now()
    iteration = 1
    while(iteration < 2400):
        logging.info('Iteration: ' + str(iteration))
        every_n_seconds(ib, all_contracts, data_proc)

        ib.waitUntil(initial_time + config.refresh_interval_inseconds*iteration)
        iteration += 1
    
    
if __name__ == "__main__":
    run_the_trading_system()