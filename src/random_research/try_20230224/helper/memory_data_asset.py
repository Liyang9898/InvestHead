'''
Created on Mar 19, 2023

@author: spark
'''
import pandas as pd


def prepare_ticker_df_dict(ticker_list):
    ticker_df_dict = {}
    for ticker in ticker_list:
        if 'date' in ticker:
            continue    
        ticker_path = "C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv".format(ticker=ticker)
        ticker_df = pd.read_csv(ticker_path)
        
        # reformat
        ticker_df['ts'] = ticker_df['close']
        ticker_df = ticker_df[['date', 'ts']]
        ticker_df = ticker_df.copy()
        ticker_df_dict[ticker] = ticker_df
    return ticker_df_dict


def prepare_ticker_idc_df_dict(ticker_list):
    ticker_df_dict = {}
    for ticker in ticker_list:
        if 'date' in ticker:
            continue    
        ticker_path = "C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv".format(ticker=ticker)
        ticker_df = pd.read_csv(ticker_path)
        
        # reformat
        ticker_df = ticker_df.copy()
        ticker_df_dict[ticker] = ticker_df
    return ticker_df_dict