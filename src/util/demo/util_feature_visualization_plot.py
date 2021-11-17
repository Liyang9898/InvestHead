import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate, \
    chart_positive_negative_distribution, bucket_positive_rate


# from util import chart_bucket_positive_rate
# TEST:###################################################
path = 'D:/f_data/temp/v_to_21_50_cross_training_eval.csv'
df = pd.read_csv(path)
feature='price_velocity_1d_pct'
# feature = 'price_delta_oc_pct'
label='label'
bins = 25

chart_bucket_positive_rate(
    df=df, 
    feature=feature, 
    label=label, 
    bins=bins, 
)
  
chart_positive_negative_distribution(
    df=df, 
    feature=feature, 
    label=label, 
    bins=bins, 
)
 
bucket_path = 'D:/f_data/temp/v_to_21_50_cross_training_eval_bucketed.csv'
ratio = bucket_positive_rate(df, feature,label, bins, bucket_path)
print(ratio)
# 
# df_b = pd.read_csv(bucket_path)
# threshold = -0.033950
# df_b_select = df_b[df_b['bucket_mid']==threshold]
# df_b_select = df_b_select[['date', 'label', feature]]
# print(df_b_select)
