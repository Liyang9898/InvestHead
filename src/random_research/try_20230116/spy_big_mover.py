'''
Created on Jan 16, 2023

@author: spark
'''
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from random_research.try_20220116.spy_big_mover_constant import cpi_date, \
    consumer_prel_date, consumer_final_date, gdp_date
from util.general_ui import plot_candle_stick
from util.util_finance_chart import plot_candle_stick_with_trace
from util.util_time import df_filter_dy_date

'''

'''

def get_big_move_week(df, threshold):
    '''
    return a list of date, 
    where spy weekly return are more than a threshold
    '''
    res = []
    for i in range(0, len(df)):
        date = df.loc[i, 'date']
        delta = df.loc[i, 'weekly_delta_abs']
        if delta > threshold:
            res.append(date)
    return res


path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df = pd.read_csv(path)

df.sort_values(by='time', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
df['weekly_delta'] = 0
df['weekly_delta_abs'] = 0
df['weekday'] = 0
# print(df['date'])
print(df.columns)

date_col = 'date'
s = '2022-01-01'
e = '2023-01-15'
threshold = 0.03

df = df_filter_dy_date(df,date_col,s,e)

for i in range(0, len(df)):
    if i + 4 < len(df):
        t = df.loc[i, 'time']
        s = df.loc[i, 'close']
        e = df.loc[i + 4, 'close']  
        r = e / s - 1  
        df.loc[i, 'weekly_delta'] = r
        df.loc[i, 'weekly_delta_abs'] = abs(r)
        
        dt = datetime.fromtimestamp(int(t))
        wd = dt.weekday()
        df.loc[i, 'weekday'] = wd
        
        
fig = px.histogram(df, x="weekly_delta", barmode="overlay")
fig.show()        
        
big_move_date_list = get_big_move_week(df, threshold)
# print(big_move_date_list)

consumer_prel_date
consumer_final_date
plot_candle_stick(df=df, date_marker=gdp_date, date_marker2=big_move_date_list, ticker='default', path=None)