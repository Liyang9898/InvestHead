'''
Created on Jan 28, 2023

@author: spark
'''
'''
first_trading_day is date
'''
'''
Conclusion 1:
under same final gain after applying multiplier
for fluctuation:
mudong_op_long_seq < spy weekly swing < mudong_op_only < SPY  
So, mudong_op_long_seq is the best strategy: 
1.only buy 1 year option at 1/1 of each year (strike price = current price, upper profit cap = 12.5%, lower loss start = 12.5%, bond 4.6%, based on 2023 Jan data)
2.only buy combination when spy weekly ema21 > ma5 (follow strategy of strat_param_20211006_ma_max_drawdown_cut)
'''

import pandas as pd
from random_research.try_20230119.constant import final_ts_chart_mudong_op_only, \
    final_ts_chart_mudong_op_adjust, final_ts_chart_mudong_op_long_seq, \
    final_ts_chart_spy_weekly_swing, final_op_swing_adjusted_monthly, \
    final_ts_chart_spy_benchmark, mudong_op_swing_adjusted_monthly_125_125
from random_research.try_20230119.mudong_lib import df_time_filter_and_normalize
from util.general_ui import plot_lines_from_xy_list
from util.util_math import compute_alpha_beta
from util.util_pandas import insert_missing_date_val_to_df_cols


def pre_process_ts(path, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date):
    # step 0: read csv
    df = pd.read_csv(path)

    # step 1: interpolate
    df = insert_missing_date_val_to_df_cols(df=df, date_col=date_col, val_col=val_col, start_date=max_start_date, end_date=max_end_date)
    
    # step 2: filter and normalize
    df = df_time_filter_and_normalize(df=df, date_col=date_col, normalize_col=val_col, start_date=ts_start_date, end_date=ts_end_date)
    
    return df


def diff_with_previous(l):
    res = []
    for i in range(1, len(l)):
        x = l[i] - l[i-1]
        res.append(x)
    return res


def get_multiplier_scale_pnl_from_ts(list_ts, benchmark_ts):
    '''
        input time series list_ts, benchmark_ts has the same starting point 1
        step 0: validate first is 0
        step 1: extract pnl from list_ts & benchmark_ts, meaning minus 1 on all data point of ts.
        step 2: compute multiplier x on top of list_ts to make the end point of pnl of list_ts & benchmark_ts match
    ''' 
    
    # step 0
    if list_ts[0] != 1 or  benchmark_ts[0] != 1:
        raise Exception('first element of a time series must be 0')
    
    # step 1
    list_pnl_ts = [x - 1 for x in list_ts]
    benchmark_pnl_ts = [x - 1 for x in benchmark_ts]
    
    # step 2:
    end_element_val_x = list_pnl_ts[len(list_pnl_ts) - 1]
    end_element_val_benchmark = benchmark_pnl_ts[len(benchmark_pnl_ts) - 1]
    
    multiplier = end_element_val_benchmark / end_element_val_x
    return multiplier


def extract_scale_pnl_from_ts(list_ts, multiplier):
    '''
        input time series list_ts, benchmark_ts has the same starting point 1
        step 0: validate first is 0
        step 1: apply multiplier and return scaled pnl time series
    ''' 
    
    # step 0
    if list_ts[0] != 1:
        raise Exception('first element of a time series must be 0')
    
    # step 1
    list_scaled_ts = [x * multiplier for x in list_ts]
    list_scaled_pnl_ts = [x - multiplier for x in list_scaled_ts]
    
    return list_scaled_pnl_ts
    
    
max_start_date = '1994-01-01'
max_end_date = '2023-02-05'

ts_start_date = '1994-12-15'
ts_end_date = '2022-01-17'
date_col = 'first_trading_day'
val_col = 'aum'



strategy_name_ts_csv = {
    'spy benchmark': final_ts_chart_spy_benchmark,
    'Mudong op yearly 125 125':final_ts_chart_mudong_op_only,
    'Mudong op yearly 175_75':final_ts_chart_mudong_op_adjust,
    'Mudong op yearly ema21>50':final_ts_chart_mudong_op_long_seq,
    'Weekly swing':final_ts_chart_spy_weekly_swing,
    'Mudong op monthly 175 75':final_op_swing_adjusted_monthly,
    'Mudong op monthly 125 125':mudong_op_swing_adjusted_monthly_125_125,
}


df_spy_benchmark = pre_process_ts(final_ts_chart_spy_benchmark, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
df_ts = {}
for name, csv_path in strategy_name_ts_csv.items():
    df_ts[name] = pre_process_ts(csv_path, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
    

date_list = df_ts['spy benchmark']['first_trading_day'].to_list()
ts = {}
for name, csv_path in strategy_name_ts_csv.items():
    ts[name] = df_ts[name]['aum'].to_list()


plot_lines_from_xy_list(x_list=date_list, y_list_map=ts, title='AUM time series', path=None)


'''
alpha-beta
'''
ab = {}
l = []
benchmark_return_ts = diff_with_previous(ts['spy benchmark'])
for name, csv_path in strategy_name_ts_csv.items():
    return_ts = diff_with_previous(ts[name])
    ab[name] = compute_alpha_beta(list_benchmark=benchmark_return_ts, list_exp=return_ts)
    ab[name]['strategy'] = name
    print(ab[name])
    l.append(ab[name])


df_ab = pd.DataFrame(l)
path_ab = 'C:/f_data/random/alpha_beta_merge.csv'
df_ab.to_csv(path_ab,index=False)
#
#
"""
scale
"""
y_list_pnl_map = {}
for name, csv_path in strategy_name_ts_csv.items():
    multiplier = get_multiplier_scale_pnl_from_ts(ts[name], ts['spy benchmark'])
    ts_scaled_pnl = extract_scale_pnl_from_ts(ts[name], multiplier)
    legend = name + ", multiplier = {}X".format(round(multiplier, 2))
    y_list_pnl_map[legend] = ts_scaled_pnl

plot_lines_from_xy_list(x_list=date_list, y_list_map=y_list_pnl_map, title='PNL time series', path=None)