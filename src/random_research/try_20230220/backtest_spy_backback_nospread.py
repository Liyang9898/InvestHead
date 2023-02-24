'''
Created on Jan 17, 2023

@author: spark
'''

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from util.general_ui import plot_trades_simple_base
from util.util_time import df_filter_dy_date 

'''
check spread cost opportunity
1. exclude eco data date and day before
2. spot check feature
---2022/6/9, just sell off before major eco release day?
'''

'''
the option premium is defined by market maker, which is a key of your profitability. The market maker's job is to make your momney
'''

path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df = pd.read_csv(path)

df.sort_values(by='time', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
df['close_to_close_delta'] = 0
df['weekday'] = 0
# print(df.columns)
# print(df['date'])
# print(df.columns)

date_col = 'date'
# s = '2022-01-24'
# e = '2023-01-15'


s = '2022-01-01'
e = '2023-01-15'


threshold = 0.025
threshold_stable = 0.01

buyback_lose = -0.5

gain = 0.11


df = df_filter_dy_date(df,date_col,s,e)

df['pnl'] = gain
df['pnl_cumulative'] = 0
loss_point = {}
win_point = {}

trade_cnt = 0
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
        date = df.loc[i + 1, 'date'] 
        
        # check stable
        stable = True
        if i > 4:
            if abs(df.loc[i-2, 'close_to_close_delta']) > threshold_stable or abs(df.loc[i-3, 'close_to_close_delta']) > threshold_stable or abs(df.loc[i-4, 'close_to_close_delta']) > threshold_stable:
            # if abs(df.loc[i-2, 'close_to_close_delta']) > threshold_stable:
                
                stable = False

        
        sell_put_green_light = False
        # if df.loc[i, 'ema8']>df.loc[i, 'ema21'] and df.loc[i, 'ema8_ema21_MACD'] > 0 and stable:
        if df.loc[i, 'ema8']>df.loc[i, 'ema21']:
        # if df.loc[i, 'ema8']>df.loc[i, 'ema21'] and df.loc[i, 'ema8_ema21_MACD'] > 0:
            sell_put_green_light = True
            
        sell_call_green_light = False
        # if df.loc[i, 'ema8']<df.loc[i, 'ema21'] and df.loc[i, 'ema8_ema21_MACD'] < 0 and stable:
        if df.loc[i, 'ema8']<df.loc[i, 'ema21']:
        # if df.loc[i, 'ema8']<df.loc[i, 'ema21'] and stable:
            sell_call_green_light = True
        
        # strategy
        pnl = 0
        cur_price = df.loc[i, 'open']
        end_price = df.loc[i + 1, 'close']  
        
        if sell_put_green_light: # sell put
            strike = cur_price * (1-threshold)
            if end_price < strike: # lose case
                pnl = buyback_lose
                loss_point[date] = end_price # lose
            else:
                win_point[date] = end_price # it will mark UI on the time of the cash in
                pnl = gain # win
                
            trade_cnt = trade_cnt + 1
            
        elif sell_call_green_light: # sell call
            strike = cur_price * (1+threshold)
            if end_price > strike: # lose case
                pnl = buyback_lose
                loss_point[date] = end_price # lose
            else:
                win_point[date] = end_price # it will mark UI on the time of the cash in
                pnl = gain # win
            trade_cnt = trade_cnt + 1
        else:
            pnl = 0 # no action for the day
            
        df.loc[i, 'pnl'] = pnl
        df.loc[i+1, 'pnl_cumulative'] = df.loc[i, 'pnl_cumulative'] + pnl

fig = px.line(df, x="date", y="pnl_cumulative", title='spy single day op')
fig.show()

plot_trades_simple_base(
    df, 
    enters=loss_point, 
    exits=win_point, 
    ticker='default', 
    is_image=False, 
    image_folder=None,
    ma_only=False
)
print(trade_cnt)

print('win')
print(len(win_point))
print('lose')
print(len(loss_point))
# path = 'C:/f_data/random/spy_single_day_op.csv'
# df.to_csv(path, index=False)
#
# fig = px.histogram(df, x="close_to_close_delta", barmode="overlay")
# fig.show()
#
# df = df[df['ema8']>df['ema21']]
# print(len(df))
#
#
# positive = df[df['close_to_close_delta']>0]
# negative = df[df['close_to_close_delta']<0]
#
#
#
# fig_all = px.histogram(negative, x="close_to_close_delta", barmode="overlay",cumulative=True,histnorm='percent',nbins=200)
# fig_all.show()
# fig_all2 = px.histogram(positive, x="close_to_close_delta", barmode="overlay",cumulative=True,histnorm='percent',nbins=200)
# fig_all2.show()
