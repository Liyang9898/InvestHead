import numpy as np
import pandas as pd
import plotly.graph_objects as go
from util.util_pandas import df_general_time_filter
from indicator_master.feature_lib.velocity import get_velocity
from indicator_master.feature_lib.ma_cross import ma_cross
from indicator_master.feature_lib.having_x_in_y_bars import have_x_in_y_bars
# validation
path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
  
def labeling(x):
    if x != 1:
        return False
    else: 
        return True

# read and compute
df = pd.read_csv(path)
df=df_general_time_filter(df=df, date_col='est_datetime', s='2019-04-19 09:30:00', e='2021-06-19 09:30:00')
ma_cross(df)
have_x_in_y_bars(df, 'ema21_downcross_ma50', 20, 'ema21_downcross_ma50_in_20_bar')
get_velocity(df)

df['label'] = df.apply(lambda row:labeling(row['ema21_downcross_ma50_in_20_bar']),axis=1)
# print(df.columns)
df = df[df['ema21']>df['ma50']]


df.to_csv('D:/f_data/temp/v_to_21_50_cross_training_eval.csv')
 
# draw =========================================
fig = go.Figure()
for period in [1]:
    key = f'price_velocity_{period}d_pct'
    fig.add_trace(go.Scatter(
            x=df['est_datetime'], 
            y=df[key],
            mode='markers', 
            name=key
    ))
      
    key2 = f'price_delta_{period}d_pct'
    fig.add_trace(go.Scatter(
            x=df['est_datetime'], 
            y=df[key2],
            mode='markers', 
            name=key2
    ))
  
fig.show()