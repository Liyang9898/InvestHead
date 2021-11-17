'''
Created on Mar 12, 2021

@author: leon
'''
from datetime import datetime, timedelta 
from functools import reduce

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from trade_analysis_master.constant.constant import adjust_for_measure
from trade_analysis_master.plot_lib.lib import time_range_gain, list_delta, \
    incremental, roll, ab_test
from trade_analysis_master.plot_lib.measure_adjustment import agg_plot_adjustment_benchmark
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


def ploty_daily_position_cnt(experiment_name):
    path = experiment_name + 'merge/daily_position_cnt.csv'
    df = pd.read_csv(path)
    fig = px.line(df, x="date", y="position_cnt", title=experiment_name)
    fig.show()
    

def trade_date(x):
    b= x.split(' ')[0]
    dt = datetime.strptime(b, "%Y-%m-%d")
    return dt.strftime("%Y-%m-%d")

def plot_cash_line(trade_folder):
    # SPY
    spy = bench_mark("D:/f_data/sweep_20201214/baseline/spy.csv", 'spy')
    iwf = bench_mark("D:/f_data/sweep_20201214/baseline/iwf.csv", 'iwf')
    
    # reuse
    reuse_cash_line_csv_path = trade_folder + """merge/cash_line_reuse.csv"""
    df_reuse = pd.read_csv(reuse_cash_line_csv_path)
    
    # idle
    cash_line_path = trade_folder + """merge/cash_history_idle_cash_history.csv"""
    df_idle = pd.read_csv(cash_line_path)
    df_idle['date']=df_idle.apply(
        lambda row : trade_date(row['date']), 
        axis = 1
    )  
    
    dfs = [df_reuse, df_idle, spy, iwf]
    df_merge = reduce(lambda df1,df2: pd.merge(df1,df2,on='date'), dfs)
    df_merge.to_csv(trade_folder + """merge/ui_backend_data.csv""")
    # ab test
    exp = 'fix'
    base = 'iwf'
    # 253, 126
    diff = 126
    ab_test(df_merge, exp, base, diff)
    # ab test end
    
    # daily distribution
    delta_df(df_merge, 'fix')
    delta_df(df_merge, 'roll')
    
    xbins=dict(size=0.005)
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df_merge['fix_delta'], histnorm=PX_PERCENT_HIST, name='fix_delta', xbins=xbins))
    fig.add_trace(go.Histogram(x=df_merge['roll_delta'], histnorm=PX_PERCENT_HIST, name='roll_delta', xbins=xbins))
    fig.show()
    
    
    
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['price_position'],mode='lines',name='price'))
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['spy'],mode='lines',name='spy'))
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['iwf'],mode='lines',name='iwf'))
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['fix'],mode='lines',name='reuse_fix'))
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['roll'],mode='lines',name='reuse_roll'))
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['cash_fixed_base_position'],mode='lines',name='idle_fix'))
    fig.add_trace(go.Scatter(x=df_merge['date'], y=df_merge['cash_rollover_position'],mode='lines',name='idle_roll'))
    fig.show()
    
    # plot drop comparison during adjustment
    agg_plot_adjustment_benchmark(df_merge, adjust_for_measure)

    last_i = len(df_merge) - 1
    keys = ['price_position','spy','iwf','fix','roll','cash_fixed_base_position','cash_rollover_position']
    factor = {}
    fig2 = go.Figure()
    
    for k in keys:
        factor[k] = df_merge.loc[last_i, k]
        new_k = k+'_normalized'
        df_merge[new_k] = df_merge[k] / factor[k]
         
        fig2.add_trace(go.Scatter(x=df_merge['date'], y=df_merge[new_k],mode='lines',name=new_k))
    fig2.show()


def bench_mark(path, key):
    spy = pd.read_csv(path)
    spy['date']=spy.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d'), axis = 1)
    spy[key] = spy['close']
    spy = spy[['date',key]]
    spy = spy.loc[(spy['date']>="2016-01-01") & (spy['date']<="2021-01-07")]
    base = spy[key].to_list()[0]
    spy[key] = spy[key] / base
    return spy


def plot_pnl_distribution(trade_folder):

    path = trade_folder + """merge/all_trades_all_entry.csv"""
    df = pd.read_csv(path)
#     print(df)
    
    fig = px.histogram(df, x="pnl_percent",range_x=[-0.2, 0.2])
    fig.show()

def plot_moving_window_hist(trade_folder):
#     xbins=dict(start=-1.0,end=1.0,size=0.01)
    path = trade_folder + """merge/moving_windows.csv"""
    df = pd.read_csv(path)
#     print(df)
    fig = go.Figure()
    for i in range(0, len(df)):
        window = df.loc[i, 'window']
        positive_rate = df.loc[i, 'positive_rate']
        window_pnl_p_avg = df.loc[i, 'window_pnl_p_avg']
        pnl_list = df.loc[i, 'pnl_list']
        name = str(window) + ' avg:' + str(window_pnl_p_avg) + ' rate:' + str(positive_rate)
        tokens = pnl_list.split(',')
        
        fig.add_trace(go.Histogram(histnorm='percent',x=tokens, name = name))
    fig.show()



# trade_path = t_20210420_ema21_ma50_gap_per_ticker

# trade_path =  t_20210511_ema21_ma50_gap_per_ticker_3p_out
trade_path =  t_20210425_ema21_ma50_gap_per_ticker_4p_out
# trade_path = t_20210518_ema21_ma50_gap_per_ticker_6p_out
# trade_path =  t_20210518_ema21_ma50_gap_per_ticker_8p_out
# trade_path =  t_20210518_ema21_ma50_gap_per_ticker_10p_out
# trade_path =  t_20210518_ema21_ma50_gap_per_ticker_12p_out
# trade_path = t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage

trade_folder = plot_cash_line(trade_path)
# ploty_daily_position_cnt(trade_path)
# plot_pnl_distribution(trade_path)
# plot_moving_window_hist(trade_path)
