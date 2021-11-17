'''
Created on Dec 24, 2020

@author: leon
'''
from batch_20201214.batch_trade_lib import batch_trade_lopper

#path
folder_path_trade_results = "D:/f_data/sweep_20201214/yahoo_stock_trades_ma8_21_no_profit_manage/"
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/yahoo_stock_indicator_batch/"
#strat
ma = "8_21"
strategy_param_bundle={
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":1,
    "stop_profit_enable":1,
    "stop_profit_percent":0.005,
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
