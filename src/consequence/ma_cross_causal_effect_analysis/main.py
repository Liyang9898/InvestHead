from indicator_master.feature_lib.ma_cross import ma_cross
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from util.util_pandas import df_general_time_filter


# validation
path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
 
# read and compute
df = pd.read_csv(path)
ma_cross(df)
df=df_general_time_filter(df=df, date_col='est_datetime', s='2016-06-19 09:30:00', e='2021-06-19 09:30:00')

event = {}
for i in range(1, len(df)):
    time=df.loc[i, 'est_datetime']
    if df.loc[i-1, 'ema8_downcross_ema21'] == 1.0:
        event[time] = 'ema8_downcross_ema21'
    elif df.loc[i-1, 'ema8_upcross_ema21'] == 1.0:
        event[time] = 'ema8_upcross_ema21'
    elif df.loc[i-1, 'ema21_downcross_ma50'] == 1.0:
        event[time] = 'ema21_downcross_ma50'
    elif df.loc[i-1, 'ema21_upcross_ma50'] == 1.0:
        event[time] = 'ema21_upcross_ma50'

 
pre = ''
causal_effect = {}
for ts, e in event.items():
    # do some work
    if pre == 'ema8_downcross_ema21' or pre == 'ema8_upcross_ema21':
        key = pre + '|' + e
        if key not in causal_effect.keys():
            causal_effect[key] = []
        causal_effect[key].append(ts)
        
    # set pre
    pre = e


for k, dates in causal_effect.items():
    print(k, len(dates), dates)