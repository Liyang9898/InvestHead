'''
Created on Mar 19, 2023

@author: spark
'''
from random_research.try_20230224.helper.memory_data_asset import prepare_ticker_idc_df_dict



def extract_signal(date, signal, ticker_df_dict):
    signals = {}
    for ticker, df in ticker_df_dict.items():
    
        df = df[df['date']==date]
        df=df.copy()
        df.reset_index(inplace=True, drop=True)
        val = df.loc[0, signal]
        signals[ticker] = val
    
    
    sorted_footballers_by_goals = sorted(signals.items(), key=lambda x:x[1], reverse=True)
    res = dict(sorted_footballers_by_goals)
    return res


ticker_list = ['XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLV', 'XLI', 'XLK', 'XLB', 'XLU']
ticker_df_dict = prepare_ticker_idc_df_dict(ticker_list)

date = '2022-01-03'
signal = 'close_pnl_pct_20_bar'

res = extract_signal(date, signal, ticker_df_dict)
for k,v in res.items():
    print(k, str(v))