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


def plot_pnl_distribution(x0,x1):
#     fig = px.histogram(df, x="pnl_percent",range_x=[-0.2, 0.2])
#     fig.show()
    
#     x0 = np.random.randn(500)
#     # Add 1 to shift the mean of the Gaussian distribution
#     x1 = np.random.randn(500) + 1
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0))
    fig.add_trace(go.Histogram(x=x1))
    
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    fig.show()
        
    
# normal    
trade_path_base = t_20210420_ema21_ma50_gap_per_ticker
df_bases = pd.read_csv(trade_path_base + """merge/all_trades_all_entry.csv""")
print(df_bases['entry_ts'])
# # 4%
# trade_path =  t_20210425_ema21_ma50_gap_per_ticker_4p_out
# df = pd.read_csv(trade_path + """merge/all_trades_all_entry.csv""")

print('==================================')
total = len(df_bases)
df_lose = df_bases[df_bases['pnl_percent']<0]
df_0_to_4p=df_bases[(df_bases['pnl_percent']>0) & (df_bases['pnl_percent']<=0.04111)]
df_above_4p=df_bases[df_bases['pnl_percent']>0.04111]
print(total, len(df_lose), len(df_0_to_4p),len(df_above_4p))
print(len(df_lose)/total, len(df_0_to_4p)/total,len(df_above_4p)/total)

# fig = px.histogram(df_bases, x="pnl_percent",histnorm='probability density')
# fig.show()

p1 = df_0_to_4p['pnl_percent'].sum()
p2 = df_above_4p['pnl_percent'].sum()
print(p1,p2,p1+p2)
print('==================================')
# 
# # print(len(df))
# df_4p=df[(df['pnl_percent']<0.040001) & (df['pnl_percent']>0.03999)]
# df_not4p=df[(df['pnl_percent']>0.040001) | (df['pnl_percent']<0.03999)]
# 
# df_lose=df[df['pnl_percent']<0]
# df_lose_base=df_bases[df_bases['pnl_percent']<0]
# 
# df_base_below_4p=df_bases[(df_bases['pnl_percent']<0.03999) & (df_bases['pnl_percent']>0.0)]
# df_base_above_4p=df_bases[df_bases['pnl_percent']>0.04001]
# 
# print(len(df_4p)/len(df))
# print(len(df_not4p)/len(df))
# print(len(df_lose)/len(df))
# print(len(df_base_below_4p)/len(df_bases))
# print(len(df_base_above_4p)/len(df_bases))
# 
# 
# 
# df_win=df[df['pnl_percent']>0]
# df_lose=df[df['pnl_percent']<0]
# df_neutral=df[df['pnl_percent']==0]
# assert len(df_win)+len(df_lose)+len(df_neutral)==len(df)
# print(df_win['pnl_percent'].mean(),df_lose['pnl_percent'].mean(),df_neutral['pnl_percent'].mean())
# 
# df_base_win=df_bases[df_bases['pnl_percent']>0]
# df_base_lose=df_bases[df_bases['pnl_percent']<0]
# df_base_neutral=df_bases[df_bases['pnl_percent']==0]
# assert len(df_base_win)+len(df_base_lose)+len(df_base_neutral)==len(df_bases)
# print(df_base_win['pnl_percent'].mean(),df_base_lose['pnl_percent'].mean(),df_base_neutral['pnl_percent'].mean())
# # plot_pnl_distribution(df_lose['pnl_percent'].to_list(),df_lose_base['pnl_percent'].to_list())
# 
# 
# price_in_track_path = trade_path + """merge/cash_history_reuse_trades_in_track.csv"""
# print(price_in_track_path)
# cash_df = pd.read_csv(price_in_track_path)
# print(cash_df)
# cash_dfs= {}
# for i in range(0,49):
#     cash_dfs[i] = cash_df[cash_df['track_id']==i]
# 
# # cash_df_i=cash_dfs[3]
# # cash_df_i_part = cash_df_i[['entry_ts','pnl_percent','ticker']]
# # print(cash_df_i_part)
# # cash_df_i_part.to_csv('D:/f_data/temp/a.csv', index=False)
# # fig = px.bar(cash_df_i, x='entry_ts', y='pnl_percent')
# # fig.show()
# 
# def get_cash_line(df):
#     df_sorted = df.sort_values(by=['entry_ts']).reset_index()
#     print(df_sorted)
#     pos = 1
#     df_sorted['position']=1
#     for i in range(0,len(df_sorted)):
#         factor = 1+df_sorted.loc[i,'pnl_percent']
#         pos *= factor
#         df_sorted.loc[i,'position'] = pos
# #         print(df_sorted.loc[i,'entry_ts'],factor,pos)
#     return df_sorted
# # df_with_pos = get_cash_line(cash_df_i_part)
# # print(df_with_pos)
# # 
# # 
# # final_pos = df_with_pos.loc[len(df_with_pos)-1,'position']
# # print(final_pos)
# 
# for i in range(0,50):
#     cash_df_i=cash_dfs[i]
#     cash_df_i_part = cash_df_i[['entry_ts','pnl_percent','ticker']]
#     cash_df_i_part_pos = get_cash_line(df)
#     final_pos = cash_df_i_part_pos.loc[len(cash_df_i_part_pos)-1,'position']
#     print(final_pos)