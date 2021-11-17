import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from version_master.version import (
    feature_engineering
)

    
def process_chance_neutralout_after_70p_shrink(df, main_feature_name, feature_name, feature_value):
    features_partial = df[df[feature_name]==feature_value]
    
    features_per_val = features_partial.groupby([main_feature_name])['label'].count().reset_index()[[main_feature_name, 'label']]
    new_col_name = feature_name + '=' + str(feature_value)
    features_per_val.rename(columns={"label": new_col_name}, inplace=True)    

    assert len(features_per_val) == len(features_per_val)
    print(features_per_val.columns)
    return features_per_val


def process_neutral_exited_win_lose(df, label):
    features_exited = df[df['chance_neutralout_after_70p_shrink']==1]
    feature_single_label = features_exited[features_exited['label']==label]
    features_per_val = feature_single_label.groupby(['total_21_50_gap_shrink_percent'])['label'].count().reset_index()[['total_21_50_gap_shrink_percent', 'label']]
    
    col_filter =  features_per_val[['total_21_50_gap_shrink_percent', 'label']]
    new_col_name = str(label) + '_to_neutral_exit'
    col_filter.rename(columns={"label": new_col_name}, inplace=True)  
    return col_filter
    
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
    
    # handling chance_neutralout_after_70p_shrink different value
    sub_feature = 'chance_neutralout_after_70p_shrink'
    feature_1 = process_chance_neutralout_after_70p_shrink(
        df=features, 
        main_feature_name=feature_val_col_name, 
        feature_name=sub_feature, 
        feature_value=1
    )
    feature_0 = process_chance_neutralout_after_70p_shrink(
        df=features, 
        main_feature_name=feature_val_col_name, 
        feature_name=sub_feature, 
        feature_value=0
    )
    feature_neg_1 = process_chance_neutralout_after_70p_shrink(
        df=features, 
        main_feature_name=feature_val_col_name, 
        feature_name=sub_feature, 
        feature_value=-1
    )
    percentage = pd.merge(percentage,feature_1,how="left",on=feature_val_col_name)
    percentage = pd.merge(percentage,feature_0,how="left",on=feature_val_col_name)
    percentage = pd.merge(percentage,feature_neg_1,how="left",on=feature_val_col_name)

    neutral_exit_win = process_neutral_exited_win_lose(df=features, label=1)
    neutral_exit_lose = process_neutral_exited_win_lose(df=features, label=-1)


    percentage = pd.merge(percentage,neutral_exit_win,how="left",on=feature_val_col_name)
    percentage = pd.merge(percentage,neutral_exit_lose,how="left",on=feature_val_col_name)

    percentage.to_csv(feature_engineering+'temp_shrink_70p.csv')
    print(percentage.columns)
    
    
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

# feature_bucket_analysis('total_21_50_gap_shrink')
# feature_bucket_analysis('longest_21_50_gap_shrink')
feature_bucket_analysis('total_21_50_gap_shrink_percent')