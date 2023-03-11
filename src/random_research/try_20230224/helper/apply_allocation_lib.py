'''
Created on Mar 11, 2023

@author: spark
'''
import pandas as pd
from util.util_pandas import df_general_time_filter, df_normalize, dict_to_df


def get_ts_from_allocaiton(allocation_dic, start_date, end_date):
    sum = 0 
    ts_dic_agg = {}
    
    for ticker, allocation in allocation_dic.items():
        if allocation == 0:
            continue
        sum = sum + allocation
        ticker_path = "C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv".format(ticker=ticker)  
        df_ticker = pd.read_csv(ticker_path)
        
        # check coverage
        date_min = df_ticker['date'].min()
        assert date_min < start_date
        date_max = df_ticker['date'].max()
        assert date_max > end_date
        
        # filtered
        df_ticker_filtered = df_general_time_filter(df_ticker, 'date', start_date, end_date)
        df_ticker_filtered['ts'] = df_ticker_filtered['close']
        df_ticker_filtered = df_ticker_filtered[['date', 'ts']]
        df_ticker_filtered = df_ticker_filtered.copy()
        
        # note first trading day might not be start_date
        # normalization: first trading date needs to follow allocation
        df_ticker_scaled = df_normalize(df_ticker_filtered, 'ts', initial_val=allocation)
        for i in range(0, len(df_ticker_scaled)):
            date = df_ticker_scaled.loc[i, 'date']
            v = df_ticker_scaled.loc[i, 'ts']
            if date not in ts_dic_agg.keys():
                ts_dic_agg[date] = 0
            ts_dic_agg[date] = ts_dic_agg[date] + v
        
    assert abs(1 - sum) < 0.02
    df = dict_to_df(ts_dic_agg, 'date', 'ts')
    df.reset_index(drop=True, inplace=True)
    return df
    

def connection_ts(allocation_df):
    cols = list(allocation_df.columns).copy()
    cols.remove('start_date')
    cols.remove('end_date')
    ticker_list = cols
    
    pre_end_val = 1
    dfs = []
    
    for i in range(0, len(allocation_df)):
        start_date = allocation_df.loc[i, 'start_date']
        end_date = allocation_df.loc[i, 'end_date']
        print(start_date)
        
        # get allocation
        allocaiton_dic = {}
        for ticker in ticker_list:
            if allocation_df.loc[i, ticker] != 0:
                allocaiton_dic[ticker] = allocation_df.loc[i, ticker]
        
        # get ts for that time period
        df_ts_sub = get_ts_from_allocaiton(allocaiton_dic, start_date, end_date)
        df_ts_sub_scaled = df_normalize(df=df_ts_sub, normalize_col='ts', initial_val=pre_end_val)
        # normalize = 
        
        #meta
        first_val = df_ts_sub_scaled.loc[0, 'ts']
        last_val = df_ts_sub_scaled.loc[len(df_ts_sub) - 1, 'ts']
        
        assert abs(pre_end_val - first_val) < 0.02
        dfs.append(df_ts_sub_scaled)

        
        pre_end_val = last_val
        
        
    df_all = pd.concat(dfs, axis=0, ignore_index=True)  
    df_all.sort_values(by=['ts'])
    df_all.reset_index(inplace=True, drop=True)
    
    
    return df_all

