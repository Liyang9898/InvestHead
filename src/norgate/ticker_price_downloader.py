from datetime import datetime
import norgatedata
from util.util_time import df_filter_dy_date


def func(t):
    str_datetime = str(t)
    datetime_obj = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    unix_ts = datetime.timestamp(datetime_obj)
    return unix_ts


def pull_ticker_price_locally_norgate(ticker, start_date, end_date, path_out):
    """
    norgate data updator needs to be run to get latest data locally
    then norgate python API pull data from it
    input: ticker in upper case
    output: dataframe, cols=unixtime    Open    High    Low    Close    ma200    ma50    ema21    ema8
    """
    ticker = ticker.upper()
    output_cols =['unixtime','Open','High','Low','Close','ma200','ma50','ema21','ema8']
    timeseriesformat = 'pandas-dataframe'
    priceadjust = norgatedata.StockPriceAdjustmentType.TOTALRETURN
    padding_setting = norgatedata.PaddingType.NONE
    
    # call norgate api
    stock_df = norgatedata.price_timeseries(
        ticker,
        stock_price_adjustment_setting = priceadjust,
        padding_setting = padding_setting,
        timeseriesformat = timeseriesformat,
    )
    
    stock_df.reset_index(inplace=True)
    
    # filter date
    stock_df = stock_df.sort_values(by='Date', ascending=True)
    stock_df['date_str'] = stock_df['Date'].astype(str)
    stock_df = df_filter_dy_date(stock_df, 'date_str', start_date, end_date)
    
    # add basic indicator
    if(len(stock_df)==0):
        return stock_df

    stock_df['unixtime']=stock_df.apply(lambda row : func(row['Date']), axis = 1)
    stock_df['ma200'] = stock_df['Close'].rolling(window=200).mean()
    stock_df['ma50'] = stock_df['Close'].rolling(window=50).mean()
    stock_df['ema21'] = stock_df['Close'].ewm(span=21,min_periods=0,adjust=False,ignore_na=False).mean()
    stock_df['ema8'] = stock_df['Close'].ewm(span=8,min_periods=0,adjust=False,ignore_na=False).mean()
    
    # save to csv
    stock_df = stock_df[output_cols].copy()
    stock_df.to_csv(path_out, index=False)

    

    
