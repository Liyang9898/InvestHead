import numpy as np
from spy_volocity_study.lib.constant import S, S2, LABEL_ADJUST, E
from util.util import get_all_weekdays


def labeling(signal_list, drop_list, target_date):
    if target_date in signal_list:
        return True
    elif target_date in drop_list:
        return np.nan
    else:
        return False


def flatten_adjustment_signal_range(adjustments):
    res = []
    for adj in adjustments:
        x = get_all_weekdays(adj[S],adj[S2])
        res += x
    return res
        

def flatten_adjustment_drop_range(adjustments):
    res = []
    for adj in adjustments:
        # S2 plus one day
        
        x = get_all_weekdays(adj[S2],adj[E])
        res += x
    return res
        
        
def labeling_adjust_signal_range(df, adjustments):
    positive_dates = flatten_adjustment_signal_range(adjustments)
    negative_dates = flatten_adjustment_drop_range(adjustments)
    print(negative_dates)
    df[LABEL_ADJUST] = df.apply(lambda row : labeling(positive_dates, negative_dates, row['date']), axis = 1) 
    return df
    