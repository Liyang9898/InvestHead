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
from random_research.try_20230119.mudong_op_long_seq_only import final_ts_chart_mudong_op_long_seq
from random_research.try_20230119.mudong_op_only import final_ts_chart_mudong_op_only
from random_research.try_20230119.spy_bench_mark import final_ts_chart_spy_benchmark
from random_research.try_20230119.spy_weekly_swing import final_ts_chart_spy_weekly_swing
from util.general_ui import plot_lines_from_xy_list
from util.util_math import compute_alpha_beta


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
    



df_spy_benchmark = pd.read_csv(final_ts_chart_spy_benchmark)
df_mudong_op_only = pd.read_csv(final_ts_chart_mudong_op_only)
df_mudong_op_long_seq = pd.read_csv(final_ts_chart_mudong_op_long_seq)
df_spy_weekly_swing = pd.read_csv(final_ts_chart_spy_weekly_swing)


date_list = df_spy_benchmark['first_trading_day'].to_list()
ts_spy_benchmark = df_spy_benchmark['aum'].to_list()
ts_mudong_op_only = df_mudong_op_only['aum'].to_list()
ts_mudong_op_long_seq = df_mudong_op_long_seq['aum'].to_list()
ts_spy_weekly_swing = df_spy_weekly_swing['aum'].to_list()


y_list_map = {
    'SPY benchmark': ts_spy_benchmark,
    'Mudong Option Combination': ts_mudong_op_only,
    'Mudong Option Combination-ema21>50 only': ts_mudong_op_long_seq,
    'SPY weekly swing-ema21>50 only': ts_spy_weekly_swing,
}

plot_lines_from_xy_list(x_list=date_list, y_list_map=y_list_map, title='AUM time series', path=None)

return_ts_spy_benchmark = diff_with_previous(ts_spy_benchmark)
return_ts_mudong_op_only = diff_with_previous(ts_mudong_op_only)
return_ts_mudong_op_long_seq = diff_with_previous(ts_mudong_op_long_seq)
return_ts_spy_weekly_swing = diff_with_previous(ts_spy_weekly_swing)

ab_mudong_op_only = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_mudong_op_only)
ab_mudong_op_long_seq = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_mudong_op_long_seq)
ab_spy_weekly_swing = compute_alpha_beta(list_benchmark=return_ts_spy_benchmark, list_exp=return_ts_spy_weekly_swing)

ab_mudong_op_only['strategy'] = 'mudong_op_only'
ab_mudong_op_long_seq['strategy'] = 'mudong_op_long_seq'
ab_spy_weekly_swing['strategy'] = 'spy_weekly_swing'

l = [ab_spy_weekly_swing, ab_mudong_op_only, ab_mudong_op_long_seq]
df_ab = pd.DataFrame(l)
path_ab = 'C:/f_data/random/alpha_beta_merge.csv'
df_ab.to_csv(path_ab,index=False)


# scaled PNL time series chart
multiplier_spy_benchmark = get_multiplier_scale_pnl_from_ts(ts_spy_benchmark, ts_spy_benchmark)
multiplier_mudong_op_only = get_multiplier_scale_pnl_from_ts(ts_mudong_op_only, ts_spy_benchmark)
multiplier_mudong_op_long_seq = get_multiplier_scale_pnl_from_ts(ts_mudong_op_long_seq, ts_spy_benchmark)
multiplier_spy_weekly_swing = get_multiplier_scale_pnl_from_ts(ts_spy_weekly_swing, ts_spy_benchmark)
print(multiplier_spy_benchmark, multiplier_mudong_op_only, multiplier_mudong_op_long_seq, multiplier_spy_weekly_swing)

ts_scaled_pnl_spy_benchmark = extract_scale_pnl_from_ts(ts_spy_benchmark, multiplier_spy_benchmark)
ts_scaled_pnl_mudong_op_only = extract_scale_pnl_from_ts(ts_mudong_op_only, multiplier_mudong_op_only)
ts_scaled_pnl_mudong_op_long_seq = extract_scale_pnl_from_ts(ts_mudong_op_long_seq, multiplier_mudong_op_long_seq)
ts_scaled_pnl_spy_weekly_swing = extract_scale_pnl_from_ts(ts_spy_weekly_swing, multiplier_spy_weekly_swing)

legend_spy = "SPY benchmark, multiplier = {}X".format(round(multiplier_spy_benchmark,2))
legend_mudong_op_only = "mudong_op_only, multiplier = {}X".format(round(multiplier_mudong_op_only,2))
legend_mudong_op_long_seq = "mudong_op_long_seq, multiplier = {}X".format(round(multiplier_mudong_op_long_seq,2))
legend_spy_weekly_swing = "spy_weekly_swing, multiplier = {}X".format(round(multiplier_spy_weekly_swing,2))

y_list_pnl_map = {
    legend_spy: ts_scaled_pnl_spy_benchmark,
    legend_mudong_op_only: ts_scaled_pnl_mudong_op_only,
    legend_mudong_op_long_seq: ts_scaled_pnl_mudong_op_long_seq,
    legend_spy_weekly_swing: ts_scaled_pnl_spy_weekly_swing,
}

plot_lines_from_xy_list(x_list=date_list, y_list_map=y_list_pnl_map, title='PNL time series', path=None)