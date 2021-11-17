import numpy as np
import pandas as pd
import plotly.graph_objects as go
from util.util_pandas import df_general_time_filter


def ma_cross(df):
    df['ema8_downcross_ema21'] = np.nan
    df['ema8_upcross_ema21'] = np.nan
    df['ema21_downcross_ma50'] = np.nan
    df['ema21_upcross_ma50'] = np.nan
    
    pre_ema8 = 0
    pre_ema21 = 0
    pre_ma50 = 0
    
    for i in range(0, len(df)):
        # ema 8 & 21
        if pre_ema8 is not np.nan \
        and pre_ema21 is not np.nan \
        and df.loc[i, 'ema8'] is not np.nan \
        and df.loc[i, 'ema21'] is not np.nan:
        
            if pre_ema8 > pre_ema21: # long
                if df.loc[i, 'ema8'] < df.loc[i, 'ema21']:
                    df.loc[i, 'ema8_downcross_ema21'] = 1
            elif pre_ema8 < pre_ema21: # short
                if df.loc[i, 'ema8'] > df.loc[i, 'ema21']:
                    df.loc[i, 'ema8_upcross_ema21'] = 1        

        # ma 21 & 50
        if pre_ma50 is not np.nan \
        and pre_ema21 is not np.nan \
        and df.loc[i, 'ma50'] is not np.nan \
        and df.loc[i, 'ema21'] is not np.nan:
        
            if pre_ema21 > pre_ma50: # long
                if df.loc[i, 'ema21'] < df.loc[i, 'ma50']:
                    df.loc[i, 'ema21_downcross_ma50'] = 1
            elif pre_ema21 < pre_ma50: # short
                if df.loc[i, 'ema21'] > df.loc[i, 'ma50']:
                    df.loc[i, 'ema21_upcross_ma50'] = 1    
        
        
        pre_ema8 = df.loc[i, 'ema8']
        pre_ema21 = df.loc[i, 'ema21']
        pre_ma50 = df.loc[i, 'ma50']
        
#         print(
#             df.loc[i, 'time'], 
#             df.loc[i, 'est_datetime'],
#             df.loc[i, 'ema21'],
#             df.loc[i, 'ema8'],
#             df.loc[i, 'ma50'],
#             df.loc[i, 'ema8_downcross_ema21'],
#             df.loc[i, 'ema8_upcross_ema21'],
#             df.loc[i, 'ema21_downcross_ma50'],
#             df.loc[i, 'ema21_upcross_ma50'],
#         )
        
# # validation
# path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
# 
# # read and compute
# df = pd.read_csv(path)
# ma_cross(df)
# df=df_general_time_filter(df=df, date_col='est_datetime', s='2019-04-19 09:30:00', e='2021-06-19 09:30:00')
# df['ema8_downcross_ema21_ui'] = df['ema8'] * df['ema8_downcross_ema21']
# df['ema8_upcross_ema21_ui'] = df['ema8'] * df['ema8_upcross_ema21']
# df['ema21_downcross_ma50_ui'] = df['ema8'] * df['ema21_downcross_ma50']
# df['ema21_upcross_ma50_ui'] = df['ema8'] * df['ema21_upcross_ma50']
# 
# # draw
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
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema8_upcross_ema21_ui'],
#                     mode='markers', name='ema8_upcross_ema21_ui'))
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema21_downcross_ma50_ui'],
#                     mode='markers', name='ema21_downcross_ma50_ui'))
# fig.add_trace(go.Scatter(x=df['est_datetime'], y=df['ema21_upcross_ma50_ui'],
#                     mode='markers', name='ema21_upcross_ma50_ui'))
# 
# fig.show()