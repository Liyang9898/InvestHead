'''
Created on Dec 25, 2020

@author: leon
'''
import pandas as pd

trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion/ma21_50_with_profit_manage_no_neutral_out_201612_202012.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
print(stocks_trade_summary)
blacklist = [
    'QQQ',
    'SQQQ',
    'TQQQ',
]
market_cap_threshold = 1000000000
volume_threshold= 5000000

# stock feature
stocks_trade_summary=stocks_trade_summary.loc[~stocks_trade_summary['ticker'].isin(blacklist)]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['MarketCapNum']>market_cap_threshold]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['vol']>volume_threshold]

#performance
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_rate']>0.2]#6/4 win rate happy
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_pnl_fix']>2.8] # 5 year inflate 10%
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_pnl_rollover']>2.8]

print(len(stocks_trade_summary))
print(stocks_trade_summary)

#write result
stocks_trade_summary.to_csv("D:/f_data/sweep_20201214/conclusion_filtered/ma21_50_with_profit_manage_no_neutral_out_201612_202012_tier.csv")