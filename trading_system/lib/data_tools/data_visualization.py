import logging
import plotly.graph_objects as go
import os 
from parameters.config_tradingbot import base_directory, today

logger = logging.getLogger(__name__)

def plot_data(contract):
    logging.info('Creating the figure')

    try:
        fig_bars = go.Figure(data=[go.Candlestick(x=contract.bars['date'],
                    open=contract.bars['open'],
                    high=contract.bars['high'],
                    low=contract.bars['low'],
                    close=contract.bars['close'])])
        # fig_buyorder = go.Figure(data=go.Scatter(x=contract.buyorders.orders['time'],
        #             y=contract.buyorders.orders['price'],name="Buy orders"))
        # fig_shortorder = go.Figure(data=go.Scatter(x=contract.shortorders.orders['time'],
        #             y=contract.shortorders.orders['price'],name="Short orders")) 
        # fig_sellorder = go.Figure(data=go.Scatter(x=contract.sellorders.orders['time'],
        #             y=contract.sellorders.orders['price'],name="Sell orders",mode='markers')) 
        # fig_spike = go.Figure(data=go.Scatter(x=contract.patterns.spikes['time'],
        #             y=contract.patterns.spikes['price'],name="Spike encountered",mode='markers')) 
        # fig_spikeO = go.Figure(data=go.Scatter(x=contract.patterns.spike_resolved['time'],
        #             y=contract.patterns.spike_resolved['price'],name="Spike over",mode='markers'))
        # fig_dip = go.Figure(data=go.Scatter(x=contract.patterns.massive_dip['time'],
        #             y=contract.patterns.massive_dip['price'],name="massive dip",mode='markers'))
        # fig_NaN = go.Figure(data=go.Scatter(x=contract.patterns.nan_tick['time'],
        #                     y=contract.patterns.nan_tick['price'],name="NaN or -1",mode='markers')) 
        fig_all = go.Figure(data = fig_bars.data)#+ fig_buyorder + fig_shortorder.data +
                        # fig_sellorder.data + fig_spike.data + fig_spikeO.data + fig_dip)
        
        folder = os.path.join(base_directory,"images", today)
        try:
            fig_all.write_html(os.path.join(folder, contract.symbol +".html"))
        except Exception as e:
            logging.info(e)            
            os.mkdir(folder)
            logging.info("Created a new folder")
            fig_all.write_html(os.path.join(folder, contract.symbol +".html"))
    except Exception as e:
        logging.info("Could not create the figure.")
        logging.info(e)