'''
Created on Dec 30, 2020

@author: leon
'''
from batch_20201214.util_for_batch.reveal_trade_lib import reveal_trade
import pandas as pd

trade_summary_bundle_path=trade_summary_bundle_path = "D:/f_data/sweep_20201214/edit/csv/20210110_straght_line_growth_us.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
ticker_list = list(stocks_trade_summary['ticker'])
print(ticker_list)

cnt = 1
start = 1
for ticker in ticker_list:
    if cnt >= start and cnt <= start+5:
        print(ticker)
        reveal_trade(ticker)
    cnt = cnt + 1
    
