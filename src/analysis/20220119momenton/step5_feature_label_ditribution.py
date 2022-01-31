import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate, \
    chart_positive_negative_distribution, feature_cumulative_cnt_win_rate


# feature_label_merge = 'D:/f_data/analysis/20220119_momenton/step4_added_label/GIS.csv'
feature_label_merge = 'D:/f_data/analysis/20220119_momenton/merged_feature_label.csv'

df = pd.read_csv(feature_label_merge)
print(len(df))

feature_list = [
    'ema21_increase_rate_5bar', # helpful, distinction not large
    'ema21_increase_rate_10bar',  # helpful, distinction not large
    'ma50_increase_rate_5bar', # no correlation at all
    'ma50_increase_rate_10bar',
    'ma50_increase_rate_90bar', # the higher the more likely to lose # need to see some example, more reverse?
    
    'ema21_peak_over_x_days_40', # obviously useful
    'ma50_peak_over_x_days_40', # no correlation at all
    
    'v_ema21_2', # obviously useful
    'v_ema21_3', # obviously useful
]


feature = 'v_ema21_2'
label = 'label'
bins = 40


# df = df[df[feature] < 0.02]


# chart_bucket_positive_rate(df, feature, label, bins, img_path='')
# chart_positive_negative_distribution(df, feature, label, bins, img_path='')

feature_cumulative_cnt_win_rate(df, feature, label)