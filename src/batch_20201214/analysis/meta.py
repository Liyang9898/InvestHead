'''
Created on Feb 15, 2021

@author: leon
'''
import pandas as pd

path_ticker = """D:/f_data/sweep_20201214/white_list/20210117_2b_1m_10trade_60win_positive_iwf_200.csv"""
path_meta = """D:/f_data/sweep_20201214/all_ticker_meta/20210117_ticker_meta_with_vol.csv"""
path_ticker_with_mata = """D:/f_data/sweep_20201214/white_list/with_meta/20210117_2b_1m_10trade_60win_positive_iwf_200.csv"""

df_ticker = pd.read_csv(path_ticker)
df_meta = pd.read_csv(path_meta)

print(df_ticker)
print(df_meta)
result = pd.merge(df_ticker, df_meta, how="inner", on=["ticker"])
result['vol_dollar'] = result['vol'] * result['LastSale']
print(result)

result.to_csv(path_ticker_with_mata)