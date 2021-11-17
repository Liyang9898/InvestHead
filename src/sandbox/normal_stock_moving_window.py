import pandas as pd
from plotting_lib.simple import moving_window_batch
from util.util import df_2col_to_dic


trade = 't_20210425_ema21_ma50_gap_per_ticker_4p_out'
path_spy = f'D:/f_data/sweep_20201214/trades/{trade}/merge/ui_backend_data.csv'

df = pd.read_csv(path_spy)
# print(df[['date','close']])

ticker = 'spy'
priceline = df_2col_to_dic(df, 'date', ticker)
mw_list = moving_window_batch(
    dic=priceline, 
    window_option=[260,120,60,20,10,5,2], 
    csv_path=f'D:/f_data/temp/moving_window_{ticker}.csv'
)
print(mw_list)

