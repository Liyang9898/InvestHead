'''
Created on Feb 27, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.helper.validate_allocation_lib import validation_allocation
from random_research.try_20230224.sector_lib import rebuild_etf, \
    connect_ts_df_list


# get allocation
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_ranked.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_ranked.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_ranked_top3.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv"
path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute.csv"
# path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_increase_only.csv"


df_allo = pd.read_csv(path_allocation)
df_allo = df_allo.fillna(0)

ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLU']
validation_allocation(df_allo, ticker_list)


df_allo_list = df_allo.to_dict('records')


ts_list = []
for row in df_allo_list:
    start_date = row['start_date']
    end_date = row['end_date']
    allocation = row
    del allocation['start_date']
    del allocation['end_date']
    print(allocation)
    
    ts = rebuild_etf(allocation, start_date, end_date)
    
    title = start_date + '  ' + end_date
    path_debug = """C:/f_data/sector/debug/{title}.csv""".format(title=title)
    ts.to_csv(path_debug, index=False)
    
    ts_list.append(ts)

ts_connected = connect_ts_df_list(ts_list)
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50.csv'
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50_alpha_ranked.csv'
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50_alpha_calibrated_ranked.csv'
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg.csv'
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_ranked.csv'
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_ranked_top3.csv'
# path_out = 'C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv'
path_out = "C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute.csv"
# path_out = "C:/f_data/sector/result/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_increase_only.csv"


ts_connected.to_csv(path_out, index=False)
    
fig = px.line(ts_connected, x="date", y="ts", title='sector_remix')
fig.show()      


