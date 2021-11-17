
from indicator_master.feature_lib.ma_cross import ma_cross
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from util.util_pandas import df_general_time_filter


def have_x_in_y_bars(df, x_feature, y, feature):
    # feature = 1 if x_feature will be 1 in next y bars
    
    recent = -1
    df[feature] = np.nan
    for i in range(0, len(df)):
        i = len(df) - 1 - i # scan from back

        if df.loc[i, x_feature] == 1:
            recent = i 
            
        if recent > 0 and recent - i <= y: # has x_feature=1 and within 10 bar on recent left
            df.loc[i, feature] = 1
            
# 
# # validation
# path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
#  
# # read and compute
# df = pd.read_csv(path)
# ma_cross(df)
# df=df_general_time_filter(df=df, date_col='est_datetime', s='2019-04-19 09:30:00', e='2021-06-19 09:30:00')
# have_x_in_y_bars(df, 'ema8_downcross_ema21', 1, 'ema8_downcross_ema21_in_10_bar')
# # draw
# df['ema8_downcross_ema21_ui'] = df['ema8'] * df['ema8_downcross_ema21']
# df['ema8_downcross_ema21_in_10_bar_ui'] = df['ema8'] * df['ema8_downcross_ema21_in_10_bar']
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema21'],
#                     mode='lines',
#                     name='ema21'))
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema8'],
#                     mode='lines',
#                     name='ema8'))
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ma50'],
#                     mode='lines', name='ma50'))
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema8_downcross_ema21_ui'],
#                     mode='markers', name='ema8_downcross_ema21_ui'))
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema8_downcross_ema21_in_10_bar_ui'],
#                     mode='markers', name='ema8_downcross_ema21_in_10_bar_ui'))
#  
# fig.show()