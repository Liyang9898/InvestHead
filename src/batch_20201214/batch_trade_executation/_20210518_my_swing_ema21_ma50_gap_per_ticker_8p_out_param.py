'''
Created on Jan 13, 2021

@author: leon
'''

from batch_20201214.batch_trade_lib import batch_trade_lopper
# from batch_20201214.util_for_batch.batch_util import get_ticker_list
from strategy_lib.stratage_param import strat_param_swing_2150in_2150out_ma_gap_8p_out
import pandas as pd
from version_master.version import (
    indicator_20210408,
    t_20210518_ema21_ma50_gap_per_ticker_8p_out,
    swing_set1,
) 

################################### 4 things to adjust#####################################
################################### 4 things to adjust#####################################
trader_folder = t_20210518_ema21_ma50_gap_per_ticker_8p_out
indicator_folder = indicator_20210408
ticker_set = swing_set1
strategy_param_bundle=strat_param_swing_2150in_2150out_ma_gap_8p_out
################################### 4 things to adjust#####################################
################################### 4 things to adjust#####################################

#path output
folder_path_trade_results = trader_folder + "summary/"
trade_detail_path = trader_folder + "detail/"

#path input
folder_path_price_with_indicator = indicator_folder
ticker_list_path = ticker_set

# ticker list
ticker_list_df = pd.read_csv(ticker_list_path)
ticker_list = ticker_list_df['ticker'].to_list()

# test sample overide
# ticker_list=['AAPL']

print(len(ticker_list))
#strat
ma = "21_50"

#time
start_time="2016-01-01 20:00:00"
end_time="2020-12-31 19:00:00"

############################################source region start#############################################   
batch_trade_lopper(
    folder_path_price_with_indicator, 
    folder_path_trade_results, 
    trade_detail_path,
    ma, 
    strategy_param_bundle,
    start_time,
    end_time,
    ticker_list = ticker_list
)
