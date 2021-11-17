from datetime import datetime, timedelta
import os
import shutil

from batch_20201214.download_stock.download_stock_lib import batch_download_stock
from batch_20201214.format_lib.lib import batch_format
from batch_20201214.indicator_lib.lib import batch_indicator
import pandas as pd
from version_master.version import (
    swing_set1,
    price_asset_path_base,
)

def refresh_price_asset(time_window, ticker_list):
    # params
    period = time_window # days, not trading days
    
    # process ticker list
    print('processing: ticker list')
#     df = pd.read_csv(set_list)
#     ticker_list = df['ticker'].to_list()
#     ticker_list = ticker_list + addition_ticker
    # ticker_list=ticker_list[0:5]
    # ticker_list = ['FTNT','TPX','CARE']
    print(ticker_list)
#     ticker_list = ['AZPN','ENTG','INTU','MORN','MTCH','PTC','SQ','CG','ETSY','MSFT']

    
    # process time period
    print('processing: download')
    now = datetime.today()
    now_str = now.strftime('%Y-%m-%d')
    start_dt = now - timedelta(days=period)
    start_date = start_dt.strftime('%Y-%m-%d')
    end_dt = now + timedelta(days=1)
    end_date = end_dt.strftime('%Y-%m-%d')
    print('date:',start_date, end_date)
    
    # make folder
    path_base = price_asset_path_base  + now_str
    op_path_raw_stock = path_base + '/raw/'
    op_path_format = path_base + '/format/'

    # 
    if os.path.exists(path_base):
        shutil.rmtree(path_base)
    os.mkdir(path_base) 
    os.mkdir(op_path_raw_stock) 
    os.mkdir(op_path_format) 
#     os.mkdir(op_path_indicator) 
      
    # download stock data
    print('processing: download')
    print(datetime.today())
    print(op_path_raw_stock)
    batch_download_stock(ticker_list, start_date, end_date, op_path_raw_stock)
      
      
    # format
    print('processing: format')
    print(datetime.today())
    batch_format(op_path_raw_stock, op_path_format)
    print('stock price data path in:', op_path_format)
    print(datetime.today())
     
  