'''
Created on Feb 26, 2023

@author: spark
'''
####################################################################################################
####################################################################################################
####################################################################################################
# start_date = '2016-06-01'
# end_date = '2024-01-01'
# ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLRE', 'XLU']
# # get signal file
# path = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50.csv"
# df_signal = pd.read_csv(path)
########################################## REMOVE XLRE ##############################################
'''
real estite start on 2016, while others start on 1999, this is a bottle neck
since real estate is around 1-3% all the time, we ignore it
'''

import pandas as pd
from random_research.try_20230224.helper.memory_data_asset import prepare_ticker_df_dict, \
    prepare_ticker_idc_df_dict
from random_research.try_20230224.sector_lib import extract_allocation_by_year
from random_research.try_20230224.sector_remix_strategy_lib import remix5, \
    remix6, remix7, remix6_5, remix4, remix
from util.util_finance import get_alpha_beta
from util.util_pandas import df_general_time_filter, dict_to_df, df_to_dict
from util.util_time import date_add_days, df_filter_dy_date


start_date = '2005-06-01'
# start_date = '2023-01-01'
end_date = '2023-02-15'
ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLU']
# get signal file

####################################################################################################
####################################################################################################
####################################################################################################
'''
# for using swing segment
'''
# path = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50.csv"

####################################################################################################
#######################################  choose one   ##############################################
####################################################################################################

'''
# for using weekly update
'''
path = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50_weekly.csv"
####################################################################################################
####################################################################################################
####################################################################################################

df_signal = pd.read_csv(path)
if 'XLRE' in df_signal.columns:
    df_signal.drop(['XLRE'], axis=1)

####################################################################################################
####################################################################################################
####################################################################################################

################### in memory data asset ###################
   
# get start aum of each ticket
ticker_df_dict = prepare_ticker_idc_df_dict(ticker_list)

################### in memory data asset ###################

df_signal = df_general_time_filter(df_signal, 'date', start_date, end_date)

signals = df_signal.to_dict('records')
log_df = pd.DataFrame(columns = ['ticker', 'date', 'signal'])

allocation_list = []
for signal in signals:   
    # signal is a dict with cols (date, start_date,end_date,year, changed, xlk,xlf.....)  date = start_date
    # only 3 columns works (start_date,end_date,year)
    log = 'processing:' + signal['start_date']
    print(log)
    spy_allocation = extract_allocation_by_year(signal['year'])
    
    allocation = remix(ticker_list, spy_allocation, signal) # for version besides 6_5
    
    # allocation = remix6_5(ticker_list=ticker_list, spy_allocation=spy_allocation, signal=signal, order_by='pnl_pct', ticker_df_dict=ticker_df_dict, log_df=log_df)
    
    print(allocation)
    
    if len(allocation) <= 2: # check if there are zero allocations, there are only 2 date cols if there is 0 allocaiton
        continue
    
    allocation_list.append(allocation)

res_allo = pd.DataFrame(allocation_list)
print(res_allo)
path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_ranked_top3.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute.csv"
# path_out = "C:/f_data/sector/allocation/weekly_allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_precompute.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3_increase_only.csv"
res_allo.to_csv(path_out, index=False)

    
