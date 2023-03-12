'''
Created on Mar 11, 2023

@author: spark
'''
import numpy as np
import pandas as pd

def get_pnl_pct_on_metric(df, feature_name, window_size, base_col):
    if window_size >= len(df):
        raise Exception('window too big')
    df[feature_name] = np.nan
    for end_idx in range(window_size, len(df)):
        start_idx = end_idx - window_size
        val_end = df.loc[end_idx, base_col]
        val_start = df.loc[start_idx, base_col]
        
        s_d = df.loc[start_idx, 'date']
        e_d = df.loc[end_idx, 'date']
        
        s = s_d + ' ' + str(val_start) + ' ' + e_d + ' ' + str(val_end)
        print(s)
        
        
        pnl_pct = val_end / val_start - 1
        df.loc[end_idx, feature_name] = pnl_pct
        

################## test ####################################

# ticker = 'XLK'
# sector_idc_path = "C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv".format(ticker=ticker)  
#
# df = pd.read_csv(sector_idc_path)
# print(df.columns)
# print(len(df.columns))
#
# get_pnl_pct_on_metric(df, 'pnl_pct_20_bar', 20, 'close')
# print(df.columns)
# print(len(df.columns))

################## test ####################################

