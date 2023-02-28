'''
Created on Feb 27, 2023

@author: spark
'''
from sklearn import linear_model

import numpy as np
import pandas as pd
from util.util_finance import get_beta_from_list, get_alpha_beta
from util.util_time import df_filter_dy_date


path_benchmark = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
path_test = "C:/f_data/sector/indicator_day/XLF_1D_fmt_idc.csv"
df = pd.read_csv(path_test)
df_benchmark = pd.read_csv(path_benchmark)

start_date = '2018-02-01'
end_date = '2023-02-01'
period = 20
val_col = 'close'


ab = get_alpha_beta(df, df_benchmark, val_col, period, start_date, end_date)
print(ab)