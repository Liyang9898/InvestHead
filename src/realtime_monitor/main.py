'''
Created on Jan 1, 2021

@author: leon
'''
from download_stock.download_stock_lib import batch_download_stock
from datetime import datetime, timedelta
from batch_20201214.format_lib.lib import batch_format
from batch_20201214.indicator_lib.lib import batch_indicator
from realtime_monitor.batch_entry_exit.lib import batch_entries
# download stock 50+20
#process time
end_time_dt = datetime.today()
gap = (50+20) * 2
start_time_dt = end_time_dt - timedelta(days=gap)

print('date_time_dt:', start_time_dt,'-------', end_time_dt)
end_time=end_time_dt.strftime('%Y-%m-%d')
start_time=start_time_dt.strftime('%Y-%m-%d')
print('date_time:', start_time,'-------', end_time)

    
ticker_list = ['AMZN','FB']

folder = """D:/f_data/reatime_monitor/raw_stock_data/"""
batch_download_stock(ticker_list, start_time, end_time, folder)

# format
print('format')
folder_path_raw_downloaded = """D:/f_data/reatime_monitor/raw_stock_data/"""
folder_path_raw_price_formated = "D:/f_data/reatime_monitor/stock_formated/"
batch_format(folder_path_raw_downloaded, folder_path_raw_price_formated)

# add indicator
print('add indicator')
folder_path_price_with_indicator = "D:/f_data/reatime_monitor/stock_indicator/"
batch_indicator(folder_path_price_with_indicator, folder_path_raw_price_formated)

# test entry or exit
print('scan entry')
folder_path_price_with_entry = "D:/f_data/reatime_monitor/stock_entry/"
ma = "21_50"
strategy_param_bundle={
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
}
res =  batch_entries(ma,strategy_param_bundle, folder_path_price_with_indicator,folder_path_price_with_entry)
# for ticker, val in res.items():
#     print(ticker)
#     for x in val:
#         print(x['entry_ts'], x['entry_price'])
# mark

# list today's entry