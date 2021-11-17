'''
Created on Dec 25, 2020

@author: leon
'''
'''
Created on Dec 25, 2020

@author: leon
'''
import pandas as pd

from plotting_lib.simple import plotTimeSerisDic,plotTimeSerisDic3 
from batch_20201214.cash_history_lib import gen_cash_history


#strat
ma = "21_50"
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


cash_history=gen_cash_history('FB',ma,strategy_param_bundle,start_time,end_time)
print(cash_history)
plotTimeSerisDic3(cash_history['price_position'],cash_history['cash_rollover_position'],cash_history['cash_fixed_base_position'])