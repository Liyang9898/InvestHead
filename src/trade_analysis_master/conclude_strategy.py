'''
Created on Feb 21, 2021

@author: leon
'''

from trade_analysis_master.concat_lib.helper import all_in_trade_conclude 
from version_master.version import (
    indicator_20210408,
    meta_20210117,
     
    trade_swing_2150in_2150out_20210313_iwf,
    trade_swing_2150in_2150out_20210313_iwf_channel_in,
     
    trade_swing_2150in_2150out_20210313_iwf_50up,
#     trade_swing_2150in_2150out_20210313_iwf_50down,
    t_20210314_iwf_ma50up_channel_out,
    t_20210314_iwf_ma50up_channel_inout,
    t_20210321_myswing_20210321,
    t_20210321_myswing,
    t_20210404_myswing_4percent_out,
    t_20210404_myswing,
    t_20210408_myswing,
    t_20210418_myswing,
    t_20210420_ema21_ma50_gap_per_ticker,
    t_20210425_ema21_ma50_gap_per_ticker_4p_out,
    t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage,
    t_20210511_ema21_ma50_gap_per_ticker_3p_out,
    
    t_20210518_ema21_ma50_gap_per_ticker_6p_out,
    t_20210518_ema21_ma50_gap_per_ticker_8p_out,
    t_20210518_ema21_ma50_gap_per_ticker_10p_out,
    t_20210518_ema21_ma50_gap_per_ticker_12p_out
)
  
  
 
trade_path = t_20210425_ema21_ma50_gap_per_ticker_4p_out
indicator_path = indicator_20210408
  
start_time="2016-01-01 20:00:00"
end_time="2020-12-31 19:00:00"
meta = meta_20210117
  
dic = all_in_trade_conclude(
    trade_path, 
    indicator_path,
    start_time,
    end_time,
    meta
)
   
for k,v in dic.items():
    print(k,v)
#      

