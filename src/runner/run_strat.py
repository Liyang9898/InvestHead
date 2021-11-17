import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from plot.plot import plot_day_chart_multi
from plot.runner import run
from plot.util import pnltimeseries, plottimeseries,pnltotaltimeseries,pnldistribution,plotcategory,pnldistributionagg,plotpie,pnlma,plottimeseriesmultiline
from strat.replay_wrap import replay
from strat.replay_xxtill import replay_xxtill
from plot.stat import compute_stat
import numpy as np
import plotly.express as px
import time


def back_test(stop_gain, stop_loss, threshold, opentop, df, start_time, end_time,daytrade_endtime):
    ds_unique = df.date.unique()
    dss_df = ds_unique[:]
    dss = []
    for ds in dss_df:
        if ds >= start_time and ds <= end_time:
            dss.append(ds)

    trades = dict()
    df_one_days = dict()
    for ds in dss:
        df_one_days[ds] = df.loc[((df['date']==ds) & (df['est_time'] < daytrade_endtime)),:]
        
        stop_gain_calibrated=stop_gain
        stop_loss_calibrated=stop_loss

        trades[ds] = replay(
            df_one_days[ds], 
            end_time, 
            stop_gain_calibrated, 
            stop_loss_calibrated,
            opentop,
            threshold
        )
    return trades

def run_strat(stop_gain, stop_loss, threshold, opentop, df, start_time, end_time,daytrade_endtime,plot):
    ds_unique = df.date.unique()
    dss_df = ds_unique[:]
    dss = []
    for ds in dss_df:
        if ds >= start_time and ds <= end_time:
            dss.append(ds)
            
    trades = back_test(stop_gain, stop_loss, threshold, opentop, df, start_time, end_time, daytrade_endtime)
#     print(trades)

#     deal with loss trades
#     for ds,trade in trades.items():
#         if trade['pnl'] < 0:
#             print(trade)
#             plot_day_chart_multi(df, ds, trades)

    # these few lines plot chart in a day
#     for ds in dss:
#         print('plot date '+ds)
#         plot_day_chart_multi(df, ds, trades)
        
    stat = compute_stat(trades,plot,dss)
    stat = {
        # generaly information
        'days':len(dss),
        'start_time':start_time,
        'end_time':end_time,
        'opentop': opentop,
        'stop_loss': stop_loss,
        'stop_gain': stop_gain,
        
        # trading stat
        'avg_monthly_gain':stat['avg_monthly_gain'],
        'win_rate':stat['win_rate'],
        'win_rate_exclude_neutral':stat['win_rate_exclude_neutral'],
        'win':stat['win'],
        'lose':stat['lose'],
        'neutual':stat['neutual'],
        'pnl':stat['pnl'],
        'daily_balance_10_contract':stat['daily_balance_10_contract'],
        
#         over all gain 
        'pnl_ma_20_avg':stat['pnl_ma_20_avg'],
        # over all success rate
        'rate_ma_20_avg':stat['rate_ma_20_avg'],
         
        # gain consistency
        'pnl_ma_20_positive_rate':stat['pnl_ma_20_positive_rate'],
        # success rate consistency
        'rate_ma_20_positive_rate':stat['rate_ma_20_positive_rate'],
    }
    return stat
    
# future threshold = 0.025
# param: stop win, stop loss, threshold, open top?, stock data in df, start time, end time

# out1. MA x % above 0, over all monthly gain, win rate. MA 20 line
# out2: MA 20, 10, 5 x % above 0,  ma 20, 10, 5 line
