import csv
from datetime import datetime  # string to datetime object conversion
import pandas as pd
import yfinance as yf



def download_stock_volume(ticker, start, end):
    stock_df = yf.download(ticker, start, end)
    stock_df.reset_index(level=0, inplace=True)
    cnt = len(stock_df)
    vol_avg = stock_df['Volume'].sum() / cnt
    return {
        'ticker':ticker,
        'vol':str(vol_avg)
    }

def download_stock(ticker, start, end, interval):
#     yf.download(symbol,threads= False,start=max_hist,end=today)
    stock_df = yf.download(tickers=ticker, start=start, end=end, interval=interval)
    stock_df.reset_index(level=0, inplace=True)
    stock_df.dropna(inplace=True)
    if(len(stock_df)==0):
        return stock_df
    
    stock_df['unixtime']=stock_df.apply(lambda row : func(row['Date']), axis = 1)
    stock_df['ma200'] = stock_df['Close'].rolling(window=200).mean()
    stock_df['ma50'] = stock_df['Close'].rolling(window=50).mean()
    stock_df['ema21'] = stock_df['Close'].ewm(span=21,min_periods=0,adjust=False,ignore_na=False).mean()
    stock_df['ema8'] = stock_df['Close'].ewm(span=8,min_periods=0,adjust=False,ignore_na=False).mean()
    return stock_df

def func(t):
    str_datetime = str(t)
    datetime_obj = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    unix_ts = datetime.timestamp(datetime_obj)
    return unix_ts

def download_format_2csv(ticker, start, end, path_out, interval):
    stock_df =  download_stock(ticker, start, end, interval)
#     print(stock_df['ma50'])
    if len(stock_df) == 0:
        print('done')
        return
    stock_df.to_csv(path_out, columns =['unixtime','Open','High','Low','Close','ma200','ma50','ema21','ema8'], index=False)
    print('done')


def batch_download_stock(list_tickers, start_time, end_time, folder, interval):
    cnt = 1
    for ticker in list_tickers:
        if cnt > 0:
            print('')
            print('No:' + str(cnt) + ' start processing:'+ticker)
            path_out = folder + """{ticker}_downloaded_raw.csv""".format(ticker=ticker)
            download_format_2csv(ticker, start_time, end_time, path_out, interval)
            print('No:' + str(cnt) + ' finish processing:'+ticker)
            print('')
        cnt = cnt + 1
