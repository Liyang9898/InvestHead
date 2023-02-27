'''
Created on Feb 26, 2023

@author: spark
'''
from functools import reduce

import pandas as pd
import plotly.express as px
from util.util_pandas import dict_to_df


def ema21_below_ma50(ema21, ma50):
    if ema21 < ma50:
        return 1
    else:
        return 0


def today_changed(df, compare_column):
    change_log = {}
    for cur in range(1, len(df)):
        date = df.loc[cur, 'date']
        change_log[date] = 0
        
        # compare column and log change_log
        for col in compare_column:
            val_cur = df.loc[cur, col]
            val_pre = df.loc[cur - 1, col]
            
            if val_cur != val_pre:
                change_log[date] = 1
                break
    
    df_changed = dict_to_df(change_log, 'date', 'changed')
    return df_changed

    

tickers = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLRE', 'XLU']
dfs = []
for ticker in tickers:
    sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)  
    df = pd.read_csv(sector_idc_path)
    df['ema21_below_ma50']=df.apply(lambda row : ema21_below_ma50(row['ema21'], row['ma50']), axis = 1)
    df[ticker] = df['ema21_below_ma50']
    df=df[['date', ticker]]
    df=df.copy()
    dfs.append(df)


df_merge = reduce(lambda df1,df2: pd.merge(df1,df2,on='date'), dfs)
# print(df_merge)

df_changed = today_changed(df_merge, tickers)
# print(df_changed)

df_merge_changed = reduce(lambda df1,df2: pd.merge(df1,df2,on='date'), [df_merge, df_changed])
print(df_merge_changed)

p = "C:/f_data/sector/feature/ema21_below_ma50.csv"
df_merge_changed.to_csv(p, index=False)

fig = px.line(df_merge_changed, x="date", y="changed", title='mudong op timeseries')
fig.show()