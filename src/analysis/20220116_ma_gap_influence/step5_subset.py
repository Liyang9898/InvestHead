import pandas as pd
from util.util_feature_visualization import chart_bucket_positive_rate


feature_label_merge = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label_merge.csv'
feature_label_merge_less4p_lose = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label_merge_less4p_lose.csv'

df = pd.read_csv(feature_label_merge)

df = df[df['label']==False]
df = df[df['ma21_50_pct_gap']<0.04]
df = df.copy()
df.reset_index(inplace=True, drop=True)

print(df)
df.to_csv(feature_label_merge_less4p_lose)