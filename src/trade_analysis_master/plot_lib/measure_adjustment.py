from datetime import datetime, timedelta 
from functools import reduce

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from trade_analysis_master.constant.constant import S, E
from trade_analysis_master.plot_lib.lib import time_range_gain, list_delta, \
    incremental, roll, ab_test
from util.util import delta_df, PX_PERCENT_HIST
from version_master.version import (
#     trade_swing_2150in_2150out_20210302_iwf_channel,
    trade_swing_2150in_2150out_20210227_iwf,
#     trade_swing_2150in_2150out_20210302_iwf_trend_start,
    trade_swing_2150in_2150out_20210310_iwf_channel_in,
    trade_swing_2150in_2150out_20210310_iwf_channel_out,
    trade_swing_2150in_2150out_20210310_iwf_channel_inout,
    trade_swing_2150in_2150out_20210313_iwf_50up,
    trade_swing_2150in_2150out_20210313_iwf,
    
    t_20210314_iwf_ma50up_channel_out,
    t_20210314_iwf_ma50up_channel_inout,
    
    t_20210321_myswing_20210321,
    t_20210321_myswing,
    t_20210404_myswing_4percent_out,
    t_20210404_myswing,
    t_20210418_myswing,
    t_20210420_ema21_ma50_gap_per_ticker,
    t_20210425_ema21_ma50_gap_per_ticker_4p_out,
    t_20210511_ema21_ma50_gap_per_ticker_3p_out,
    t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage,
    t_20210518_ema21_ma50_gap_per_ticker_6p_out,
    
    t_20210518_ema21_ma50_gap_per_ticker_8p_out,
    t_20210518_ema21_ma50_gap_per_ticker_10p_out,
    t_20210518_ema21_ma50_gap_per_ticker_12p_out,
)


# experiment = t_20210518_ema21_ma50_gap_per_ticker_12p_out
# path = f"{experiment}merge/ui_backend_data.csv"
# print(path)
# 
# df = pd.read_csv(path)
# print(df)

def meaure_adjustment(df, adjustments):
    rows = []
    for adj in adjustments:
        
        df_start=df[df['date']==adj[S]]
        df_start.reset_index(drop=True, inplace=True)
        df_end=df[df['date']==adj[E]]
        df_end.reset_index(drop=True, inplace=True)

        res = {
            S:adj[S],
            E:adj[E],
            'date_period': f"{adj[S]}_{adj[E]}",
            'spy_delta':  (df_end.loc[0, 'spy'] - df_start.loc[0, 'spy']) / df_start.loc[0, 'spy'],
            'iwf_delta':  (df_end.loc[0, 'iwf'] - df_start.loc[0, 'iwf']) / df_start.loc[0, 'iwf'],
            'fix_delta':  (df_end.loc[0, 'fix'] - df_start.loc[0, 'fix']) / df_start.loc[0, 'fix'],
            'roll_delta':  (df_end.loc[0, 'roll'] - df_start.loc[0, 'roll']) / df_start.loc[0, 'roll'],
            'price_delta':  (df_end.loc[0, 'price_position'] - df_start.loc[0, 'price_position']) / df_start.loc[0, 'price_position']
        }
        rows.append(res)
    df_res = pd.DataFrame(rows)
    return df_res
        

def plot_adjustment_benchmark(df_res):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_res['date_period'],
        y=df_res['spy_delta'],
        name='spy',
    ))
    fig.add_trace(go.Bar(
        x=df_res['date_period'],
        y=df_res['iwf_delta'],
        name='iwf',
    ))
    fig.add_trace(go.Bar(
        x=df_res['date_period'],
        y=df_res['roll_delta'],
        name='roll',
    ))
    fig.add_trace(go.Bar(
        x=df_res['date_period'],
        y=df_res['price_delta'],
        name='price',
    ))
    fig.update_layout(title_text='Drop comparison during adjustment')
    fig.show()
    
def agg_plot_adjustment_benchmark(df, adjust_for_measure):
    df_res = meaure_adjustment(df, adjust_for_measure)
    plot_adjustment_benchmark(df_res)
    
# agg_plot_adjustment_benchmark(df)