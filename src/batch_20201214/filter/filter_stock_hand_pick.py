'''
Created on Dec 25, 2020

@author: leon
'''
import pandas as pd

trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion/ma21_50_with_profit_manage_201612_202012.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
print(stocks_trade_summary)
whitelist = [
    'GOOG',
    'FB',
    'MSFT',
    'AMZN',
    'AAPL',
    
    'NVDA',
    'AMD',
    'V',
    'NFLX',
    'JD'
]
market_cap_threshold = 1000000
volume_threshold= 1000000

# stock feature
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['ticker'].isin(whitelist)]


#write result
stocks_trade_summary.to_csv("D:/f_data/sweep_20201214/conclusion_filtered/ma21_50_with_profit_manage_201612_202012_hand_pick.csv")