import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate


# feature_label_merge = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label_merge.csv'
feature_label_merge = 'D:/f_data/analysis/20220119_momenton/step4_added_label/ACC.csv'
feature_label_merge = 'D:/f_data/analysis/20220119_momenton/merged_feature_label.csv'

df = pd.read_csv(feature_label_merge)
print(len(df))


#     metric_positive_rate_mw(df=df, metric='ema21_delta', window_size=5, feature_col='ema21_increase_rate_5bar')
#     metric_positive_rate_mw(df=df, metric='ema21_delta', window_size=10, feature_col='ema21_increase_rate_10bar')
#     metric_positive_rate_mw(df=df, metric='ma50_delta', window_size=5, feature_col='ma50_increase_rate_5bar')
#     metric_positive_rate_mw(df=df, metric='ma50_delta', window_size=10, feature_col='ma50_increase_rate_10bar')
#     metric_positive_rate_mw(df=df, metric='ma50_delta', window_size=90, feature_col='ma50_increase_rate_90bar')
#     
#     # peak_over_x_days_max
#     peak_over_x_days(df=df, metric='ema21', lookback_range=40, feature_col='ema21_peak_over_x_days_40')
#     peak_over_x_days(df=df, metric='ma50', lookback_range=40, feature_col='ma50_peak_over_x_days_40')
#     
#     #speed
#     get_velocity_pct_on_metric(df=df, metric='ema21', bar_range=2, feature_col='v_ema21_2')
#     get_velocity_pct_on_metric(df=df, metric='ema21', bar_range=3, feature_col='v_ema21_3')
#     
#     # next bar date
#     next_bar_date(df, date_col='date', feature_col='next_bar_date')
    
    
feature_list = [
    'ema21_increase_rate_5bar', 
    'ema21_increase_rate_10bar', 
    'ma50_increase_rate_5bar',
    'ma50_increase_rate_10bar',
    'ma50_increase_rate_90bar',
    
    'ema21_peak_over_x_days_40',
    'ma50_peak_over_x_days_40',
    
    'v_ema21_2',
    'v_ema21_3',
]


feature = 'ma50_increase_rate_90bar'
label = 'label'
bins = 40

print(df)


chart_bucket_positive_rate(df, feature, label, bins, img_path='')