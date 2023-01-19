'''
Created on Jan 18, 2023

@author: spark
'''


from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from util.util_pandas import df_col_percentile
from util.util_time import df_filter_dy_date 


path = 'C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'
df = pd.read_csv(path)
print(df['date'])

df.sort_values(by='time', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
df['yearly_delta'] = 0


date_col = 'date'
s = '2022-01-01'
e = '2023-01-15'
time_window = 52
# df = df_filter_dy_date(df,date_col,s,e)


for i in range(0, len(df)):
    if i + time_window < len(df):
        t = df.loc[i, 'time']
        s = df.loc[i, 'close']
        e = df.loc[i + time_window, 'close']  
        r = e / s - 1  
        df.loc[i, 'yearly_delta'] = r
r = len(df)
l = len(df)-time_window
df.drop(df.index[l:r], inplace=True)

##########################################################################
df = df[df['ema21']<df['ma50']]
# print(len(df))
##########################################################################
col = 'yearly_delta'
p_list=[0,0.05,0.1,0.15,0.2,0.25,0.5,0.75,0.8,0.85,0.9,0.95,1]
percentile_val = {}
for p in p_list:
    percentile_val[p] = df_col_percentile(df, col, p, asc=True)
    # print(p, percentile_val[p])
    # print(p)
    print(percentile_val[p])

##########################################################################
# over all histogram
fig = px.histogram(df, x="yearly_delta",title='overall yearly delta distribution')
fig.show()

# time chart
fig2 = px.line(df, x="date", y="yearly_delta", title='yearly delta')
fig2.show()


##########################################################################
# df = df[df['ema21']>df['ma50']]
# print(len(df))
#
#
# positive = df[df['yearly_delta']>0]
# negative = df[df['yearly_delta']<0]
#
# fig_p = px.histogram(positive, x="yearly_delta", cumulative=True,histnorm='percent',title='up',nbins=200)
# fig_p.show()
#
# fig_n = px.histogram(negative, x="yearly_delta", cumulative=True,histnorm='percent',title='down',nbins=200)
# fig_n.show()
