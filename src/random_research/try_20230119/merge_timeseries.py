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
    final_ts_chart_spy_benchmark
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


df_spy_benchmark = pre_process_ts(final_ts_chart_spy_benchmark, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
df_mudong_op_only = pre_process_ts(final_ts_chart_mudong_op_only, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
df_mudong_op_only_adjust = pre_process_ts(final_ts_chart_mudong_op_adjust, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
df_mudong_op_long_seq = pre_process_ts(final_ts_chart_mudong_op_long_seq, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
df_spy_weekly_swing = pre_process_ts(final_ts_chart_spy_weekly_swing, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)
df_op_swing_adjusted_monthly = pre_process_ts(final_op_swing_adjusted_monthly, date_col, val_col, ts_start_date, ts_end_date, max_start_date, max_end_date)


date_list = df_spy_benchmark['first_trading_day'].to_list()
ts_spy_benchmark = df_spy_benchmark['aum'].to_list()
ts_mudong_op_only = df_mudong_op_only['aum'].to_list()
ts_mudong_op_only_adjust = df_mudong_op_only_adjust['aum'].to_list()
ts_op_swing_adjusted_monthly = df_op_swing_adjusted_monthly['aum'].to_list()
ts_mudong_op_long_seq = df_mudong_op_long_seq['aum'].to_list()
ts_spy_weekly_swing = df_spy_weekly_swing['aum'].to_list()


y_list_map = {
    'SPY benchmark': ts_spy_benchmark,
    'Mudong Option Combination': ts_mudong_op_only,
    'Mudong Option Combination, adjusted': ts_mudong_op_only_adjust,
    'Mudong Option Combination, adjusted monthly': ts_op_swing_adjusted_monthly,
    'Mudong Option Combination-ema21>50 only': ts_mudong_op_long_seq,
    'SPY weekly swing-ema21>50 only': ts_spy_weekly_swing,
}

plot_lines_from_xy_list(x_list=date_list, y_list_map=y_list_map, title='AUM time series', path=None)

return_ts_spy_benchmark = diff_with_previous(ts_spy_benchmark)
return_ts_mudong_op_only = diff_with_previous(ts_mudong_op_only)
return_ts_mudong_op_only_adjust = diff_with_previous(ts_mudong_op_only_adjust)
return_ts_swing_adjusted_monthly = diff_with_previous(ts_op_swing_adjusted_monthly)
return_ts_mudong_op_long_seq = diff_with_previous(ts_mudong_op_long_seq)
return_ts_spy_weekly_swing = diff_with_previous(ts_spy_weekly_swing)


ab_mudong_op_only = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_mudong_op_only)
ab_mudong_op_only_adjust = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_mudong_op_only_adjust)
ab_mudong_op_swing_adjusted_monthly = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_swing_adjusted_monthly)
ab_mudong_op_long_seq = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_mudong_op_long_seq)
ab_spy_weekly_swing = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_spy_weekly_swing)

ab_mudong_op_only['strategy'] = 'mudong_op_only'
ab_mudong_op_only_adjust['strategy'] = 'mudong_op_only_adjust'
ab_mudong_op_swing_adjusted_monthly['strategy'] = 'mudong_op_swing_adjusted_monthly'
ab_mudong_op_long_seq['strategy'] = 'mudong_op_long_seq'
ab_spy_weekly_swing['strategy'] = 'spy_weekly_swing'



l = [ab_spy_weekly_swing, ab_mudong_op_only, ab_mudong_op_only_adjust, ab_mudong_op_swing_adjusted_monthly, ab_mudong_op_long_seq]
df_ab = pd.DataFrame(l)
path_ab = 'C:/f_data/random/alpha_beta_merge.csv'
df_ab.to_csv(path_ab,index=False)


# scaled PNL time series chart
multiplier_spy_benchmark = get_multiplier_scale_pnl_from_ts(ts_spy_benchmark, ts_spy_benchmark)
multiplier_mudong_op_only = get_multiplier_scale_pnl_from_ts(ts_mudong_op_only, ts_spy_benchmark)
multiplier_mudong_op_only_adjust = get_multiplier_scale_pnl_from_ts(ts_mudong_op_only_adjust, ts_spy_benchmark)
multiplier_op_swing_adjusted_monthly = get_multiplier_scale_pnl_from_ts(ts_op_swing_adjusted_monthly, ts_spy_benchmark)
multiplier_mudong_op_long_seq = get_multiplier_scale_pnl_from_ts(ts_mudong_op_long_seq, ts_spy_benchmark)
multiplier_spy_weekly_swing = get_multiplier_scale_pnl_from_ts(ts_spy_weekly_swing, ts_spy_benchmark)

print(multiplier_spy_benchmark, multiplier_mudong_op_only, multiplier_mudong_op_only_adjust, multiplier_op_swing_adjusted_monthly, multiplier_mudong_op_long_seq, multiplier_spy_weekly_swing)

ts_scaled_pnl_spy_benchmark = extract_scale_pnl_from_ts(ts_spy_benchmark, multiplier_spy_benchmark)
ts_scaled_pnl_mudong_op_only = extract_scale_pnl_from_ts(ts_mudong_op_only, multiplier_mudong_op_only)
ts_scaled_pnl_mudong_op_only_adjust = extract_scale_pnl_from_ts(ts_mudong_op_only_adjust, multiplier_mudong_op_only_adjust)
ts_scaled_pnl_mudong_op_swing_adjusted_monthly = extract_scale_pnl_from_ts(ts_op_swing_adjusted_monthly, multiplier_op_swing_adjusted_monthly)
ts_scaled_pnl_mudong_op_long_seq = extract_scale_pnl_from_ts(ts_mudong_op_long_seq, multiplier_mudong_op_long_seq)
ts_scaled_pnl_spy_weekly_swing = extract_scale_pnl_from_ts(ts_spy_weekly_swing, multiplier_spy_weekly_swing)

legend_spy = "SPY benchmark, multiplier = {}X".format(round(multiplier_spy_benchmark,2))
legend_mudong_op_only = "mudong_op_only, multiplier = {}X".format(round(multiplier_mudong_op_only,2))
legend_mudong_op_only_adjust = "mudong_op_only_adjust, multiplier = {}X".format(round(multiplier_mudong_op_only_adjust,2))
legend_mudong_op_swing_adjust_monthly = "mudong_op_swing_adjust_monthly, multiplier = {}X".format(round(multiplier_op_swing_adjusted_monthly,2))
legend_mudong_op_long_seq = "mudong_op_long_seq, multiplier = {}X".format(round(multiplier_mudong_op_long_seq,2))
legend_spy_weekly_swing = "spy_weekly_swing, multiplier = {}X".format(round(multiplier_spy_weekly_swing,2))

y_list_pnl_map = {
    legend_spy: ts_scaled_pnl_spy_benchmark,
    legend_mudong_op_only: ts_scaled_pnl_mudong_op_only,
    legend_mudong_op_only_adjust: ts_scaled_pnl_mudong_op_only_adjust,
    legend_mudong_op_swing_adjust_monthly: ts_scaled_pnl_mudong_op_swing_adjusted_monthly,
    legend_mudong_op_long_seq: ts_scaled_pnl_mudong_op_long_seq,
    legend_spy_weekly_swing: ts_scaled_pnl_spy_weekly_swing,
}

plot_lines_from_xy_list(x_list=date_list, y_list_map=y_list_pnl_map, title='PNL time series', path=None)