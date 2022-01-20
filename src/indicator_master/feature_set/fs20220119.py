from indicator_master.feature_lib.date_feature import next_bar_date
from indicator_master.feature_lib.moving_window_indicator import metric_positive_rate_mw
from indicator_master.feature_lib.peak_over_x_days_max import peak_over_x_days
from indicator_master.feature_lib.velocity import get_velocity_pct_on_metric


def feature_set_20220119(df):
    """
    -ema21, ma5 increase rate in past 5, 10 days
    -ema21, ma5 peak in for past x days
    -velocity of ema21 over 2,3 bars gaps
    -next date
    """
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
    
    # next bar date
    next_bar_date(df, date_col='date', feature_col='next_bar_date')
    
    return df
    
