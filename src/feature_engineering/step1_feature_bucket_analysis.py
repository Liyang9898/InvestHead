import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from version_master.version import (
    feature_engineering
)

    
def feature_bucket_analysis(feature_val_col_name):
    path=feature_engineering+'features.csv'
    features = pd.read_csv(path)
    
    # a filter per ticker for debugging purpose
#     features = features[features['ticker']=='AMD'] # a filter per ticker
#     print(features.columns)
    
    # distinct feature value
    vals=list(features[feature_val_col_name].unique())
    
    # total
    total_per_val = features.groupby([feature_val_col_name])['label'].count().reset_index()
    total_per_val.rename(columns={"label": "cnt_total"}, inplace=True)
    
    # positive
    features_positive = features[features['label'] == 1]
    total_per_val_positive = features_positive.groupby([feature_val_col_name])['label'].count().reset_index()
    total_per_val_positive.rename(columns={"label": "cnt_positive"}, inplace=True)

    percentage = pd.merge(total_per_val,total_per_val_positive,how="inner",on=feature_val_col_name)
    percentage['win_rate'] = percentage['cnt_positive'] / percentage['cnt_total']
    total = len(features)
    percentage['distribution'] = percentage['cnt_total'] / total
#     assert percentage['distribution'].sum() >= 0.9999
    print(percentage['distribution'].sum())
    print(percentage)
    percentage.to_csv(feature_engineering+'temp.csv')
    
    
##########################################################################
#         'ma50_negative_cnt':ma50_negative_cnt,
#         'total_21_50_gap_shrink':total_21_50_gap_shrink,
#         'longest_21_50_gap_shrink':longest_21_50_gap_shrink,
#         # if ma50 always positive, that require price during the holding should always > price 50 days ago
#         'exitable_after_ma50_negative':exitable_after_ma50_negative,
#         'holding_days': holding_days,
#         'total_21_50_gap_shrink_percent': total_21_50_gap_shrink_percent
##########################################################################

# feature_bucket_analysis('ma50_negative_cnt')
# feature_bucket_analysis('exitable_after_ma50_negative')

feature_bucket_analysis('total_21_50_gap_shrink')
# feature_bucket_analysis('longest_21_50_gap_shrink')
# feature_bucket_analysis('total_21_50_gap_shrink_percent')