# from download_stock.all_ticker import get_all_ticker_list
from batch_20201214.download_stock.download_stock_lib import download_format_2csv, \
    download_stock_volume,batch_download_stock
import pandas as pd

from batch_20201214.ticker.util import get_ticker_list

ticker_path="D:/f_data/sweep_20201214/all_ticker_meta/ticker_raw/ticker_all_20210106.csv"
output_folder = """D:/f_data/sweep_20201214/raw_stock_download_20210106/"""

list_tickers = get_ticker_list(ticker_path)
print(list_tickers)
# list_tickers = ['V']
# download stock data

start_time="2016-01-01"
end_time="2021-01-07"
batch_download_stock(list_tickers, start_time, end_time,output_folder)


#----------------------------------------------------------------------------

# # following code get volume of all stock
# def get_all_vol():
#     res = {}
#     cnt = 1
#     for ticker in list_tickers:   
#         cnt = cnt + 1
# 
#         print(cnt, ticker)
#         v = download_stock_volume(ticker, "2020-01-01", "2020-12-31")
#         res[v['ticker']]=v['vol']
#         
#     return res
# 
# res = get_all_vol()
# df = pd.DataFrame(res.items(), columns=['ticker', 'vol'])
# path_out = """D:/f_data/sweep_20201214/volume_all_ticker.csv"""
# df.to_csv(path_out, columns =['ticker', 'vol'], index=False)
# print(df)