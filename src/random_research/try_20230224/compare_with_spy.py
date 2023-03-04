'''
Created on Feb 26, 2023

@author: spark
'''
from functools import reduce

import pandas as pd
from random_research.try_20230224.perf_lib import plot
from util.general_ui import plot_bar_set_from_xy_list
from util.general_ui import plot_lines_from_xy_list
from util.util_finance import get_alpha_beta_from_list
from util.util_pandas import df_general_time_filter, df_normalize
from util.util_pandas import get_year_begin_rows, get_pnl_between_rows, get_month_begin_rows


# spy benchmark
spy_path = "C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv"
df_spy = pd.read_csv(spy_path)

start_date = '2005-06-01'
end_date = '2024-01-01'

df_spy = df_general_time_filter(df_spy, 'date', start_date, end_date)
df_spy_normalize = df_normalize(df_spy, 'close', initial_val=1)
df_spy_normalize['spy'] = df_spy_normalize['close']
df_spy_normalize = df_spy_normalize[['date', 'spy']]
df_spy_normalize = df_spy_normalize.copy()

# test set
# test_path = 'C:/f_data/sector/result/spy_rebuild.csv'


# test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50.csv'
# test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50_alpha_ranked.csv'
# test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50_alpha_calibrated_ranked.csv'
# test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg.csv'
# test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_ranked.csv'
# test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_ranked_top3.csv'
test_path = 'C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv'



df_test = pd.read_csv(test_path)
df_test = df_general_time_filter(df_test, 'date', start_date, end_date)
df_test = df_normalize(df_test, 'ts', initial_val=1)

# plot
df_merge = reduce(lambda df1,df2: pd.merge(df1,df2,on='date'), [df_spy_normalize, df_test])
x_list = df_merge['date'].to_list()
y_list_map = {'test': df_merge['ts'].to_list(), 'spy': df_merge['spy'].to_list()}

plot_lines_from_xy_list(x_list, y_list_map, title='default', path=None)

ppp = 'C:/f_data/sector/result/merge.csv'
df_merge.to_csv(ppp, index=False)


#########################################

benchmark_col = 'spy'
exp_col = 'ts'

ppp = 'C:/f_data/sector/result/merge.csv'
df = pd.read_csv(ppp)


### year
df_year = get_year_begin_rows(df)        
df_year_pnl = get_pnl_between_rows(df_year, benchmark_col, exp_col)
# print(df_year_pnl)
plot(df_year_pnl)

### month
df_month = get_month_begin_rows(df)        
df_month_pnl = get_pnl_between_rows(df_month, benchmark_col, exp_col)

pnl_diff_path = 'C:/f_data/sector/debug/pnl_diff.csv'
df_month_pnl.to_csv(pnl_diff_path)
# print(df_month_pnl)
plot(df_month_pnl)
