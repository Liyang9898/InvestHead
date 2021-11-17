from price_asset_master.lib.refresh_price_asset import refresh_price_asset
from price_asset_master.lib.refresh_price_asset_add_indicator import refresh_price_asset_add_indicator
from price_asset_master.lib.util import csv_to_ticker_list
from version_master.version import swing_set1


swing_set1_ticket_list = csv_to_ticker_list(swing_set1)

# this function get price until today for the ticket in set_list. 
# Price will be kept in the a folder with today's date
ticker_list = [
    'iwf', 
    'BTC-USD' ,
    'SPY', 
    'JLGMX',
    'JMGMX',
    'JGSMX',
    'JSDRX',
    'xlk', 
    'xlf', 
    'fb', 
    'amzn', 
    'goog'
]
time_window=365*5
# ticker_list = ['spy', 'iwf', 'xlk', 'xlf', 'fb', 'amzn', 'goog']

op_path_base = 'D:/f_data/operation_test/'
interval = '1d'
# interval = '1wk'

path_base = refresh_price_asset_add_indicator(time_window, ticker_list, op_path_base, interval)


# JLGMX:JPMorgan Large Cap Growth Fund Class R6 
# JMGMX:JPMorgan Mid Cap Growth Fund
# JGSMX:JPMorgan Small Cap Growth Fund
# JGVVX:JPMorgan Growth Advantage Fund
# JSDRX:JPMorgan Short Duration Core Plus Fund