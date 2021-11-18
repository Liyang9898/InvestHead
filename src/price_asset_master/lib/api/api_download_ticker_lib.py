import yfinance as yf
from datetime import datetime



    
    
def download_format_2csv(ticker, start, end, path_out, interval):
    stock_df =  download_stock(ticker, start, end, interval)
    if len(stock_df) == 0:
        return
    stock_df.to_csv(path_out, columns =['unixtime','Open','High','Low','Close','ma200','ma50','ema21','ema8'], index=False)
    

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