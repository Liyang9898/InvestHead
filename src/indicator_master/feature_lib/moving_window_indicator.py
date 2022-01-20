import numpy as np
import pandas as pd


def metric_positive_rate_mw(df, metric, window_size, feature_col):
    """
    input: feature_col is new feature name
    """
    df.reset_index(drop=True, inplace=True)
    df[feature_col] = np.nan
    
    full = False
    positive = 0
    negative = 0
#     queue = []
    l = 0
    r = 0
    
    for r in range(0, len(df)):
        # right edge moved up
        rv = df.loc[r, metric]
#         queue.append(rv)
        if not pd.isnull(rv):
            if rv > 0:
                positive += 1
            else:
                negative += 1
        
        # process left edge
        lv = df.loc[l, metric]
        if full and not pd.isnull(lv):
            if lv > 0:
                positive -= 1
            else:
                negative -= 1        
        
        # left edge move up
        if r - l >= window_size:
            l += 1
            full = True
#             queue.pop(0)
            
        # rate
        if positive + negative > 0:
            rate = positive / (positive + negative)
            df.loc[r, feature_col] = rate
            

