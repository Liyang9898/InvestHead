

from batch_20220207.batch_20220207_lib.constant import INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME
from batch_20220207.batch_20220207_lib.util_feature_threshold import merge_idc_trade_add_label, \
    compute_v_threshold_on_idc_trade_merged_data
import pandas as pd
from util.util_feature_visualization import chart_feature_cumulative_win_rate_sample_cnt, \
    BIG_EQ_FEATURE


ticker = 'AAPL'
output_path_all_entry = f'{RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}_all_entry.csv'


output_path_all_entry = f'{RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}_all_entry.csv'
file_path = f'{INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}.csv'

# merge trade and indicator, add labeling
df_idc = pd.read_csv(file_path)
df_trade = pd.read_csv(output_path_all_entry)

df_merge = merge_idc_trade_add_label(df_idc, df_trade)

# compute threshold
threshold = compute_v_threshold_on_idc_trade_merged_data(df_merge, ticker)
feature = 'v_ema21_3'
label = 'label'
chart_feature_cumulative_win_rate_sample_cnt(df=df_merge, feature=feature, label=label, direction_flag=BIG_EQ_FEATURE)
print(threshold)