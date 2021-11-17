'''
Created on Jan 13, 2021

@author: leon
'''

from batch_20201214.batch_trade_lib import batch_trade_lopper
from batch_20201214.util_for_batch.batch_util import get_ticker_list
from strategy_lib.stratage_param import ribbon_start
import pandas as pd

#path output
folder_path_trade_results = "D:/f_data/sweep_20201214/trade_summary/20210213_swing_iwf_only/"
trade_detail_path = "D:/f_data/sweep_20201214/trades/20210213_swing_iwf_only/"

#path input
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/indicator/2021-02-09/"
ticker_list_path = "D:/f_data/sweep_20201214/white_list/20210117_2b_1m_10trade_60win_positive_iwf_200.csv"



ticker_list_df = pd.read_csv(ticker_list_path)
ticker_list = ticker_list_df['ticker'].to_list()

# ticker_list = get_ticker_list(ticker_list, 'ticker')
print(ticker_list)
print(len(ticker_list))
#strat
ma = "21_50"
strategy_param_bundle=ribbon_start
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
    ticker_list=ticker_list
)
