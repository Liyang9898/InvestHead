from statistics import (
    mean,
    pstdev
)

def moving_window_pct_diff(l, window):
    # window = 1 len = 2,   len >= window + 1
    if len(l) < window + 1:
        print('window too big')
        return
    end_idx = len(l) - 1 - window
    begins = list(range(0,end_idx+1,1))
    res = []
    for s in begins:
        e = s + window
        diff = (l[e]-l[s]) / l[s]
        res.append(diff)
    return res


def max_pct_drop_positive_list(l):
    # have to assume all element are 0
    max_element = 0
    max_element_idx = -1
    max_drop_pct = 0
    max_drop_pct_idx = -1
    idx = 0
    max_idx_diff = 0
    max_recover_period_start = -1
    
    below_max_array = []
    
    for x in l:
        if x>max_element: # new max 
            max_element = x
            # update max recover time
            idx_diff = idx - max_element_idx
            if max_idx_diff < idx_diff:
                max_idx_diff = idx_diff
                max_recover_period_start = max_element_idx
            max_element_idx = idx
            below_max_array.append(0)
        else: # under previous max
            drop_pct = (x - max_element)/max_element
            below_max_array.append(drop_pct)
            if drop_pct < max_drop_pct:
                max_drop_pct = drop_pct
                max_drop_pct_idx = max_element_idx
        idx = idx + 1
        
    return {
        'max_drop_pct':max_drop_pct,
        'max_drop_pct_idx':max_drop_pct_idx,
        'max_recover_days':max_idx_diff,
        'max_recover_period_start':max_recover_period_start,
        'below_max_array':below_max_array
    }