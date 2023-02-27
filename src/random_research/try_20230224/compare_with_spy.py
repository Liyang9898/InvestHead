'''
Created on Feb 26, 2023

@author: spark
'''
from functools import reduce

import pandas as pd
from util.general_ui import plot_lines_from_xy_list
from util.util_pandas import df_general_time_filter, df_normalize


# spy benchmark
spy_path = "C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv"
df_spy = pd.read_csv(spy_path)

start_date = '2016-01-01'
end_date = '2022-01-01'

df_spy = df_general_time_filter(df_spy, 'date', start_date, end_date)
df_spy_normalize = df_normalize(df_spy, 'close', initial_val=1)
df_spy_normalize['spy'] = df_spy_normalize['close']
df_spy_normalize = df_spy_normalize[['date', 'spy']]
df_spy_normalize = df_spy_normalize.copy()

# test set
# test_path = 'C:/f_data/sector/result/spy_rebuild.csv'
test_path = 'C:/f_data/sector/result/spy_remix1.csv'
df_test = pd.read_csv(test_path)
df_test = df_normalize(df_test, 'ts', initial_val=1)

# plot
df_merge = reduce(lambda df1,df2: pd.merge(df1,df2,on='date'), [df_spy_normalize, df_test])
x_list = df_merge['date'].to_list()
y_list_map = {'test': df_merge['ts'].to_list(), 'spy': df_merge['spy'].to_list()}

plot_lines_from_xy_list(x_list, y_list_map, title='default', path=None)

       
