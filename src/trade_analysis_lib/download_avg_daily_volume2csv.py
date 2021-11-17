'''
Created on Jun 9, 2020

@author: leon
'''

from download_stock.download_yfinance_daily_stock_data import download_stock_volume
import pandas as pd
from util import util

stock_ticker_folder="""D:/f_data/download_yfinance_with_indicator/"""
filepath_list=util.get_all_csv_file_path_from_folder(stock_ticker_folder)

cnt=1
res = {}
for file in filepath_list.keys():
    ticker=util.extract_symbol_name(file)
    print(str(cnt) + " processing: "+ticker+"   "+file)
    cnt = cnt + 1
    avg_daily_vol = download_stock_volume(ticker, "2020-01-15", "2020-03-15")
    res[avg_daily_vol['ticker']]=avg_daily_vol['vol']


df = pd.DataFrame(res.items(), columns=['ticker', 'vol'])
path_out = """D:/f_data/volume_all_ticker.csv"""
df.to_csv(path_out, columns =['ticker', 'vol'], index=False)
