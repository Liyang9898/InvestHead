import csv
from datetime import datetime  # string to datetime object conversion
import pandas as pd
import yfinance as yf

op_path_base = 'D:/f_data/temp/spywk.csv'
stock_df = yf.download(tickers='spy', start='2019-01-01', end='2022-01-01', interval='1wk')
stock_df.dropna(inplace=True)
print(stock_df['Close'])
stock_df.to_csv(op_path_base)
stock_df['ma50'] = stock_df['Close'].rolling(window=50).mean()
print(stock_df['ma50'])
# 
# def download_stock(ticker, start, end, interval):
# #     yf.download(symbol,threads= False,start=max_hist,end=today)
#     stock_df = yf.download(tickers=ticker, start=start, end=end, interval=interval)
# #     print(stock_df)
#     stock_df.reset_index(level=0, inplace=True)
#     
#     if(len(stock_df)==0):
#         return stock_df
#     
#     stock_df['unixtime']=stock_df.apply(lambda row : func(row['Date']), axis = 1)
#     stock_df['ma200'] = stock_df['Close'].rolling(window=200).mean()
# #     print(stock_df['Close'].to_list())
#     stock_df['ma50'] = stock_df['Close'].rolling(window=50).mean()
# #     print(stock_df)
# #     stock_df['xxx'] = stock_df['Close'].rolling(window=50).mean()
# #     print('Close',stock_df['Close'].to_list())
# #     print('xxx',stock_df['xxx'].to_list())
#     stock_df['ema21'] = stock_df['Close'].ewm(span=21,min_periods=0,adjust=False,ignore_na=False).mean()
#     stock_df['ema8'] = stock_df['Close'].ewm(span=8,min_periods=0,adjust=False,ignore_na=False).mean()
#     return stock_df
