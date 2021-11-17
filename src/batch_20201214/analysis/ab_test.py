'''
Created on Jan 27, 2021

@author: leon
'''
import pandas as pd
from pandas._libs import index


path_test = "D:/f_data/sweep_20201214/filtered/20210209_ribbon_start.csv"
path_control = "D:/f_data/sweep_20201214/filtered/20210117_2b_1m_10trade_60win_positive_iwf.csv"
path_diff = "D:/f_data/sweep_20201214/ab_test/diff_ribbon_start_vs_2b_1m_10trade_60win_positive_iwf.csv"


join_key = 'ticker'
tracking_cols=[
    'all_universe_win_rate',
    'all_universe_lose_rate',
    'total_pnl_fix',
    'total_pnl_rollover',
    'total_trades'
]

df_test = pd.read_csv(path_test)
df_control = pd.read_csv(path_control)

def append_col(df, tracking_cols, postfix):
    for col in tracking_cols:
        col_new = col + postfix
        df[col_new] = df[col]
    return df

def merge_test_control(df_test, df_control, tracking_cols):
    df_test = append_col(df_test, tracking_cols, '_test')
    df_control = append_col(df_control, tracking_cols, '_control')
    df_merged = df_test.merge(df_control, left_on=join_key, right_on=join_key, how='inner')
    
    useful_col = []
    
    for col in tracking_cols:
        col_test = col + '_test'
        col_control = col + '_control'
        col_diff = col + '_diff'
        df_merged[col_diff] = df_merged[col_test] - df_merged[col_control]
        useful_col.append(col_diff)
        useful_col.append(col_test)
        useful_col.append(col_control)
        
    for col in df_merged.columns.to_list():
        if col not in useful_col:
            del df_merged[col]   
        
    return df_merged

df_merged = merge_test_control(df_test, df_control, tracking_cols)
df_merged.to_csv(path_diff, index=False)

print(df_merged.mean())