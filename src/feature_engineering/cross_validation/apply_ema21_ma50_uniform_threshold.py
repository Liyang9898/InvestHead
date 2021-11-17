from feature_engineering.cross_validation.k_fold_validation import k_fold_validation, \
    cross_validation_auto_cut
from feature_engineering.util.util import split_by_ticker
import pandas as pd
from version_master.version import (
    feature_engineering,
)
def applied_df(features, threshold):
    feature_better_bucket = features[(features['gap_ema21_ma50'] > threshold) & (features['gap_ema21_ma50'] <= 1)]
    return feature_better_bucket

df = pd.read_csv(feature_engineering+'features.csv')
path_model_per_ticker_df = pd.read_csv(feature_engineering+'per_ticker_model_and_perf.csv')
# path_per_ticker_model_applied_features = feature_engineering+'path_per_ticker_model_applied_features.csv'
path_per_ticker_uniform_threshold = feature_engineering+'_uniform_threshold.csv'

dfs=split_by_ticker(df)
new_dfs = []
threshold = 0.038
ress = []
for ticker, df_ticker in dfs.items():
    win_cnt = len(df_ticker[df_ticker['label']==1])
    perf = win_cnt / len(df_ticker)
#     print(ticker, perf)    
    
    df_new = df_ticker[(df_ticker['gap_ema21_ma50'] > threshold) & (df_ticker['gap_ema21_ma50'] <= 1)]
    
    win_cnt_new = len(df_new[df_new['label']==1])
    perf_new = win_cnt_new / len(df_new)
    perf_delta = perf_new-perf
    print(ticker, perf, perf_new, perf_delta)
    res = {
        'ticker':ticker,
        'perf_before':perf,
        'perf_after':perf_new,
        'perf_delta':perf_delta,
        'sample_cnt_before': len(df_ticker),
        'sample_cnt_after': len(df_new),
        'win_before':len(df_ticker)*perf,
        'win_after':len(df_new)*perf_new
    }
    ress.append(res)
    
df_perf_all = pd.DataFrame(ress)
df_perf_all.to_csv(path_per_ticker_uniform_threshold, index=False)
# merged_new = pd.concat(new_dfs)
# merged_new.to_csv(path_per_ticker_model_applied_features, index=False)
#     