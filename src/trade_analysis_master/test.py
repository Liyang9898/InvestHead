'''
Created on Feb 27, 2021

@author: leon
'''
import pandas as pd
from trade_analysis_master.concat_lib.concat_trades_details import join_trades_with_indicator
from trade_analysis_master.concat_lib.summary_process_lib import conclude_summary2
# from trade_analysis_master.concat_lib.trade_plus_indicator import build_indicator_collection, \
#     make_feature_table_base
from version_master.version import (
    trade_swing_2150in_821out_20210226_iwf,
    trade_swing_2150in_850out_20210227_iwf,
    trade_swing_2150in_2150out_20210227_iwf,
    meta_20210117,
    indicator_20210301,
    trade_swing_2150in_2150out_20210313_iwf,
    trade_swing_2150in_2150out_20210313_iwf_channel_in
)


#  
# # conclude_summary2(trade_swing_2150in_2150out_20210227_iwf)
# path_in = "D:/f_data/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_in/merge/cash_history_reus_price_in_track.csv"
# path_out= "D:/f_data/sweep_20201214/trades/2150in_2150out_20210310_iwf_channel_in/merge/reuse_daily_position_cnt.csv"
# def get_daily_position_cnt(path_in, path_out):
#     df = pd.read_csv(path_in)
#     daily_position_cnt = df.groupby('date').size().to_frame(name = 'position_cnt').reset_index()
#     daily_position_cnt.to_csv(path_out, index=False)
# 
# get_daily_position_cnt(path_in, path_out)
# est_datetime
# indicator_folder = indicator_20210301
# output_path = 'D:/test_indic.csv'
# ticker_list = ['AAPL', 'Z']
# build_indicator_collection(ticker_list, indicator_folder, output_path)
# 
# output_path2 = 'D:/test_trade_indic.csv'
# trade_path = 'D:/f_data/sweep_20201214/trades/20210313_2150in_2150out_iwf_channel_in/merge/all_trades_all_entry.csv'
# join_trades_with_indicator(trade_path, output_path, output_path2)



trade_path = trade_swing_2150in_2150out_20210313_iwf_channel_in

all_entry_trade_path = trade_path + 'merge/all_trades_all_entry.csv'
all_indicator_path = indicator_20210301 + 'merge/all_indicator.csv'
feature_table = trade_path + 'merge/features.csv'
 
join_trades_with_indicator(all_entry_trade_path, all_indicator_path, feature_table)