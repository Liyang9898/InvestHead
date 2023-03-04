'''
Created on Feb 26, 2023

@author: spark
'''

import pandas as pd
from random_research.try_20230224.sector_lib import extract_allocation_by_year
from random_research.try_20230224.sector_remix_strategy_lib import remix5, \
    remix6
from util.util_finance import get_alpha_beta
from util.util_pandas import df_general_time_filter, dict_to_df, df_to_dict
from util.util_time import date_add_days, df_filter_dy_date


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
start_date = '2005-06-01'
end_date = '2024-01-01'
ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLU']
# get signal file
path = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50.csv"
df_signal = pd.read_csv(path)
if 'XLRE' in df_signal.columns:
    df_signal.drop(['XLRE'], axis=1)

####################################################################################################
####################################################################################################
####################################################################################################





df_signal = df_general_time_filter(df_signal, 'date', start_date, end_date)

signals = df_signal.to_dict('records')

allocation_list = []
for signal in signals:
    log = 'processing:' + signal['start_date']
    print(log)
    spy_allocation = extract_allocation_by_year(signal['year'])
    allocation = remix6(ticker_list, spy_allocation, signal)
    allocation_list.append(allocation)

res_allo = pd.DataFrame(allocation_list)
print(res_allo)
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked_delete_neg.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_ranked_top3.csv"
path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_recent_pnl_past_1_month_ranked_top3.csv"
res_allo.to_csv(path_out, index=False)

    
