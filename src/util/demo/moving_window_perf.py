import pandas as pd
from util.util_finance import moving_window_perf_bundle
from util.util_math import max_pct_drop_positive_list


# path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
# df_ticker = pd.read_csv(path)
# 
# sample = df_ticker['close'].to_list()
# sample_date = df_ticker['date'].to_list()
# print(sample)
# 
# res_250 = moving_window_perf_bundle(sample, 250)
# res_20 = moving_window_perf_bundle(sample, 20)
# res_5 = moving_window_perf_bundle(sample, 5)
# res_1 = moving_window_perf_bundle(sample, 1)
# 
# print(res_250)
# print(res_20)
# print(res_5)
# print(res_1)


# a = max_drawdown_recover(sample, sample_date)
# print(a)
e = '2020-08-01'
path2 = 'D:/f_data/temp/movingwindow_test.csv'
def_real = pd.read_csv(path2)

d_list = def_real['date'].to_list()


p_mv = moving_window_perf_bundle(def_real['price'].to_list(),d_list, 250)

print(p_mv)


st_old_mv = moving_window_perf_bundle(def_real['exit_on_21_50'].to_list(), d_list,250)

print(st_old_mv)


st_new_mv = moving_window_perf_bundle(def_real['exit_on_not_8_21_50'].to_list(), d_list,250)

print(st_new_mv)