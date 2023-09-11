'''
Created on Sep 10, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from strategy_lib.stratage_param import strat_param_20211006_ma_max_drawdown_cut
from util.general_ui import plot_bar_set_from_xy_list
from util.util_finance_chart import gen_yearly_return_plot
from util.util_pandas import df_to_dict


strat_param_20211006_ma_max_drawdown_cut
strategy_name = strat_param_20211006_ma_max_drawdown_cut['name']
path_cash_position = f'C:/f_data/temp/cash_position_{strategy_name}.csv'
df = pd.read_csv(path_cash_position)
print(df)

gen_yearly_return_plot(df, 'baseline', 'test')
#
#

