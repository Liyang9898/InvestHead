from datetime import datetime, timedelta
import os
import shutil

from batch_20201214.download_stock.download_stock_lib import batch_download_stock
from batch_20201214.format_lib.lib import batch_format
from batch_20201214.indicator_lib.lib import batch_indicator
import pandas as pd
from price_asset_master.lib.refresh_price_asset_add_indicator import refresh_price_asset_add_indicator
from version_master.version import (
    swing_set1,
    op_path_base,
)


def refresh_price_asset(time_window, set_list):
    # params
    period = time_window # days, not trading days
    
    # process ticker list
    print('processing: ticker list')
    df = pd.read_csv(set_list)
    ticker_list = df['ticker'].to_list()
    ticker_list = ticker_list + ['BTC-USD']
#     ticker_list.remove('ZS')
#     ticker_list = ['BTC-USD']
    # ticker_list=ticker_list[0:5]
    # ticker_list = ['FTNT','TPX','CARE']
    print(ticker_list)
#     ticker_list = ['AZPN','ENTG','INTU','MORN','MTCH','PTC','SQ','CG','ETSY','MSFT']


    refresh_price_asset_add_indicator(time_window, ticker_list, op_path_base, interval='1d')
