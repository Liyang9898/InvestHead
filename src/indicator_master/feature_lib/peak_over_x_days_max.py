import numpy as np
import pandas as pd


def peak_over_x_days(df, metric, lookback_range, feature_col):
    """
    input:
    df:the indicator Dataframe
    metric: the metric we need to compute feature on
    bar_range: how many gap are there between the start and end price, min = 1
    feature_col: column name of the new feature
    
    this function add a col called feature_col as a new feature
    
    today's metric value is higher than past x days at most
    """
    df.reset_index(drop=True, inplace=True)
    df[feature_col] = np.nan

    
    for r in range(0, len(df)):
        rv = df.loc[r, metric]
        if pd.isnull(rv):
            continue
        
        x = 0
        lmin = max(0, r - lookback_range)

        for l in range(r-1, lmin-1, -1):            
            lv = df.loc[l, metric]
            if pd.isnull(lv):
                df.loc[r, feature_col] = x
                break                

            if lv < rv:
                x += 1
                if l == lmin:
                    df.loc[r, feature_col] = x 
            else:
                df.loc[r, feature_col] = x
                break
        

