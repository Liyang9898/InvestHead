'''
Created on Feb 26, 2023

@author: spark
'''

import pandas as pd
from random_research.try_20230224.sector_lib import extract_allocation_by_year
from util.util_finance import get_alpha_beta
from util.util_pandas import df_general_time_filter, dict_to_df, df_to_dict
from util.util_time import date_add_days


def alpha_beta_spy(ticker, period, end_date, duration):
    path_benchmark = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
    path_test = """C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv""".format(ticker=ticker)
    df = pd.read_csv(path_test)
    df_benchmark = pd.read_csv(path_benchmark)
    duration = duration * -1
    start_date = date_add_days(end_date, duration)
    val_col = 'close'
    
    t = ticker + ' ' + start_date + ' ' + end_date
    # print(t)
    ab = get_alpha_beta(df, df_benchmark, val_col, period, start_date, end_date)
    return ab


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


# strategy 2 
def remix2(ticker_list, spy_allocation, signal, order_by='alpha_calibrated'):
    duration = 3*20
    period = 5
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    end_date = signal['end_date']
    
    
    ab_info_list = []
    for ticker in ticker_list:
        ab = alpha_beta_spy(ticker, period, end_date, duration)
        a = ab['alpha']
        b = ab['beta']
        a_calibrated = a/b
        ab['alpha_calibrated'] = a_calibrated
        ab['ticker'] = ticker
        ab_info_list.append(ab)
    df = pd.DataFrame(ab_info_list)
    df = df.sort_values(by=[order_by], ascending=False)
    df.reset_index(drop=True, inplace=True)
    
    title = signal['start_date'] + '_' + signal['end_date']


    # df_allo = dict_to_df(spy_allocation, 'ticker', 'allocation')
    # df_allo = df_allo.sort_values(by=['allocation'], ascending=False)
    # df_allo.reset_index(drop=True, inplace=True)
    # print(df_allo)
    
    allo_l = list(spy_allocation.values())
    allo_l.sort(reverse = True)

    # print(allo_l)
    
    df['allocation'] = allo_l
    
    path_ab = """C:/f_data/sector/ab/{title}.csv""".format(title=title)
    # df.to_csv(path_ab, index=False)
    
    res_allo = df_to_dict(df, 'ticker', 'allocation')
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']        
    return res_allo
    


# get signal file
path = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50.csv"
df_signal = pd.read_csv(path)
start_date = '2016-06-01'
end_date = '2022-01-01'
ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLRE', 'XLU']

df_signal = df_general_time_filter(df_signal, 'date', start_date, end_date)

signals = df_signal.to_dict('records')

allocation_list = []
for signal in signals:
    log = 'processing:' + signal['start_date']
    print(log)
    spy_allocation = extract_allocation_by_year(signal['year'])
    allocation = remix(ticker_list, spy_allocation, signal)
    allocation_list.append(allocation)

res_allo = pd.DataFrame(allocation_list)
print(res_allo)
path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_ranked.csv"
# path_out = "C:/f_data/sector/allocation/allocation_ema21_below_ma50_alpha_calibrated_ranked.csv"
res_allo.to_csv(path_out, index=False)

    
