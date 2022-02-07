import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate, \
    chart_positive_negative_distribution, get_df_feature_cumulative_cnt_win_rate, \
    chart_feature_cumulative_win_rate_sample_cnt, BIG_EQ_FEATURE, \
    SMALL_EQ_FEATURE


feature_label_merge = 'D:/f_data/analysis/20220119_momenton/step4_added_label/TYL.csv'
# feature_label_merge = 'D:/f_data/analysis/20220119_momenton/merged_feature_label.csv'

df = pd.read_csv(feature_label_merge)

feature_list = [
    'ema21_increase_rate_5bar', # helpful, distinction not large
    'ema21_increase_rate_10bar',  # helpful, distinction not large
    'ma50_increase_rate_5bar', # no correlation at all
    'ma50_increase_rate_10bar',
    'ma50_increase_rate_90bar', # the higher the more likely to lose # need to see some example, more reverse?
    
    'ema21_peak_over_x_days_40', #  useful between 0-4 on all stock, but no correlation on individual
    'ma50_peak_over_x_days_40', # no correlation at all
    
    'v_ema21_2', # obviously useful
    'v_ema21_3', # obviously useful
]


feature = 'v_ema21_3'
label = 'label'
bins = 40


# df = df[df[feature] < 0.02]


chart_bucket_positive_rate(df, feature, label, bins, img_path='')
# chart_positive_negative_distribution(df, feature, label, bins, img_path='')

chart_feature_cumulative_win_rate_sample_cnt(df=df, feature=feature, label=label, direction_flag=BIG_EQ_FEATURE)