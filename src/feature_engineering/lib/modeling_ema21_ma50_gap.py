import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from version_master.version import (
    feature_engineering
)
from numpy import arange



def win_rate_under_threshold(features, threshold):
    feature_better_bucket = features[(features['gap_ema21_ma50'] >= threshold) & (features['gap_ema21_ma50'] <= 1)]
    features_positive_better_bucket = feature_better_bucket[feature_better_bucket['label'] == 1]
    features_negative_better_bucket = feature_better_bucket[feature_better_bucket['label'] == -1]
    win = len(features_positive_better_bucket)
    lose = len(features_negative_better_bucket)
    total = len(feature_better_bucket)
    if total == 0:
        return None
    win_percent = win/total
    lose_percent = lose/total
    win_rate = win_percent / total
    
    return {
        'win_rate': win_percent,
        'opportunity_remain': total/len(features),
        'threshold':threshold
    }


def fit(df):
    max_win_rate = 0
    max_perf = None
    for threshold in arange(0.0,0.5,0.001):
        performance = win_rate_under_threshold(df,threshold)

        if performance['win_rate'] > max_win_rate:
            max_perf = performance
            max_win_rate = performance['win_rate']
        if performance['opportunity_remain'] < 0.33:
            break
    return max_perf


def eval(df, threshold):
    perf = win_rate_under_threshold(df, threshold)
    return perf


# df = pd.read_csv(feature_engineering+'features.csv')
# model = fit(df)
# print(model)
# eval_res = eval(df, 0.039)
# print(eval_res)
