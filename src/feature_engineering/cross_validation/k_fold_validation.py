# import random

from feature_engineering.cross_validation.k_split import k_split
from feature_engineering.lib.modeling_ema21_ma50_gap import fit, eval
import pandas as pd
# from version_master.version import (
#     t_20210321_myswing,
#     indicator_20210404,
#     feature_engineering,
#     feature_engineering_split
# )
# from batch_20201214.analysis.compare_with_without_channel_enter import res


# df = pd.read_csv(feature_engineering+'features.csv')


def k_fold_validation(df,k):
    win_rate = []
    models = []
    dfs = k_split(df,k)
    for i in range(0,k):
        eval_data = dfs[i]
        training_list = []
        for j in range(0,k):
            if i == j:
                continue
            training_list.append(dfs[j].copy()) 
        training_date = pd.concat(training_list)
#         print(len(eval_data), len(training_date))
        model = fit(training_date)
#         print(model)
        eval_res = eval(eval_data, model['threshold'])
#         print(eval_res)
        win_rate.append(eval_res['win_rate'])
        models.append(model['threshold'])
    avg_perf = sum(win_rate) / len(win_rate)
    avg_model = sum(models) / len(models)
    perf_max = max(win_rate)/avg_perf - 1
    perf_min = min(win_rate)/avg_perf - 1
    
    model_max = 0
    model_min = 0
    if avg_model != 0:
        model_max = max(models)/avg_model - 1
        model_min = min(models)/avg_model - 1
    
    win_cnt = len(df[df['label']==1])
    perf_baseline = win_cnt / len(df)
    
    res = {
        'sample_size_baseline':len(df),
        'perf_baseline':perf_baseline,
        'perf':avg_perf,
        'perf_gain':avg_perf-perf_baseline,
        'perf_max':perf_max,
        'perf_min':perf_min,
        'model':avg_model,
        'model_max':model_max,
        'model_min':model_min,
        'fold':k
    }
    return res
  
        
def cross_validation_auto_cut(df):
    fold = fold_selector(len(df))
    res = k_fold_validation(df,fold)
    return res


def fold_selector(sample_size):
    fold = int(sample_size / 20)
    if fold < 2:
        fold = 2
    if fold > 10:
        fold = 10
    return fold
