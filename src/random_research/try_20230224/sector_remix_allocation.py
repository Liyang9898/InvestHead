'''
Created on Feb 26, 2023

@author: spark
'''

import pandas as pd
from random_research.try_20230224.sector_lib import extract_allocation_by_year
from util.util_pandas import df_general_time_filter


# strategy
def remix(ticker_list, spy_allocation, signal):
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    for ticker in ticker_list:
        delete = signal[ticker]
        allo = spy_allocation[ticker]
        if delete == 1:
            res_allo[ticker] = 0
        else:
            res_allo[ticker] = allo
            sum = sum + allo
    
    
    # re scale
    factor = 1 / sum
    for ticker in ticker_list:
        res_allo[ticker] = res_allo[ticker] * factor
    
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']
    
    return res_allo


# get signal file
path = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50.csv"
df_signal = pd.read_csv(path)
start_date = '2016-01-01'
end_date = '2022-01-01'
ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLRE', 'XLU']

df_signal = df_general_time_filter(df_signal, 'date', start_date, end_date)

signals = df_signal.to_dict('records')

allocation_list = []
for signal in signals:
    spy_allocation = extract_allocation_by_year(signal['year'])
    allocation = remix(ticker_list, spy_allocation, signal)
    allocation_list.append(allocation)

res_allo = pd.DataFrame(allocation_list)
print(res_allo)
path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50.csv"
res_allo.to_csv(path_out, index=False)

    
