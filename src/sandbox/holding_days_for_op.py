from datetime import datetime, timedelta 
from functools import reduce

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from trade_analysis_master.plot_lib.lib import time_range_gain, list_delta, \
    incremental, roll, ab_test
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
    t_20210425_ema21_ma50_gap_per_ticker_4p_out
)



    
# normal    
trade_path_base = t_20210420_ema21_ma50_gap_per_ticker
df_bases = pd.read_csv(trade_path_base + """merge/all_trades_all_entry.csv""")
print(df_bases['entry_ts'])
# # 4%
trade_path_4p =  t_20210425_ema21_ma50_gap_per_ticker_4p_out
df_4p = pd.read_csv(trade_path_4p + """merge/all_trades_all_entry.csv""")

print('==================================')

df_bases_win=df_bases[df_bases['pnl_percent']>0]
df_4p_win=df_4p[df_4p['pnl_percent']>0]

fig = go.Figure()
fig.add_trace(go.Histogram(x=df_bases_win['holding_days'],name='major'))
fig.add_trace(go.Histogram(x=df_4p_win['holding_days'],name='4p'))
fig.show()

df_bases_below90=df_bases[df_bases['holding_days']<90]
df_bases_below60=df_bases[df_bases['holding_days']<60]
df_bases_below30=df_bases[df_bases['holding_days']<30]
total = len(df_bases)
print(len(df_bases_below30)/total,len(df_bases_below60)/total,len(df_bases_below90)/total)


df_4p_below90=df_4p[df_4p['holding_days']<90]
df_4p_below60=df_4p[df_4p['holding_days']<60]
df_4p_below30=df_4p[df_4p['holding_days']<30]
total = len(df_4p)
print(len(df_4p_below30)/total,len(df_4p_below60)/total,len(df_4p_below90)/total)
