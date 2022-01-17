import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate


feature_label_merge = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label_merge.csv'

df = pd.read_csv(feature_label_merge)
print(len(df))
# filter
# df = df[df['ma21_50_pct_gap']<0.2]
df1 = df[df['label'] == 1]
df2 = df[df['label'] == -1]
print(len(df1), len(df2), len(df1) / len(df))



feature_list = ['ma21_50_pct_gap', 'ma21_50_pct_gap_4p', 'label']
feature = 'ma21_50_pct_gap'
label = 'label'
bins = 30




chart_bucket_positive_rate(df, feature, label, bins, img_path='')