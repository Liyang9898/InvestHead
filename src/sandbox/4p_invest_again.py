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
    t_20210425_ema21_ma50_gap_per_ticker_4p_out,
    t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage
    
)

path = t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage + 'merge/all_trades_all_entry.csv'
print(path)
df = pd.read_csv(path)
df_win = df[df['pnl_percent'] > 0]
df_lose = df[df['pnl_percent'] < 0]

fig = go.Figure()
fig.add_trace(go.Histogram(
    x=df['best_potential_pnl_percent'],
    histnorm='percent',
    xbins=dict( # bins used for histogram
        start=0.0,
        end=1.0,
        size=0.01
    ),
    opacity=0.75
))
fig.show()