import pandas as pd
from datetime import datetime, timedelta

def previous_trading_day(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    date_time_obj = date_time_obj - timedelta(days=1)
    if date_time_obj.weekday() >= 5:
        date_time_obj = date_time_obj - timedelta(days=1)
      
    if date_time_obj.weekday() >= 5:
        date_time_obj = date_time_obj - timedelta(days=1)

    date_time_str = date_time_obj.strftime('%Y-%m-%d')
    return date_time_str

def trade_day_reformat(date_time_str):
    return date_time_str.split(' ')[0]

    
def join_trade_indicator_df(ticker, df_trades,df_indicator):

    df_trades['entry_date'] = df_trades.apply(lambda row : trade_day_reformat(row['entry_ts']), axis = 1)   
    df_trades['join_key']=df_trades['entry_date']

    df_indicator['previous_trading_day'] = df_indicator.apply(lambda row : previous_trading_day(row['date']), axis = 1)   
    df_indicator['join_key']=df_indicator['previous_trading_day']

    result = pd.merge(df_trades, df_indicator, how="left", on=["join_key"])
    del result['join_key']
    result['ticker'] = ticker
    assert len(df_trades) == len(result)
    return result

# def join_trade_indicator(ticker, df_trades, df_indicator):
# #     # get trade
# #     trade_path = trade_folder + 'detail/' + ticker + '_all_entry.csv'
# #     df_trades = pd.read_csv(trade_path)
# #     
# #     # get indicator
# #     indicator_path = indicator_folder + '/' + ticker + '_downloaded_raw.csv'
# #     df_indicator = pd.read_csv(indicator_path)
#     
#     # join
#     res = join_trade_indicator_df(df_trades,df_indicator)
#     return res
