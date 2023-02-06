'''
Created on Jan 17, 2023

@author: spark
'''

import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from util.util_time import df_filter_dy_date 


path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df = pd.read_csv(path)

df.sort_values(by='time', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
df['close_to_close_delta'] = 0
df['weekday'] = 0
# print(df['date'])
print(df.columns)

date_col = 'date'
s = '2021-01-01'
e = '2023-01-15'

df = df_filter_dy_date(df,date_col,s,e)


for i in range(0, len(df)):
    if i + 1 < len(df):
        t = df.loc[i, 'time']
        s = df.loc[i, 'open']
        e = df.loc[i + 1, 'close']  
        r = e / s - 1  
        df.loc[i, 'close_to_close_delta'] = r
        
        dt = datetime.fromtimestamp(int(t))
        wd = dt.weekday()
        df.loc[i, 'weekday'] = wd
        
        



fig = px.histogram(df, x="close_to_close_delta", barmode="overlay")
fig.show()

df = df[df['ema8']>df['ema21']]
print(len(df))


positive = df[df['close_to_close_delta']>0]
negative = df[df['close_to_close_delta']<0]



fig_all = px.histogram(negative, x="close_to_close_delta", barmode="overlay",cumulative=True,histnorm='percent',nbins=200)
fig_all.show()
fig_all2 = px.histogram(positive, x="close_to_close_delta", barmode="overlay",cumulative=True,histnorm='percent',nbins=200)
fig_all2.show()
