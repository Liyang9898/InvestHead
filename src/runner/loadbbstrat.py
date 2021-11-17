import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from plot.plot_indicator import plot_chart_indi, plot_ma_bb,bbpabs,validpoint,validlongplot,validshortplot,normalize_ma_in_bb
from plot.util import pnltimeseries, plottimeseries,pnltotaltimeseries,pnldistribution,plotcategory,pnldistributionagg,plotpie
from strat.replay_wrap import replay
# from strat.replay_32 import replay_32
from strat.replay_xxtill import replay_xxtill
import numpy as np
import plotly.express as px
import time

stop_loss = 0.3
stop_gain = 0.3
# timescope = '1min'
timescope = '5min_es'
opentop = True
# opentop = False

scope_option = {
    '1min':{
        'path':"""D:/f_data/BATS_SPY_1min.csv""",
        'endtime':'10:30:00'
    },
    '5min':{
        'path':"""D:/f_data/BATS_SPY_5min.csv""",
        'endtime':'11:30:00'
    },
    '5min_es':{
        'path':"""D:/f_data/CME_MINI_DL_ES1_5min.csv""",
        'endtime':'11:30:00'
    }
}

end_time = scope_option[timescope]['endtime']
path = scope_option[timescope]['path']

df = pd.read_csv(
    path,
    sep=',',
    header=0,
    names=['time', 'open','high','low','close','bb_base','bb_up','bb_low','ma21','ma8','ma17','bb']
)


df['date']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d'), axis = 1)
df['est_time']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%H:%M:%S'), axis = 1)
df['ma17_nor']=df.apply(lambda row : normalize_ma_in_bb(row['bb_up'], row['bb_low'], row['ma17']), axis = 1)
df['bbvalid']=df.apply(lambda row : validpoint(row['ma8'], row['ma21'], row['ma17_nor'], row['bb']), axis = 1)
df['validlongplot']=df.apply(lambda row : validlongplot(row['bbvalid'], row['close']), axis = 1)
df['validshortplot']=df.apply(lambda row : validshortplot(row['bbvalid'], row['close']), axis = 1)

# 
print(df)
  
ds_unique = df.date.unique()
dss = ds_unique[:]
 
# plot_chart_indi(df)
print(dss)
dss = ['2020-01-06']
trades = dict()
df_one_days = dict()
for ds in dss:
    df_one_days[ds] = df.loc[((df['date']==ds)),:]
    plot_chart_indi(df_one_days[ds],ds)
    plot_ma_bb(df_one_days[ds],ds)
#     
# win_count = 0.0
# lose_count = 0.0  
# neutual_cnt = 0.0
# pnl = 0.0
# for ds in dss:
#     win_str = 'win'
#     if trades[ds]['pnl'] == 0:
#         win_str = 'neutral'
#         neutual_cnt = neutual_cnt + 1
#     elif trades[ds]['pnl'] < 0:
#         win_str = 'lose'
#         lose_count =lose_count + 1
#     else:
#         win_count =win_count + 1
#     pnl = pnl + trades[ds]['pnl']  * 10
#     long_str = 'short'
#     if trades[ds]['is_long']:
#         long_str = 'long'
#     
#     res_str = ds + '  ' + win_str + ' pnl:' + str(trades[ds]['pnl'] * 10)
#     print(res_str)
# win_rate = float(win_count) / (float(win_count) + float(lose_count)+float(neutual_cnt))
# e_daily_10_contract = pnl / (float(win_count) + float(lose_count)+float(neutual_cnt)) / 2 *1000
# monthly = e_daily_10_contract * 20
# print('win:' + str(win_count) + '  lose:' + str(lose_count) + '  neutual:' + str(neutual_cnt) + '  win_rate:' + str(win_rate) + '  pnl:' + str(pnl) + '  E_daily_10_contract:' + str(e_daily_10_contract) + '  monthly:' + str(monthly))
# print(str(len(dss)) + ' days')
# 
# # statprint
# # pnldic = pnltimeseries(trades)
# # pnlaggdic = pnltotaltimeseries(trades)
# # plottimeseries(pnldic)
# # plottimeseries(pnlaggdic)
# # dis = pnldistribution(trades)
# # disagg = pnldistributionagg(trades)
# # # plotcategory(dis)
# # # plotcategory(disagg)
# # plotpie(dis, 'change')
# # plotpie(disagg, 'amount of money')
# 
# 
# # 
# for ds in dss:
# #     if trades[ds]['pnl'] < 0:
#         plot_day_chart_multi(df_one_days[ds],ds, [trades[ds]])