from datetime import datetime, timedelta
import os
import shutil

from batch_20201214.download_stock.download_stock_lib import batch_download_stock
from batch_20201214.format_lib.lib import batch_format
from batch_20201214.indicator_lib.lib import batch_indicator
import pandas as pd


def refresh_price_asset_add_indicator(time_window, ticker_list, op_path_base, interval="1d"):
#     interval= 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

    # params
    period = time_window # days, not trading days
    
    # process ticker list
    print('processing: ticker list')
    print(ticker_list)

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
    path_base = op_path_base  + now_str
    op_path_raw_stock = path_base + '/raw/'
    op_path_format = path_base + '/format/'
    op_path_indicator = path_base + '/indicator/'
    # 
    if not os.path.exists(op_path_base):
        os.mkdir(op_path_base) 
    if os.path.exists(path_base):
        shutil.rmtree(path_base)
    print('making folder:', op_path_base)
    os.mkdir(path_base) 
    os.mkdir(op_path_raw_stock) 
    os.mkdir(op_path_format) 
    os.mkdir(op_path_indicator) 
    print('making folder complete')
      
    # download stock data
    print('processing: download')
    print(datetime.today())
    print(op_path_raw_stock)
    batch_download_stock(ticker_list, start_date, end_date, op_path_raw_stock, interval)
      
      
    # format
    print('processing: format')
    print(datetime.today())
    batch_format(op_path_raw_stock, op_path_format)
    print(datetime.today())
     
     
    # indicator
    print('processing: indicator')
    print(datetime.today())    
    batch_indicator(
        op_path_indicator, 
        op_path_format, 
        start_date, 
        end_date,
        ticker_list
    )
    print(datetime.today())   
    
    return path_base