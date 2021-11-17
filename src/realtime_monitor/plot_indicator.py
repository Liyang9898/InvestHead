'''
Created on Jan 3, 2021

@author: leon
'''
from indicator_master.indicator_compute_lib import tsfilter
from indicator_master.plot_indicator_lib import plot_indicator
import pandas as pd


folder_path_price_with_indicator = "D:/f_data/reatime_monitor/stock_indicator/"
ticker = 'FB'
df = pd.read_csv(folder_path_price_with_indicator+ticker+'_downloaded_raw.csv')
print(df)
start_time = '2019-01-01'
end_time = '2021-01-01'

price_with_indicator = tsfilter(df,start_time,end_time)

# plot raw price with indicator
plot_indicator(price_with_indicator, 'sequence_8_21_50',ticker)