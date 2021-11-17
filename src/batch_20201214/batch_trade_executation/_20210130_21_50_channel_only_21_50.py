'''
Created on Jan 13, 2021

@author: leon
'''

from batch_20201214.batch_trade_lib import batch_trade_lopper
from batch_20201214.util_for_batch.batch_util import get_ticker_list
from strategy_lib.stratage_param import strat_param_channel_only_50in75out_21_50

#path
folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210130_21_50_channel_only/"
folder_path_price_with_indicator = "D:/f_data/sweep_20201214/indicator_stock_20210129/"
ticker_list = "D:/f_data/sweep_20201214/conclusion_filtered/20200113_filter_vol_1m_cap_03b_80winrate_10trade.csv"

ticker_list = get_ticker_list(ticker_list, 'ticker')
print(ticker_list)
#strat
ma = "21_50"
strategy_param_bundle=strat_param_channel_only_50in75out_21_50
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
    ticker_list=None
)
