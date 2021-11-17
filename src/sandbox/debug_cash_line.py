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



trade_path=t_20210425_ema21_ma50_gap_per_ticker_4p_out
# trade_path=t_20210420_ema21_ma50_gap_per_ticker
price_in_track_path = trade_path + """merge/cash_history_reuse_trades_in_track.csv"""

all_trade_df = pd.read_csv(price_in_track_path)
i_trade_df = all_trade_df[all_trade_df['track_id']==0]
i_trade_df.to_csv('D:/f_data/temp/a1.csv')
g2 = i_trade_df.groupby( ["ticker"] ).count()
print(g2)
# print(i_trade_df)


#figure
fig = go.Figure()
fig.add_trace(go.Scatter(x=i_trade_df['entry_ts'], y=i_trade_df['pnl_percent'],mode='lines+markers',name='pnl_percent'))
fig.add_trace(go.Scatter(x=i_trade_df['entry_ts'], y=i_trade_df['position'],mode='lines+markers',name='position'))
fig.show()
 
# fig2 = go.Figure()
# fig2.add_trace(go.Scatter(x=i_trade_df['entry_ts'], y=i_trade_df['pnl_percent'],mode='lines+markers',name='position'))
fig2 = px.scatter(i_trade_df, x="exit_ts", y="position", color="ticker")
fig2.show()

price_in_track_path = trade_path + """merge/cash_history_reuse_price_in_track.csv"""
all_price_df = pd.read_csv(price_in_track_path)
i_price_df = all_price_df[all_price_df['track_id']==0]
g1 = i_price_df.groupby( ["ticker"] ).count()
print(g1)
i_price_df.to_csv('D:/f_data/temp/a2.csv')
# print(i_price_df)
fig3 = px.scatter(i_price_df, x="date", y="price", color="ticker")
# fig3 = go.Figure()
# fig3.add_trace(go.Scatter(x=i_price_df['date'], y=i_price_df['price'],color="ticker",mode='lines+markers',name='position'))
fig3.show()


path = 'D:/f_data/temp/cashline_0.csv'
line0 = pd.read_csv(path)
# fig3 = go.Figure()
# fig3.add_trace(go.Scatter(x=line0['date'], y=line0['cash_roll'],mode='lines+markers',name='position'))
# fig3.show()