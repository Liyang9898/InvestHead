import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from plot.plot import plot_day_chart_multi
from strat.replay2big import replay2big

import numpy as np
import plotly.express as px
import time
# from stat import entry

# stop_loss = 0.2
# stop_gain = 0.1

bigbarsize = 0.2

timescope = '1min'
# timescope = '5min'
# opentop = True
opentop = False

scope_option = {
    '1min':{
        'path':["""D:/f_data/BATS_SPY_1min_1120_1224.csv""", """D:/f_data/BATS_SPY_1min_1223_0107.csv"""],
        'endtime':'10:30:00'
    },
    '5min':{
        'path':["""D:/f_data/BATS_SPY_5min.csv"""],
        'endtime':'11:30:00'
    }
}

end_time = scope_option[timescope]['endtime']
paths = scope_option[timescope]['path']

dfs = []
for path in paths:
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['time', 'open','high','low','close']
    )
    dfs.append(df)
df = pd.concat(dfs).drop_duplicates().reset_index(drop=True)
  
df['date']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d'), axis = 1)
df['est_time']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%H:%M:%S'), axis = 1)
 
ds_unique = df.date.unique()
dss = ds_unique[:]
print(dss)
# dss = ['2019-12-17']
trades = dict()
df_one_days = dict()
for ds in dss:
    df_one_days[ds] = df.loc[((df['date']==ds) & (df['est_time'] < '10:30:00')),:]
    trades[ds] = replay2big(df_one_days[ds],bigbarsize)



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
        pnl = pnl + trades[ds][ts]['pnl']  * 10
        long_str = 'short'
        if trades[ds][ts]['is_long']:
            long_str = 'long'
        
        res_str = ds + '  ' + win_str + ' pnl:' + str(trades[ds][ts]['pnl'] * 10)
#         print(res_str)
win_rate = float(win_count) / (float(win_count) + float(lose_count)+float(neutual_cnt))
e_daily_10_contract = pnl / len(dss) / 2 *1000
monthly = e_daily_10_contract * 20
# print('win:' + str(win_count) + '  lose:' + str(lose_count) + '  neutual:' + str(neutual_cnt) + '  win_rate:' + str(win_rate) + '  pnl:' + str(pnl) + '  E_daily_10_contract:' + str(e_daily_10_contract) + '  monthly:' + str(monthly))
# print(str(len(dss)) + " days")
# 
# for ds in dss:
#         plot_day_chart_multi(df_one_days[ds],ds, list(trades[ds].values()))