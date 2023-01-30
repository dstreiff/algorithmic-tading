import telebot
import pandas as pd
import os 
import parameters.config_telegram as config
import parameters.config_tradingbot as parameters
import datetime 
import logging

logger = logging.getLogger(__name__)

class TelegramBot():

    bot = None
    notification_id = 0
    path_to_notifications = os.path.join(parameters.base_directory,
        'trading_system','lib','telegram','notifications.txt')


    @classmethod
    def start(cls):
        cls.bot = telebot.TeleBot(config.API_KEY)
        logging.info("Telegram Bot started.")


    @classmethod
    def notify(cls,symbol,reason):

        telegram_dict = {'id': [cls.notification_id], 
            'symbol': [str(symbol)],
            'time': [str(datetime.datetime.now())],
            'reason': [str(reason)]}
        telegram_dataframe = pd.DataFrame(data=telegram_dict)
        telegram_dataframe.to_csv(cls.path_to_notifications,
            index=False, mode='a', header=False)
        cls.notification_id+=1
        
        cls.bot.send_message(config.receiver_id, "Symbol: " 
            + str(symbol) + "\nTime: " + str(datetime.datetime.now()) 
            + "\nReason for the alert: "  + str(reason))


    






