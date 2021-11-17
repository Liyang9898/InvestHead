import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from plot.plot import plot_day_chart_multi
from plot.runner import run
from plot.util import win_rate_ma_multi_trade_a_day,pnltimeseries, plottimeseries,pnltotaltimeseries,pnldistribution,plotcategory,pnldistributionagg,plotpie,pnlma,plottimeseriesmultiline
from strat.replay_wrap import replay
from strat.replay2big import replay2big
from plot.stat import compute_stat
import numpy as np
import plotly.express as px
import time

def run_strat_bug_bar(stop_gain, stop_loss, threshold, opentop, df, start_time, end_time,plot,dynamic_stop,bigbarsize):
    ds_unique = df.date.unique()
    dss_df = ds_unique[:]
    dss = []
    for ds in dss_df:
        if ds >= start_time and ds <= end_time:
            dss.append(ds)

    trades = dict()
    df_one_days = dict()
    for ds in dss:
    #     print(ds)
        df_one_days[ds] = df.loc[((df['date']==ds) & (df['est_time'] < end_time)),:]
        

        stop_gain_calibrated=stop_gain
        stop_loss_calibrated=stop_loss
        if dynamic_stop:
            first_bar_close = df_one_days[ds].loc[df['est_time']=='09:30:00'].iloc[0]['close']
            stop_gain_dynamic = float(stop_gain)/3100*first_bar_close
            stop_loss_dynamic = float(stop_loss)/3100*first_bar_close
            stop_gain_calibrated=stop_gain_dynamic
            stop_loss_calibrated=stop_loss_dynamic
#             print(ds+'   '+str(first_bar_close)+'  '+str(stop_gain_dynamic))
        trades[ds] = replay2big(
            df_one_days[ds], 
            stop_gain_calibrated, 
            stop_loss_calibrated,
            bigbarsize
        )
        
    win_count = 0.0
    lose_count = 0.0  
    neutual_cnt = 0.0
    pnl = 0.0
    for ds in dss:
        for ts in trades[ds].keys():
            win_str = 'win'
            if trades[ds][ts]['pnl'] == 0:
                win_str = 'neutral'
                neutual_cnt = neutual_cnt + 1
            elif trades[ds][ts]['pnl'] < 0:
                win_str = 'lose'
                lose_count =lose_count + 1
            else:
                win_count =win_count + 1
            pnl = pnl + trades[ds][ts]['pnl']
            long_str = 'short'
            if trades[ds][ts]['is_long']:
                long_str = 'long'
              
            res_str = ds + '  ' + win_str + ' pnl:' + str(trades[ds][ts]['pnl'])
    #         print(res_str)
    win_rate = float(win_count) / (float(win_count) + float(lose_count)+float(neutual_cnt))
    win_rate_exclude_neutral = float(win_count) / (float(win_count) + float(lose_count))
    e_daily_10_contract = pnl / (float(win_count) + float(lose_count)+float(neutual_cnt)) / 2 *1000
    monthly = e_daily_10_contract * 20
#     print('win:' + str(win_count) + '  lose:' + str(lose_count) + '  neutual:' + str(neutual_cnt) + '  win_rate:' + str(win_rate) + '  pnl:' + str(pnl) + '  E_daily_10_contract:' + str(e_daily_10_contract) + '  monthly:' + str(monthly))
#     print(str(len(dss)) + ' days')
     
    # statprint
#     a = compute_stat(trades,plot)
    a = win_rate_ma_multi_trade_a_day(trades,20)
#     print(a)
    plottimeseries(a,'win_rate_ma20')
     
      
#     for ds in dss:
#     #     if trades[ds]['pnl'] > 0:
#             plot_day_chart_multi(df_one_days[ds],ds, [trades[ds]])
    # 
    # res = run(trades, 1000, 50000)
    # plottimeseries(res['balance'],'balance')
    # plottimeseries(res['contract'],'contract')
    # plottimeseries(res['daily_pnl'],'daily_pnl')
    stat = {
        'avg_monthly_gain':monthly,
        'win_rate':win_rate,
        'win_rate_exclude_neutral':win_rate_exclude_neutral,
        'days':len(dss),
        'win':win_count,
        'lose':lose_count,
        'neutual':neutual_cnt,
        'pnl':pnl,
        'daily_balance_10_contract':e_daily_10_contract
    }
    return stat
    
# future threshold = 0.025
# param: stop win, stop loss, threshold, open top?, stock data in df, start time, end time

# out1. MA x % above 0, over all monthly gain, win rate. MA 20 line
# out2: MA 20, 10, 5 x % above 0,  ma 20, 10, 5 line
