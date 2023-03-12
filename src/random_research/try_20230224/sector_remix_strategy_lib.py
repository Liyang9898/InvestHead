'''
Created on Mar 4, 2023

@author: spark
'''
import pandas as pd
from util.util_finance import get_alpha_beta
from util.util_pandas import df_to_dict
from util.util_time import date_add_days, df_filter_dy_date


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




def recent_delta_percent(ticker, end_date, duration):
    '''
    this gives you the percent change in past [duration] trading days
    '''

    path_test = """C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv""".format(ticker=ticker)
    df = pd.read_csv(path_test)
    # df_benchmark = pd.read_csv(path_benchmark)
    duration = duration * -1
    start_date = date_add_days(end_date, duration)
    val_col = 'close'
    
    df_filter = df_filter_dy_date(df,'date',start_date,end_date)
    pnl_pct = df_filter.loc[len(df_filter) - 1, val_col] / df_filter.loc[0, val_col] - 1
    
    return pnl_pct


def recent_delta_percent_pre_compute(ticker, end_date, duration):
    '''
    this gives you the percent change in past [duration] trading days
    '''

    path_test = """C:/f_data/sector/indicator_day/{ticker}_1D_fmt_idc.csv""".format(ticker=ticker)
    df = pd.read_csv(path_test)
    # print(end_date)
    # print(df['date'])
    df = df[df['date'] <= end_date]
    df = df.copy()
    trade_date_max = df['date'].max()
    
    df = df[df['date'] == trade_date_max]
    df = df.copy()    
    
    # print(df)
    assert len(df) == 1
    df.reset_index(inplace=True, drop=True)
    pnl_pct = df.loc[0, 'close_pnl_pct_20_bar']
    
    
    return pnl_pct



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
    
    
def remix3(ticker_list, spy_allocation, signal, order_by='alpha_calibrated'):
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
    # res_allo['start_date'] = signal['start_date']
    # res_allo['end_date'] = signal['end_date']        
    # return res_allo


    '''
    delete negative
    '''

    # select
    for ticker in ticker_list:
        delete = signal[ticker]
        allo = res_allo[ticker]
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


def remix4(ticker_list, spy_allocation, signal, order_by='pnl_pct'):
    '''
    1.get the percent increase of the past [duration] of time
    2.rank by 1(1)
    3.reorder the ticker but use same allocation. keep all ticker
    '''
    duration = 3*20
    period = 5
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    end_date = signal['end_date']
    
    
    info_list = []
    for ticker in ticker_list:
        pnl_pct = recent_delta_percent(ticker, end_date, duration)

        x={}
        x['ticker'] = ticker
        x['pnl_pct'] = pnl_pct
        
        info_list.append(x)
    df = pd.DataFrame(info_list)
    df = df.sort_values(by=[order_by], ascending=False)
    df.reset_index(drop=True, inplace=True)
    
    title = signal['start_date'] + '_' + signal['end_date']


    
    allo_l = list(spy_allocation.values())
    allo_l.sort(reverse = True)

    
    df['allocation'] = allo_l

    
    res_allo = df_to_dict(df, 'ticker', 'allocation')
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']        
    return res_allo


def remix5(ticker_list, spy_allocation, signal, order_by='pnl_pct'):
    '''
    1.get the percent increase of the past [duration] of time
    2.rank by 1(1)
    3.reorder the ticker but use same allocation. only keep top x ticker [x = top] 
    4. unify bucket total sum to 1
    '''
    duration = 3*20
    period = 5
    top=3
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    end_date = signal['end_date']
    
    
    info_list = []
    for ticker in ticker_list:
        pnl_pct = recent_delta_percent(ticker, end_date, duration)

        x={}
        x['ticker'] = ticker
        x['pnl_pct'] = pnl_pct
        
        info_list.append(x)
    df = pd.DataFrame(info_list)
    df = df.sort_values(by=[order_by], ascending=False)
    df.reset_index(drop=True, inplace=True)


    # get allocation bucket and attach to the ranked ticker, ranked by past pnl
    allo_l = list(spy_allocation.values())
    allo_l.sort(reverse = True)
    df['allocation'] = allo_l
    
    # get top x
    df = df.iloc[:top]
    df = df.copy()
    # print(df)
    sum = df['allocation'].sum()
    # print(sum)
    
    res_allo = df_to_dict(df, 'ticker', 'allocation')
    
    
    # re scale
    ticker_list = df['ticker'].to_list()
    factor = 1 / sum
    for ticker in ticker_list:
        res_allo[ticker] = res_allo[ticker] * factor

    
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']    
    print(res_allo)    
    return res_allo



