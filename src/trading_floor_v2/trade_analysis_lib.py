'''
Created on Mar 1, 2023

@author: spark
'''

from util.util_pandas import df_general_time_filter, \
    connect_a_list_of_time_series_df


def gen_ts_with_trades(df_price, df_trades, date_col, ts_col, initial_aum):
    '''
    This function draw the time series of portfolio according to the trades
    '''
    ts_list = []
    
    # get time series for each trade
    for i in range(0, len(df_trades)):
        s = df_trades.loc[i, 'ts_enter']
        e = df_trades.loc[i, 'ts_exit']
        ts = df_general_time_filter(df_price, date_col, s, e)
        ts_list.append(ts)
    
    # connect all time series
    ts_all = connect_a_list_of_time_series_df(ts_list, date_col, ts_col, initial_aum)
    ts_all = ts_all[[date_col, ts_col]]
    ts_all = ts_all.copy()
    
    return ts_all


