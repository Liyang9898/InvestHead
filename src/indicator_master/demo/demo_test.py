
from indicator_master.feature_lib.moving_window_indicator import metric_positive_rate_mw
from indicator_master.feature_lib.peak_over_x_days_max import peak_over_x_days
from indicator_master.feature_lib.velocity import get_velocity_pct_on_metric
import pandas as pd


path='D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/step3_add_indicator/ACA.csv'
path_out='D:/f_data/temp/ACA_test.csv'

df = pd.read_csv(path)

# metric up rate
metric_positive_rate_mw(df=df, metric='ema21_delta', window_size=5, feature_col='ema21_increase_rate_5bar')
metric_positive_rate_mw(df=df, metric='ema21_delta', window_size=10, feature_col='ema21_increase_rate_10bar')
metric_positive_rate_mw(df=df, metric='ma50_delta', window_size=5, feature_col='ma50_increase_rate_5bar')
metric_positive_rate_mw(df=df, metric='ma50_delta', window_size=10, feature_col='ma50_increase_rate_10bar')
metric_positive_rate_mw(df=df, metric='ma50_delta', window_size=90, feature_col='ma50_increase_rate_90bar')

# peak_over_x_days_max
peak_over_x_days(df=df, metric='ema21', lookback_range=40, feature_col='ema21_peak_over_x_days_40')
peak_over_x_days(df=df, metric='ma50', lookback_range=40, feature_col='ma50_peak_over_x_days_40')

#speed
get_velocity_pct_on_metric(df=df, metric='ema21', bar_range=2, feature_col='v_ema21_2')
get_velocity_pct_on_metric(df=df, metric='ema21', bar_range=3, feature_col='v_ema21_3')


df.to_csv(path_out, index=False)
