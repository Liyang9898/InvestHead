from statistics import (
    mean,
    pstdev
)
import random

from datetime import datetime
from statistics import (
    mean,
    pstdev
)

from sklearn import linear_model
from norgate.ticker_price_downloader import pull_ticker_price_locally_norgate
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from price_asset_master.lib.api.api import download_ticker
from util.general_ui import plot_line_from_xy_list, plot_lines_from_xy_list
from util.util import plot_hist_from_df_col, \
    extract_sub_df_single_st_based_on_period

from util.util_time import days_gap_date_str, mark_year_month_week_start, \
    df_filter_dy_date


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
    
    
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def intersection_of_k_list(lists):
    main = lists[0].copy()
    for i in range(1,len(lists)):
        cur = lists[i]
        main = intersection(main, cur)
    return main


def draw_x_card_out_of_y(x, y):

    res = []
    for i in range(0,min(x,y)):
        r = random.randint(1, y)
        while r in res:
            r = random.randint(1, y)

        res.append(r)
    return res


def percentile(l, p, asc=True):
    '''
    compute value at a certain percentile
    l is a list values
    p is percentile
    asc means the l list is sorted in asc order
    p=90 will pick the 10% element from the right
    '''
    if len(l)==0:
        raise Exception("no value to compute percentile")
    if p < 0 or p > 1:
        raise Exception("p should be between 0 and 1")
    if asc:
        l.sort() # default is ascending
    else: # descending
        l.sort(reverse=True) 
    length = len(l)
    idx = int(length * p) - 1
    if idx < 0:
        idx = 0
    return l[idx]


def get_beta_from_list(baseline, target):
    array1 = np.array(baseline)
    array2 = np.array(target)
    cov_matrix = np.cov(array1, array2)
    covariance = cov_matrix[0][1]
    variance  = np.var(baseline)
    beta = covariance / variance
    return beta


def compute_alpha_beta(list_benchmark, list_exp):
    x = np.array(list_benchmark).reshape(-1, 1)
    y = np.array(list_exp).reshape(-1, 1)

    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(x, y)
    # The coefficients
    r_sq = regr.score(x, y)
    alpha = regr.intercept_[0]
    beta = regr.coef_[0][0]
    beta2 = get_beta_from_list(list_benchmark, list_exp)

    res = {
        'alpha':round(alpha,4),
        'beta':round(beta,4),
        'beta2':round(beta2,4),
        'r_sq':round(r_sq,4)
    }
    
    return res


    