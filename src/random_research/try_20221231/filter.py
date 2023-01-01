'''
Created on Jan 1, 2023

@author: spark
'''
import pandas as pd

path = 'C:/f_data/random/SPY_1W_1_year_return.csv'
df = pd.read_csv(path)
print(df.columns)
df_long = df[df['ema21']>df['ma50']]
df_short = df[df['ema21']<df['ma50']]
df_long.reset_index(drop=True, inplace=True)
df_short.reset_index(drop=True, inplace=True)

path_long = 'C:/f_data/random/SPY_1W_1_year_return_long.csv'
path_short = 'C:/f_data/random/SPY_1W_1_year_return_short.csv'

df_long.to_csv(path_long, index=False)
df_short.to_csv(path_short, index=False)
print(df_long)
print(df_short)