'''
Created on Feb 27, 2023

@author: spark
'''


import pandas as pd
from util.general_ui import plot_bar_set_from_xy_list
from util.util_pandas import get_year_begin_rows, get_pnl_between_rows, get_month_begin_rows



def plot(df_pnl):
    x_list = list(df_pnl['date'].to_list())
    y_list_map = {
        'spy':list(df_pnl['spy'].to_list()),
        'exp':list(df_pnl['ts'].to_list()),
        'diff':list(df_pnl['diff_pnl'].to_list())
    }
    plot_bar_set_from_xy_list(x_list, y_list_map, title='year')
    

benchmark_col = 'spy'
exp_col = 'ts'

ppp = 'C:/f_data/sector/result/merge.csv'
df = pd.read_csv(ppp)


### year
df_year = get_year_begin_rows(df)        
df_year_pnl = get_pnl_between_rows(df_year, benchmark_col, exp_col)
print(df_year_pnl)
plot(df_year_pnl)

### month
df_month = get_month_begin_rows(df)        
df_month_pnl = get_pnl_between_rows(df_month, benchmark_col, exp_col)

pnl_diff_path = 'C:/f_data/sector/debug/pnl_diff.csv'
df_month_pnl.to_csv(pnl_diff_path)
print(df_month_pnl)
plot(df_month_pnl)