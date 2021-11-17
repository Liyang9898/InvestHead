from feature_engineering.cross_validation.k_fold_validation import k_fold_validation, \
    cross_validation_auto_cut
from feature_engineering.util.util import split_by_ticker
import pandas as pd
from version_master.version import (
    feature_engineering,
)


path_per_ticker_model_applied_features = feature_engineering+'path_per_ticker_model_applied_features.csv'
df = pd.read_csv(path_per_ticker_model_applied_features)


print(df)

win_cnt = len(df[df['label']==1])
perf = win_cnt / len(df)
print(perf)