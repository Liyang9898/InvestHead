'''
Created on Feb 26, 2023

@author: spark
'''
from functools import reduce

import pandas as pd
import plotly.express as px
from util.util_pandas import dict_to_df
from util.util_time import date_add_days, get_year_str


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

# fig = px.line(df_merge_changed, x="date", y="changed", title='mudong op timeseries')
# fig.show()


###################### create allocation signal #######################
'''
this part create a csv, with time range and the signal for allocation in this time range
'''

# keep changed only
df_merge_changed.loc[0, 'changed'] = 1
df_merge_changed_only = df_merge_changed[df_merge_changed['changed']==1]
df_merge_changed_only = df_merge_changed_only.copy()
df_merge_changed_only.reset_index(drop=True, inplace=True)


# apply range
'''
col date in df is the date of the first occurence of this pattarn, meaning 'start_date'
'''
df_range_feature = df_merge_changed_only
df_range_feature['start_date'] = df_range_feature['date']
df_range_feature['end_date'] = df_range_feature['date']

for i in range(0, len(df_range_feature)-1):
    next_start_date = df_range_feature.loc[i + 1, 'start_date']
    end_date = date_add_days(next_start_date, -1)
    df_range_feature.loc[i, 'end_date'] = end_date


# join spy allocation
df_range_feature['year']=df_range_feature.apply(lambda row : get_year_str(row['date']), axis = 1)
p_allocation_signal = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50.csv"
df_range_feature.to_csv(p_allocation_signal, index=False)
print(df_range_feature)