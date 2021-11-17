'''
Created on Jan 13, 2021

@author: leon
'''

from batch_20201214.batch_trade_lib import batch_trade_lopper
from batch_20201214.util_for_batch.batch_util import get_ticker_list
from strategy_lib.stratage_param import strat_param_swing_2150in_821out
import pandas as pd
from version_master.version import (
    indicator_20210226,
    trade_swing_2150in_821out_20210226_iwf,
    iwf
#     russell1000_plus_iwf_amend
) 


#path output
folder_path_trade_results = trade_swing_2150in_821out_20210226_iwf + "summary/"
trade_detail_path = trade_swing_2150in_821out_20210226_iwf + "detail/"

#path input
folder_path_price_with_indicator = indicator_20210226
ticker_list_path = iwf

# ticker list
ticker_list_df = pd.read_csv(ticker_list_path)
ticker_list = ticker_list_df['ticker'].to_list()


print(len(ticker_list))
#strat
ma = "21_50"
strategy_param_bundle=strat_param_swing_2150in_821out
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
