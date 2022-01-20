
from indicator_master.feature_lib.moving_window_indicator import metric_positive_rate_mw
from indicator_master.feature_lib.velocity import get_velocity_on_metric
import numpy as np
import pandas as pd


path='D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/step3_add_indicator/ACA.csv'
path_out='D:/f_data/temp/ACA_test.csv'

df = pd.read_csv(path)
print(df.columns)
# 'ema21_delta', 'ma50_delta',
metric='ema21'
window_size = 5
# feature_col = 'ema21_delta_uprate_mw5'
feature_col = 'ema21_v5'
# metric_positive_rate_mw(df, metric, window_size, feature_col)
get_velocity_on_metric(df, metric, window_size, feature_col)
# print(df[feature_col].to_list())

df.to_csv(path_out, index=False)
# for x in df[feature_col].to_list():
#     print(x)