def remix6(ticker_list, spy_allocation, signal, order_by='pnl_pct'):
    '''
    1.get the percent increase of the 1 month of time
    2.rank by 1(1)
    3.reorder the ticker but use same allocation. only keep top 3 ticker  
    4. unify bucket total sum to 1
    '''
    duration = 1*20
    period = 5
    top=3
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    end_date = signal['end_date']
    
    
    info_list = []
    for ticker in ticker_list:
        pnl_pct = recent_delta_percent(ticker, end_date, duration)

        x={}
        x['ticker'] = ticker
        x['pnl_pct'] = pnl_pct
        
        info_list.append(x)
    df = pd.DataFrame(info_list)
    df = df.sort_values(by=[order_by], ascending=False)
    df.reset_index(drop=True, inplace=True)


    # get allocation bucket and attach to the ranked ticker, ranked by past pnl
    spy_allocation_keys = list(spy_allocation.keys()).copy()
    for t in spy_allocation_keys:
        if t not in ticker_list:
            del spy_allocation[t]
    allo_l = list(spy_allocation.values())
    allo_l.sort(reverse = True)
    df['allocation'] = allo_l
    
    # get top x
    df = df.iloc[:top]
    df = df.copy()
    # print(df)
    sum = df['allocation'].sum()
    # print(sum)
    
    res_allo = df_to_dict(df, 'ticker', 'allocation')
    
    
    # re scale
    ticker_list = df['ticker'].to_list()
    factor = 1 / sum
    for ticker in ticker_list:
        res_allo[ticker] = res_allo[ticker] * factor

    
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']    
    print(res_allo)    
    return res_allo


def remix6_5(ticker_list, spy_allocation, signal, order_by='pnl_pct'):
    '''
    1.get the percent increase of the 1 month of time
    2.rank by 1(1)
    3.reorder the ticker but use same allocation. only keep top 3 ticker  
    4. unify bucket total sum to 1
    '''
    duration = 1*20
    period = 5
    top=3
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    end_date = signal['end_date']
    
    
    info_list = []
    for ticker in ticker_list:
        pnl_pct = recent_delta_percent_pre_compute(ticker, end_date, duration)

        x={}
        x['ticker'] = ticker
        x['pnl_pct'] = pnl_pct
        
        info_list.append(x)
    df = pd.DataFrame(info_list)
    df = df.sort_values(by=[order_by], ascending=False)
    df.reset_index(drop=True, inplace=True)


    # get allocation bucket and attach to the ranked ticker, ranked by past pnl
    spy_allocation_keys = list(spy_allocation.keys()).copy()
    for t in spy_allocation_keys:
        if t not in ticker_list:
            del spy_allocation[t]
    allo_l = list(spy_allocation.values())
    allo_l.sort(reverse = True)
    df['allocation'] = allo_l
    
    # get top x
    df = df.iloc[:top]
    df = df.copy()
    # print(df)
    sum = df['allocation'].sum()
    # print(sum)
    
    res_allo = df_to_dict(df, 'ticker', 'allocation')
    
    
    # re scale
    ticker_list = df['ticker'].to_list()
    factor = 1 / sum
    for ticker in ticker_list:
        res_allo[ticker] = res_allo[ticker] * factor

    
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']    
    print(res_allo)    
    return res_allo


def remix7(ticker_list, spy_allocation, signal, order_by='pnl_pct'):
    '''
    1.get the percent increase of the 1 month of time
    2.rank by 1(1)
    3.reorder the ticker but use same allocation. only keep top 3 ticker  
    4. unify bucket total sum to 1
    '''
    duration = 1*20
    period = 5
    top=3
    '''
    this convert a spy allocation dict<key=ticker,val=allocation> into a new one based on signal
    '''
    res_allo = {}
    sum = 0
    # select
    end_date = signal['end_date']
    
    
    info_list = []
    for ticker in ticker_list:
        pnl_pct = recent_delta_percent(ticker, end_date, duration)

        x={}
        x['ticker'] = ticker
        x['pnl_pct'] = pnl_pct
        
        info_list.append(x)
    df = pd.DataFrame(info_list)
    df = df.sort_values(by=[order_by], ascending=False)
    df.reset_index(drop=True, inplace=True)


    # get allocation bucket and attach to the ranked ticker, ranked by past pnl
    spy_allocation_keys = list(spy_allocation.keys()).copy()
    for t in spy_allocation_keys:
        if t not in ticker_list:
            del spy_allocation[t]
    allo_l = list(spy_allocation.values())
    allo_l.sort(reverse = True)
    df['allocation'] = allo_l
    
    # get top x
    df = df.iloc[:top]
    df = df.copy()
    df = df[df['pnl_pct']>0]
    df = df.copy()
    print(df)
    sum = df['allocation'].sum()

    # print(sum)
    
    res_allo = df_to_dict(df, 'ticker', 'allocation')  
    
    # re scale
    ticker_list = df['ticker'].to_list()
    
    if sum != 0:
        factor = 1 / sum
        for ticker in ticker_list:
            res_allo[ticker] = res_allo[ticker] * factor
    else:
        return {}
    
    res_allo['start_date'] = signal['start_date']
    res_allo['end_date'] = signal['end_date']    
   
    return res_allo