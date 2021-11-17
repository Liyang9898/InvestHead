'''
Created on Dec 24, 2020

@author: leon
'''
from batch_20201214.batch_trade_lib import batch_trade_lopper

#path
folder_path_trade_results = "D:/f_data/sweep_20201214/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210108/"
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/indicator_stock_20210106/"
#strat
ma = "21_50"
strategy_param_bundle={
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
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
    end_time
)
