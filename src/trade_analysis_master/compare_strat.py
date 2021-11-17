'''
Created on Feb 27, 2021

@author: leon
'''
from version_master.version import (
 
    trade_swing_2150in_2150out_20210313_iwf,
    trade_swing_2150in_2150out_20210313_iwf_channel_in,
    trade_swing_2150in_2150out_20210313_iwf_50up,
    trade_swing_2150in_2150out_20210313_iwf_50down,
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
    t_20210518_ema21_ma50_gap_per_ticker_6p_out,
    t_20210518_ema21_ma50_gap_per_ticker_8p_out,
    t_20210518_ema21_ma50_gap_per_ticker_10p_out,
    t_20210518_ema21_ma50_gap_per_ticker_12p_out,
    t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage
)
import pandas as pd

trade_list = [
    
#     trade_swing_2150in_2150out_20210313_iwf, 
#     trade_swing_2150in_2150out_20210313_iwf_50up,
# #     t_20210314_iwf_ma50up_channel_out,
# #     t_20210314_iwf_ma50up_channel_inout,
#     t_20210321_myswing_20210321,
#     t_20210321_myswing,
#     t_20210404_myswing,
#     t_20210404_myswing_4percent_out,
#     t_20210418_myswing
#     t_20210420_ema21_ma50_gap_per_ticker,

    t_20210511_ema21_ma50_gap_per_ticker_3p_out,
    t_20210425_ema21_ma50_gap_per_ticker_4p_out,
    t_20210518_ema21_ma50_gap_per_ticker_6p_out,
    t_20210518_ema21_ma50_gap_per_ticker_8p_out,
    t_20210518_ema21_ma50_gap_per_ticker_10p_out,
    t_20210518_ema21_ma50_gap_per_ticker_12p_out,
    t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage,    
]

dfs = []
for trade in trade_list:
    path = trade + 'merge/strat_conclusion.csv'
    df = pd.read_csv(path)
#     tokens = trade.split('/')
    
    df['strategy'] = trade
    dfs.append(df)

#     print(tokens)
    
df_merged = pd.concat(dfs)    
df_merged.to_csv("D:/f_data/sweep_20201214/compare_strat/gradually_increase_profit_threshold.csv", index=False)