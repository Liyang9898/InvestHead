'''
Created on Feb 27, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.helper.build_aum import build_aum
from random_research.try_20230224.helper.memory_data_asset import prepare_ticker_df_dict
from random_research.try_20230224.helper.validate_allocation_lib import validation_allocation
from random_research.try_20230224.sector_lib import rebuild_etf, \
    connect_ts_df_list
from util.util_pandas import df_general_time_filter


# experiment_name
# experiment_name = "allocation_ema21_below_ma50"
# experiment_name = "allocation_ema21_below_ma50_alpha_ranked"
# experiment_name = "allocation_ema21_below_ma50_alpha_calibrated_ranked"
# experiment_name = "allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg"
# experiment_name = "allocation/allocation_ema21_below_ma50_recent_pnl_ranked"
# experiment_name = "allocation_ema21_below_ma50_recent_pnl_ranked_top3"
# experiment_name = "allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3"
# experiment_name = "allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute"
experiment_name = "weekly_allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute"
# experiment_name = "allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_increase_only"


# get allocation
path_allocation = "C:/f_data/sector/allocation/{experiment_name}.csv".format(experiment_name=experiment_name)
path_out = "C:/f_data/sector/result/{experiment_name}.csv".format(experiment_name=experiment_name)
path_out_sector = "C:/f_data/sector/result_sector/{experiment_name}.csv".format(experiment_name=experiment_name)

start_date = '2005-06-01'
end_date = '2023-02-15'

df_allo = pd.read_csv(path_allocation)
df_allo = df_general_time_filter(df_allo, 'start_date', start_date, end_date)
df_allo = df_allo.fillna(0)

ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLU']
validation_allocation(df_allo, ticker_list)


        
# get start aum of each ticket
ticker_df_dict = prepare_ticker_df_dict(df_allo.columns)

aum_ts = build_aum(df_allo, ticker_df_dict)
aum_all_df_merged = aum_ts['all']
aum_ticker_df_merged = aum_ts['ticker']


'''
IO
'''
# path_aum_all_df_merged = "C:/f_data/sector/debug/aum_all_df_merged_dev.csv"
# path_aum_ticker_df_merged = "C:/f_data/sector/debug/aum_ticker_df_merged_dev.csv"

aum_all_df_merged.to_csv(path_out, index=False)
aum_ticker_df_merged.to_csv(path_out_sector, index=False)


'''
Chart
'''
fig = px.line(aum_all_df_merged, x="date", y="ts", title='sector_remix')
fig.show()   

fig_sector = px.scatter(aum_ticker_df_merged, x="date", y="ts", color='ticker', title='sector_remix')
fig_sector.show()   
        
