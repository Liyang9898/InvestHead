import numpy as np
import pandas as pd
from util.util_pandas import df_general_time_filter
import plotly.graph_objects as go



def get_velocity_on_metric(df, metric, bar_range, feature_col):
    """
    input:
    df:the indicator Dataframe
    metric: the metric we need to compute speed on
    bar_range: how many gap are there between the start and end price, min = 1
    feature_col: column name of the new feature
    """
    df.reset_index(inplace=True,drop=True)    
    df[feature_col] = np.nan
    
    for r in range(0, len(df)):
        l = r - bar_range
        if l < 0:
            continue
        gap = df.loc[r, metric] - df.loc[l, metric]
        v = gap / bar_range
        df.loc[r, feature_col] = v
        print(v)


def get_velocity(df):
    # added 4 new features type * x time period
    # given time period:
    # price delta
    # price percent delta
    # price change dollar/bar
    # price change dollar percent / bar
     
    velocity_period = [1,2,3,4,5,10,20]
    for period in velocity_period:
        df[f'price_delta_{period}d'] = np.nan
        df[f'price_delta_{period}d_pct'] = np.nan
        df[f'price_velocity_{period}d'] = np.nan
        df[f'price_velocity_{period}d_pct'] = np.nan
    
    
    df['price_delta_oc'] = np.nan
    df['price_delta_oc_pct'] = np.nan

         
    for i in range(0, len(df)):
        df.loc[i, 'price_delta_oc'] = df.loc[i, 'close'] - df.loc[i, 'open']
        df.loc[i, 'price_delta_oc_pct'] = df.loc[i, 'price_delta_oc'] / df.loc[i, 'close']
        
         
        for period in velocity_period:
            if i > period - 1:
                df.loc[i, f'price_delta_{period}d'] = df.loc[i, 'close'] - df.loc[i - period, 'close']
                df.loc[i, f'price_delta_{period}d_pct'] = df.loc[i, f'price_delta_{period}d'] / df.loc[i, 'close']   
                df.loc[i, f'price_velocity_{period}d'] = df.loc[i, f'price_delta_{period}d'] / period
                df.loc[i, f'price_velocity_{period}d_pct'] = df.loc[i, f'price_delta_{period}d_pct'] / period
     


def get_velocity_one_bar_on_close(df):
    df.sort_values(by='date', inplace=True)
    df.reset_index(inplace=True,drop=True)
     
    velocity_period = [1]
    for period in velocity_period:
        df[f'price_delta_{period}bar'] = np.nan
        df[f'price_delta_{period}bar_pct'] = np.nan
        df[f'price_velocity_{period}bar'] = np.nan
        df[f'price_velocity_{period}bar_pct'] = np.nan
    
         
    for i in range(0, len(df)):
         
        for period in velocity_period:
            if i > period - 1:
                df.loc[i, f'price_delta_{period}bar'] = df.loc[i, 'close'] - df.loc[i - period, 'close']
                df.loc[i, f'price_delta_{period}bar_pct'] = df.loc[i, f'price_delta_{period}bar'] / df.loc[i, 'close']   
                df.loc[i, f'price_velocity_{period}bar'] = df.loc[i, f'price_delta_{period}bar'] / period
                df.loc[i, f'price_velocity_{period}bar_pct'] = df.loc[i, f'price_delta_{period}bar_pct'] / period

# 
# # validation
# path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
#  
# # read and compute
# df = pd.read_csv(path)
# df=df_general_time_filter(df=df, date_col='est_datetime', s='2019-04-19 09:30:00', e='2021-06-19 09:30:00')
# 
# get_velocity(df)
# 
# # draw =========================================
# fig = go.Figure()
# for period in [1]:
#     key = f'price_velocity_{period}d_pct'
#     fig.add_trace(go.Scatter(
#             x=df['est_datetime'], 
#             y=df[key],
#             mode='markers', 
#             name=key
#     ))
#     
#     key2 = f'price_delta_{period}d_pct'
#     fig.add_trace(go.Scatter(
#             x=df['est_datetime'], 
#             y=df[key2],
#             mode='markers', 
#             name=key2
#     ))
# 
# fig.show()