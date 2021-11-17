import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from version_master.version import (
    feature_engineering
)

    
def exitable_after_ma50_negative_win_rate_improve():
    path=feature_engineering+'features.csv'
    
    # original
    features = pd.read_csv(path)
    features_positive = features[features['label'] == 1]
    features_negative = features[features['label'] == -1]
    win = len(features_positive)
    lose = len(features_negative)
    total = len(features)
    win_percent = win/total
    lose_percent = lose/total
    print(win_percent, lose_percent)
    
    # filter
    neutral_in_features_positive = features[(features['label'] == 1) & (features['exitable_after_ma50_negative'] == 1)]
    neutral_in_features_negative = features[(features['label'] == -1) & (features['exitable_after_ma50_negative'] == 1)]
    neutral_in_features_positive_cnt = len(neutral_in_features_positive)
    neutral_in_features_negative_cnt = len(neutral_in_features_negative)
    neutral_in_positive = neutral_in_features_positive_cnt/total
    neutral_in_negative = neutral_in_features_negative_cnt/total
    print('neutral from positive and negative:', neutral_in_positive, neutral_in_negative)
    
    print(win_percent-neutral_in_positive,neutral_in_positive,neutral_in_negative,lose_percent-neutral_in_negative)
    print('new win rate:',(win_percent-neutral_in_positive)/(lose_percent-neutral_in_negative+(win_percent-neutral_in_positive)))
    

def entry_ma50_ema21_improve():
    path=feature_engineering+'features.csv'
    
    # original
    features = pd.read_csv(path)
    features_positive = features[features['label'] == 1]
    features_negative = features[features['label'] == -1]
    win = len(features_positive)
    lose = len(features_negative)
    total = len(features)
    win_percent = win/total
    lose_percent = lose/total
    print(win_percent, lose_percent)
    
    # filter
    print('==============================================')
    feature_better_bucket = features[(features['gap_ema21_ma50_half_percent_bucket'] > 0.01) & (features['gap_ema21_ma50_half_percent_bucket'] <= 0.8)]
    features_positive_better_bucket = feature_better_bucket[feature_better_bucket['label'] == 1]
    features_negative_better_bucket = feature_better_bucket[feature_better_bucket['label'] == -1]
    win = len(features_positive_better_bucket)
    lose = len(features_negative_better_bucket)
    total = len(feature_better_bucket)
    win_percent = win/total
    lose_percent = lose/total
    print(win_percent, lose_percent)
    
    print('==============================================')
    print(len(feature_better_bucket)/len(features))
    
    # distribution in positive and negative

    
    fig = go.Figure()
    fig.add_trace(go.Histogram(name='+',histnorm='percent',x=list(features_positive['gap_ema21_ma50_half_percent_bucket'])))
    fig.add_trace(go.Histogram(name='-',histnorm='percent',x=list(features_negative['gap_ema21_ma50_half_percent_bucket'])))
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    fig.show()
    
# exitable_after_ma50_negative_win_rate_improve()
entry_ma50_ema21_improve()