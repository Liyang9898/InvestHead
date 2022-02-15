from batch_20220207.batch_20220207_lib.constant import BASE_PATH
import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate, \
    chart_feature_cumulative_win_rate_sample_cnt, BIG_EQ_FEATURE


path_all = BASE_PATH + 'all_idc_trade.csv'


df = pd.read_csv(path_all)
print(len(df))



feature = 'v_ema21_3'
label = 'label'
bins = 40

df = df[df[feature] < 0.02]

chart_bucket_positive_rate(df, feature, label, bins, img_path='')
# chart_positive_negative_distribution(df, feature, label, bins, img_path='')

chart_feature_cumulative_win_rate_sample_cnt(df=df, feature=feature, label=label, direction_flag=BIG_EQ_FEATURE)
# print(threshold)