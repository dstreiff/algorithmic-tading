import datetime
import os


base_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

today = datetime.datetime.now().date().isoformat()
ten_am = datetime.datetime.now().replace(hour=10, minute=00, second=0, microsecond=0)
market_open_time = datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
market_open_time_timeZoneAware = datetime.datetime.now(datetime.timezone.utc).replace(
    hour=15, minute=30, second=00, microsecond=0) - datetime.timedelta(seconds = 7200)
market_close_time = datetime.datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
exit_time = market_close_time + datetime.timedelta(seconds = 3600 * 4)

long_duration = '86400 S' # last 24 hours
short_duration = '301 S'    # larger than 5*60 seconds

client_id = 1
ibkr_port = 7497

# Symbols that I am trading
symbols =  ['AAPL','MSFT']

# Allocated money in usd for each stock
allocation_of_funds = {'TSLA':1000*1000.,
                'AAPL':1000*1000.,
                'MSFT':1000*1000.}

refresh_interval = 30
refresh_interval_inseconds = datetime.timedelta(seconds = refresh_interval)