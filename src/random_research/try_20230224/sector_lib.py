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


def rebuild_etf(allocation, start_date, end_date, sector_ts_list=[]):
    '''
    allocation: a dict key=ticker, val=allocaiton between 0-1 = initial aum of each ticker of time series
    start/end_date: range of time series
    
    step 1: get ticker price history, cut into time range, scale according to the initial allocation
    step 2: aggregate
    '''
    ts_list = []
    for ticker, initial_aum in allocation.items():
        ticker_path = "C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv".format(ticker=ticker)  
        df_ticker = pd.read_csv(ticker_path)
    
        df_scaled = get_one_sector_ts_scaled(start_date, end_date, df_ticker, initial_aum)
        
        ts_list.append(df_scaled)
        
        ##### for debug ######
        df_scaled['ticker'] = ticker
        sector_ts_list.append(df_scaled)
        ##### for debug ######

    ts_agg = aggregate_ts(ts_list)
    return ts_agg


def connect_ts_df_list(df_list, sector_ts_list_list):
    '''
    df_list: a list of df with col 'date' and 'ts'
    !!! the df are already ordered in chrological order
    '''
    pre_e = 1
    l = []
    sector_ts_list_scaled = []
    
    for i in range(0, len(df_list)):
        df = df_list[i]
        

        val_s = df.loc[0, 'ts']
        
        # re scale
        factor = pre_e / val_s
        df_cp = df.copy()
        
        df_cp['ts'] = df_cp['ts'] * factor
        l.append(df_cp)
        
        # done
        pre_e = df_cp.loc[len(df_cp) - 1, 'ts']
        
        ##### debug ######
        #need to scale secotr_df_list as well
        sector_df_list = sector_ts_list_list[i]
        sector_df_list_scaled = []
        for sector_df in sector_df_list:
            val_s = sector_df.loc[0, 'ts']
            
            if val_s == 0: ### sector not in hold
                continue
            
            initial_aum = val_s * factor
            print(initial_aum)
            df_sector_scaled = df_normalize(sector_df, 'ts', initial_aum)
            sector_df_list_scaled.append(df_sector_scaled)
        
        
        ##### debug ######
        sector_ts_list_scaled.append(sector_df_list_scaled)
        
    df_all = pd.concat(l, axis=0, ignore_index=True)  
    ##### debug ######
    sector_ts_list_list = sector_ts_list_scaled
    ##### debug ######
    return df_all


def extract_allocation_by_year(year):
    path = 'C:/f_data/sector/spy_sector_history_clean.csv'
    df = pd.read_csv(path)
    allocation = df_to_dict(df, 'ticker', str(year))
    return allocation


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