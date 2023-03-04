'''
Created on Feb 27, 2023

@author: spark
'''


import pandas as pd
from util.general_ui import plot_bar_set_from_xy_list
from util.util_finance import get_alpha_beta_from_list
from util.util_pandas import get_year_begin_rows, get_pnl_between_rows, get_month_begin_rows


def plot(df_pnl):
    # print(df_pnl)
    list_test = df_pnl['ts'].to_list()
    list_benchmark = df_pnl['spy'].to_list()
    ab = get_alpha_beta_from_list(list_test, list_benchmark)
    # print(ab)
    alpha = ab['alpha']
    beta = ab['beta']
    
    p = df_pnl[df_pnl['diff_pnl']>0]
    n = df_pnl[df_pnl['diff_pnl']<0]
    out_perf_chance = len(p) / (len(p) + len(n))
    p_sum = p['diff_pnl'].copy().sum()
    n_sum = n['diff_pnl'].copy().sum()
    
    ratio = 'inf'
    if n_sum != 0:
        ratio = p_sum/n_sum*-1
    
    
    title = "Out perform change = {out_perf_chance}, ratio={ratio}, alpha={alpha}, beta={beta}".format(
        out_perf_chance=out_perf_chance,
        ratio=ratio,
        alpha=alpha,
        beta=beta
    )
    
    x_list = list(df_pnl['date'].to_list())
    y_list_map = {
        'spy':list(df_pnl['spy'].to_list()),
        'exp':list(df_pnl['ts'].to_list()),
        'diff':list(df_pnl['diff_pnl'].to_list())
    }
    plot_bar_set_from_xy_list(x_list, y_list_map, title=title)
    
