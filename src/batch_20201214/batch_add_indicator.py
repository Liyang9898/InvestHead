'''
Created on Dec 14, 2020

@author: leon
'''

import os

from batch_20201214.indicator_lib.lib import batch_indicator, \
    build_indicator_collection
from batch_20201214.util_for_batch.batch_util import get_all_files
import pandas as pd
from version_master.version import indicator_20210408, iwf


# ticker list
ticker_list_df = pd.read_csv(iwf)
ticker_list = ticker_list_df['ticker'].to_list()
print(len(ticker_list))

folder_path_raw_price_formated = "D:/f_data/sweep_20201214/format_stock_20210106/"
folder_path_price_with_indicator = indicator_20210408
start_time="1991-01-31 20:00:00"
end_time="2020-12-31 19:00:00"
    
batch_indicator(
    folder_path_price_with_indicator, 
    folder_path_raw_price_formated, 
    start_time, 
    end_time,
    ticker_list=ticker_list
)



# print('merging indicator')
# build_indicator_collection(folder_path_price_with_indicator)