'''
Created on Mar 1, 2023

@author: spark
'''
import pandas as pd
from trading_floor_v2.trading_infra_lib import run_trading_strategy


path_test = "C:/f_data/sector/indicator_day/XLF_1D_fmt_idc.csv"
df = pd.read_csv(path_test)

action_list = run_trading_strategy(df)
print(action_list)