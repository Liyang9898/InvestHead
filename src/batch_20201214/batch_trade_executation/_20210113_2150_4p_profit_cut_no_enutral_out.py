'''
Created on Jan 13, 2021

@author: leon
'''

from batch_20201214.batch_trade_lib import batch_trade_lopper
from batch_20201214.util_for_batch.batch_util import get_ticker_list

#path
folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210113_2150_4p_profit_cut_no_enutral_out/"
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/indicator_stock_20210106/"
ticker_list = "D:/f_data/sweep_20201214/conclusion_filtered/20200113_filter_vol_1m_cap_03b_80winrate_10trade.csv"

ticker_list = get_ticker_list(ticker_list, 'ticker')
print(ticker_list)
#strat
ma = "21_50"
strategy_param_bundle={
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.04,    
}
#time
start_time="2016-01-01 20:00:00"
end_time="2020-12-31 19:00:00"

############################################source region start#############################################   
batch_trade_lopper(
    folder_path_price_with_indicator, 
    folder_path_trade_results, 
    ma, 
    strategy_param_bundle,
    start_time,
    end_time,
    ticker_list=ticker_list
)
