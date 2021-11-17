'''
Created on Jan 10, 2021

@author: leon
'''

import pandas as pd

trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210108/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210110.csv"
output = "D:/f_data/sweep_20201214/conclusion_filtered/20210113_03b_1m.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
print(stocks_trade_summary)
blacklist = [
    'QQQ',
    'SQQQ',
    'TQQQ',
]
market_cap_threshold = 3000000
volume_threshold= 1000000

# stock feature
stocks_trade_summary=stocks_trade_summary.loc[~stocks_trade_summary['ticker'].isin(blacklist)]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['MarketCapNum']>market_cap_threshold]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['vol']>volume_threshold]

#performance
# stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_rate']>0.2]#6/4 win rate happy
# stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_pnl_fix']>0.1] # 5 year inflate 10%
# stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_pnl_rollover']>0.1]

#write result
print(stocks_trade_summary)
stocks_trade_summary.to_csv(output)