'''
Created on Mar 1, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from trading_floor_v2.trade_infra_lib import STATUS_SHORT
from util.util_pandas import df_general_time_filter, \
    connect_a_list_of_time_series_df, reverse_ts_by_horizontal_line


def gen_ts_with_trades(df_price, df_trades, date_col, ts_col, initial_aum, start_end_only=False):
    '''
    This function draw the time series of portfolio according to the trades
    '''
    ts_list = []
    
    # get time series for each trade
    for i in range(0, len(df_trades)):
        s = df_trades.loc[i, 'ts_enter']
        e = df_trades.loc[i, 'ts_exit']
        ts_df = df_general_time_filter(df_price, date_col, s, e)
        trade_type = df_trades.loc[i, 'type']
        if trade_type == STATUS_SHORT:
            ts_df.reset_index(drop=True, inplace=True)
            pivot = ts_df.loc[0, ts_col]
            ts_df = reverse_ts_by_horizontal_line(ts_df, ts_col, pivot)
        
        ts_list.append(ts_df)
    
    # connect all time series
    ts_all = connect_a_list_of_time_series_df(ts_list, date_col, ts_col, initial_aum, start_end_only)
    ts_all = ts_all[[date_col, ts_col]]
    ts_all = ts_all.copy()
    
    return ts_all


# def get_ts(df_trades):
#     traces = {}
#     for i in range(0, len(df_trades)):
#         t1 = df_trades.loc[i, 'ts_enter']
#         t2 = df_trades.loc[i, 'ts_exit']
#         p1 = df_trades.loc[i, 'price_enter']
#         p2 = df_trades.loc[i, 'price_exit']
#         trace = {t1:p1, t2:p2}
#         traces.append(trace)
    
    




#
# path_ticker = "C:/f_data/sector/indicator_day/XLF_1D_fmt_idc.csv"
# df_ticker = pd.read_csv(path_ticker)
# fig = px.line(df_ticker, x="date", y="close", title='AUM time series')
# fig.show()
#
# df_r = reverse_ts_by_horizontal_line(df_ticker, 'close', 20)
# fig2 = px.line(df_r, x="date", y="close", title='AUM time series')
# fig2.show()