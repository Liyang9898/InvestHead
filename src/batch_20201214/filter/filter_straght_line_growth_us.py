'''
Created on Jan 11, 2021

@author: leon
'''

import pandas as pd

trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210108/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210110.csv"
output = "D:/f_data/sweep_20201214/conclusion_filtered/20210110_straght_line_growth_us.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
print(stocks_trade_summary)
blacklist = [
    'QQQ',
    'SQQQ',
    'TQQQ',
]
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
    'MA'
]
market_cap_threshold = 3000000
volume_threshold= 1000000

# stock feature
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['ticker'].isin(whitelist)]

#write result
stocks_trade_summary.to_csv(output)