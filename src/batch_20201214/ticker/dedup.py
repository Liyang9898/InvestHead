'''
Created on Jan 6, 2021

@author: leon
'''

# NASDAQ Updated their site, so you will have to modify the URLS:
# 
# NASDAQ
# 
# https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download
# AMEX
# 
# https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download
# NYSE
# 
# https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download

import pandas as pd
df=pd.read_csv("D:/f_data/sweep_20201214/all_ticker_meta/ticker_raw/all.csv")
print(df)
df_dedup = df.drop_duplicates(subset='Symbol', keep="last")
df_dedup.to_csv("D:/f_data/sweep_20201214/all_ticker_meta/ticker_raw/ticker_all_20210106.csv")
print(df_dedup)