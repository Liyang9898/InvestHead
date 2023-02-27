'''
Created on Feb 26, 2023

@author: spark
'''
import pandas as pd
# import plotly.express as px
from util.util_pandas import df_general_time_filter, df_normalize, df_to_dict, \
    dict_to_df


def get_one_sector_ts_scaled(start_date, end_date, df_sector, initial_aum):
    '''
    Step 1: get ts from sector
    Step 2: trim to time range
    Step 3: reweight to match initial aum
    '''
    df_sector['ts'] = df_sector['close']
    df_sector = df_sector[['date', 'ts']]
    df_sector = df_sector.copy()
    
    df_sector_filtered = df_general_time_filter(df_sector, 'date', start_date, end_date)
    df_sector_filtered_scaled = df_normalize(df_sector_filtered, 'ts', initial_aum)
    return df_sector_filtered_scaled


def aggregate_ts(df_sector_list):
    '''
    df_sector_list is a data frame with 2 mandatory columns: date, ts
    returns a data frame with all ts aggregated on the same ts
    '''
    dict_agg = {}
    for df_sector in df_sector_list:
        dic = df_to_dict(df_sector, 'date', 'ts')
        for k, v in dic.items():
            
            if k not in dict_agg: # first time key
                dict_agg[k] = 0
            
            dict_agg[k] = dict_agg[k] + v
    
    df = dict_to_df(dict_agg, 'date', 'ts')
    return df


def rebuild_etf(allocation, start_date, end_date):
    '''
    allocation: a dict key=ticker, val=allocaiton between 0-1 = initial aum of each ticker of time series
    start/end_date: range of time series
    
    step 1: get ticker price history, cut into time range, scale according to the initial allocation
    step 2: aggregate
    '''
    ts_list = []
    for ticker, initial_aum in allocation.items():
        ticker_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)  
        df_ticker = pd.read_csv(ticker_path)
    
        df_scaled = get_one_sector_ts_scaled(start_date, end_date, df_ticker, initial_aum)
        ts_list.append(df_scaled)

    ts_agg = aggregate_ts(ts_list)
    return ts_agg

########## test
# start_date = '2020-01-01'
# end_date = '2021-01-01'
#
# p1 = "C:/f_data/sector/indicator/XLK_1W_fmt_idc.csv"
# p2 = "C:/f_data/sector/indicator/XLF_1W_fmt_idc.csv"
#
#
# # ticker = 'XLK'
# # sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)  
#
# df1 = pd.read_csv(p1)
# df2 = pd.read_csv(p2)
# # print(df)
# df1 = get_one_sector_ts_scaled(start_date, end_date, df1, 0.7)
# df2 = get_one_sector_ts_scaled(start_date, end_date, df2, 0.1)
#
# df_sector_list = [df1, df2]
# df = aggregate_ts(df_sector_list)
#
# fig = px.line(df, x="date", y="ts", title='mudong op timeseries')
# fig.show()