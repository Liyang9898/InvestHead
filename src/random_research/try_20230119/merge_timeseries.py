'''
Created on Jan 28, 2023

@author: spark
'''
'''
first_trading_day is date
'''

import pandas as pd
from random_research.try_20230119.mudong_op_long_seq_only import final_ts_chart_mudong_op_long_seq
from random_research.try_20230119.mudong_op_only import final_ts_chart_mudong_op_only
from random_research.try_20230119.spy_bench_mark import final_ts_chart_spy_benchmark
from random_research.try_20230119.spy_weekly_swing import final_ts_chart_spy_weekly_swing
from util.general_ui import plot_lines_from_xy_list
from util.util_math import compute_alpha_beta


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

plot_lines_from_xy_list(x_list=date_list, y_list_map=y_list_map, title='default', path=None)

ab_mudong_op_only = compute_alpha_beta(list_benchmark=ts_spy_benchmark, list_exp=ts_mudong_op_only)
ab_mudong_op_long_seq = compute_alpha_beta(list_benchmark=ts_spy_benchmark, list_exp=ts_mudong_op_long_seq)
ab_spy_weekly_swing = compute_alpha_beta(list_benchmark=ts_spy_benchmark, list_exp=ts_spy_weekly_swing)

ab_mudong_op_only['strategy'] = 'mudong_op_only'
ab_mudong_op_long_seq['strategy'] = 'mudong_op_long_seq'
ab_spy_weekly_swing['strategy'] = 'spy_weekly_swing'

l = [ab_spy_weekly_swing, ab_mudong_op_only, ab_mudong_op_long_seq]
df_ab = pd.DataFrame(l)
path_ab = 'C:/f_data/random/alpha_beta_merge.csv'
df_ab.to_csv(path_ab,index=False)
