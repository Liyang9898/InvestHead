
from batch_20201214.util_for_batch.batch_util import get_all_files
import pandas as pd
from version_master.version import (
    meta_20210117,
    iwf_up,
    iwf_down,
    trade_swing_2150in_2150out_20210313_iwf,
    trade_swing_2150in_2150out_20210313_iwf_50up,
    trade_swing_2150in_2150out_20210313_iwf_50down
)
import os
from shutil import copyfile
from pip._internal.cli.cmdoptions import src

# 
# df1 = pd.read_csv(iwf)
# df2 = pd.read_csv(meta_20210117)
# 
# merged_df = df1.merge(df2, how='left', left_on=["ticker"], right_on=["ticker"])   
# print(len(df1), len(merged_df))
# 
# df_up = merged_df[merged_df['ma50_up_rate']>0.6]
# df_down = merged_df[merged_df['ma50_up_rate']<0.6]
# 
# up = df_up[['ticker']]
# down = df_down[['ticker']]
# print(len(up), len(down))
# up.to_csv('D:/f_data/etf/iwf_ma50_60up_2021_02_21.csv', index=False)
# down.to_csv('D:/f_data/etf/iwf_ma50_60down_2021_02_21.csv', index=False)



# trade_path1 = trade_swing_2150in_2150out_20210313_iwf
# trade_path2 = trade_swing_2150in_2150out_20210313_iwf_50down
# sub = 'summary/'    #'summary/'
# 
# src = trade_path1 + sub
# dst = trade_path2 + sub
# filter = pd.read_csv(iwf_down)['ticker'].to_list()
# 
# def get_all_files(src, dst, filter):
#     print(src,dst,len(filter))
#     for file in os.listdir(src):
#         if file.endswith(".csv"):
#             ticker = file.split('_')[0]
#             if ticker not in filter:
#                 continue
#             copyfile(src+file, dst+file)
# 
# get_all_files(src, dst, filter)           



import pandas as pd
import plotly.express as px
# my_dict = {'2020-01-01':1,'2020-01-02':4}
# df = pd.DataFrame(list(my_dict.items()),columns = ['date','v']) 
# print(df)

path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df = pd.read_csv(path)

fig = px.line(df, x="date", y="barlow_2_ema21_percent_oneyear_channel_percentile", title='aaa')
fig.show()