 
##  Overview

A basic automated trading system built with the ``ib_insync`` module that supports live, as well as paper trading via
[Interactive Brokers](https://www.interactivebrokers.com). 
- The main method can be found in ``trading_system/main.py``.
- Live ticker data is streamed from IBKR and summarized into a candlestick every $n$ seconds.
- The modular architecture allows to conveniently define different rule based algorithms, that make decisions based on the available price data.
- Algorithms can be defined in ``trading_system/algorithms``.
 
##  Requirements

- Python 3.9
- IB Trader Workstation Build 973.2
- IB paper or live trading account with an active market data subscription
- Telegram messenger app

Dependencies
├──ib-insync == 0.9.80 (https://github.com/erdewit/ib_insync)
├──plotly == 5.11.0 (https://github.com/plotly/plotly.py)
├──pandas == 1.5.2 (https://github.com/pandas-dev/pandas)
├──numpy == 1.23.5 (https://github.com/numpy/numpy)
├──pyTelegramBotAPI == 4.8.0 (https://github.com/eternnoir/pyTelegramBotAPI)
├──python-dateutil == 2.8.2 (https://github.com/dateutil/dateutil)
└──pytz == 2022.6 (https://github.com/stub42/pytz)

##  Setting up

1) Create a virtual environment at the base directory level:

```commandline
$ python -m venv venv
$ venv/Scripts/activate
```

2. Install all dependencies with the correct versions. The packages are listed in ``requirements.txt``:

```commandline
$ pip install -r requirements.txt
```

3. This project uses a telegram bot as notifcation system. 
	- Download the Telegram app (https://telegram.org) and create a new bot.
	- Copy the ``API_KEY`` and ``receiver_id`` into the ``trading_system/parameters/config_telegram.py`` file.

4. Log in to IB Trader Workstation.

5. Finally, run the program from any directory:

```commandline
$ python path_to_main/main.py
```
