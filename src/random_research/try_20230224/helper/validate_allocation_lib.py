'''
Created on Mar 11, 2023

@author: spark
'''

from util.util_time import days_gap_date_str


def validation_allocation(df, ticker_list):
    '''
    validate:
    1. has start_date, end_date, and all col in ticker_list
    2. start, end date no gap/overlap
    3. in each row, all cols value sums up to 1
    '''
    assert not df.isnull().values.any()
    
    # validate:1. has start_date, end_date, and all col in ticker_list
    assert 'start_date' in df.columns
    assert 'end_date' in df.columns
    for ticker in ticker_list:
        assert ticker in df.columns
    assert len(df.columns) == 2 + len(ticker_list)
    
    pre_end_date = ''
    for i in range(0, len(df)):
        start_date = df.loc[i, 'start_date']
        end_date = df.loc[i, 'end_date']
        
        if i > 0:
            # 2. start, end date no gap/overlap
            gap = days_gap_date_str(pre_end_date, start_date)
            assert gap >= 1
        
        sum = 0
        for ticker in ticker_list:
            # validate:3. in each row, all cols value sums up to 1
            sum = sum + df.loc[i, ticker]

        assert abs(1 - sum) < 0.02
        
        pre_end_date = end_date
        
        
