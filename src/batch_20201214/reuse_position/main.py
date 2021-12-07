'''
Created on Mar 2, 2021

@author: leon
'''
from batch_20201214.reuse_position.reuse_position_lib import reuse_position_cash_history
from version_master.version import (
    indicator_20210301, 
    trade_swing_2150in_2150out_20210302_iwf_channel,
    trade_swing_2150in_2150out_20210227_iwf,
    trade_swing_2150in_2150out_20210302_iwf_trend_start
)

trade_path = trade_swing_2150in_2150out_20210302_iwf_channel + 'detail/'

# example one, old batch
# reuse_position_cash_history(
#     start_date="2016-01-01",
#     end_date="2020-12-31",
#     trade_folder = trade_path,
#     output_folder = 'D:/f_data/temp/re/',
#     indicator_folder = indicator_20210301,
# )


# example two 20211116 batch
reuse_position_cash_history(
    start_date='2006-01-01',
    end_date='2022-01-01',
    trade_folder = "D:/f_data/batch_20211116/step4_gen_trades/",
    output_folder = 'D:/f_data/temp/re/',
    indicator_folder = "D:/f_data/batch_20211116/step3_add_indicator/",
)
