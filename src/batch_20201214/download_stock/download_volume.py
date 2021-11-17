'''
Created on Jan 8, 2021

@author: leon
'''
from batch_20201214.download_stock.download_stock_lib import download_stock_volume
import pandas as pd

from batch_20201214.ticker.util import get_ticker_list

ticker_path="D:/f_data/sweep_20201214/all_ticker_meta/ticker_raw/ticker_all_20210106.csv"


list_tickers = get_ticker_list(ticker_path)
print(list_tickers)


def get_all_vol():
    res = {}
    cnt = 1
    for ticker in list_tickers:   
        cnt = cnt + 1
 
        print(cnt, ticker)
        v = download_stock_volume(ticker, "2020-01-01", "2020-12-31")
        res[v['ticker']]=v['vol']
         
    return res
 
res = get_all_vol()
df = pd.DataFrame(res.items(), columns=['ticker', 'vol'])
path_out = """D:/f_data/sweep_20201214/all_ticker_meta/volume_all_ticker_20210108.csv"""
df.to_csv(path_out, columns =['ticker', 'vol'], index=False)
print(df)