from feature_engineering.cross_validation.k_fold_validation import k_fold_validation, \
    cross_validation_auto_cut
from feature_engineering.util.util import split_by_ticker
import pandas as pd
from version_master.version import (
    feature_engineering,
)


df = pd.read_csv(feature_engineering+'features.csv')
path_out = feature_engineering+'per_ticker_model_and_perf.csv'

ticker_dfs = split_by_ticker(df)

rows = []
for ticker, df_ticker in ticker_dfs.items():
    model_perf = cross_validation_auto_cut(df_ticker)
    model_perf['ticker'] = ticker
    rows.append(model_perf)
    print(model_perf)

df_model_and_perf = pd.DataFrame(rows)
df_model_and_perf.to_csv(path_out, index=False)