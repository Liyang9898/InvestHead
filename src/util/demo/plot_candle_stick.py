import pandas as pd
from util.util_finance_chart import plot_candle_stick_with_trace





base_path = 'D:/f_data/trades_csv/'
path_w_d = base_path + 'SPY_1W_1D_merge.csv'
df_w_d=pd.read_csv(path_w_d)
# print(df_w_d.columns)

df_idc=pd.read_csv('D:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv')
# print(df_idc.columns)
# print(df_idc[['est_datetime','est_time']])

df_idc = pd.merge(df_idc, df_w_d, left_on='est_datetime', right_on='entry_ts', how='left')
# print(df_idc.columns)
df_idc['tag'] = df_idc['pnl_label'].astype(str) + df_idc['pnl_mark_daily'].astype(str)
tags = df_idc['tag'].unique()

traces = {}
for tag in tags:
    if tag == 'nannan':
        continue
    df_sub = df_idc[df_idc['tag']==tag]
    x = df_sub['entry_ts'].to_list()
    y = df_sub['open'].to_list()
    trace = {
        "x":x,
        "y":y
    }
    traces[tag] = trace
    
plot_candle_stick_with_trace(df_idc, traces)