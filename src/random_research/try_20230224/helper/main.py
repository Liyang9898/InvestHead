'''
Created on Mar 11, 2023

@author: spark
'''
import pandas as pd
from random_research.try_20230224.helper.apply_allocation_lib import connection_ts
from random_research.try_20230224.helper.validate_allocation_lib import validation_allocation



ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLU']
path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv"
path_ts = "C:/f_data/sector/debug/ts_allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv"
allocation_df = pd.read_csv(path_allocation)
allocation_df = allocation_df.fillna(0)
validation_allocation(allocation_df, ticker_list)
df_all = connection_ts(allocation_df)
df_all.to_csv(path_ts, index=False)
