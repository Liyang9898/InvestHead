'''
Created on Dec 25, 2020

@author: leon
'''
import pandas as pd

trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion/ma8_21_no_profit_manage_201612_202012.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
print(stocks_trade_summary)
blacklist = [
    'QQQ',
    'SQQQ',
    'TQQQ',
]
market_cap_threshold = 1000000
volume_threshold= 1000000

# stock feature
stocks_trade_summary=stocks_trade_summary.loc[~stocks_trade_summary['ticker'].isin(blacklist)]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['MarketCapNum']>market_cap_threshold]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['vol']>volume_threshold]

#performance
stocks_trade_summary=stocks_trade_summary.sort_values(by=['vol'], ascending=False)
stocks_trade_summary=stocks_trade_summary.head(50)

#write result
stocks_trade_summary.to_csv("D:/f_data/sweep_20201214/conclusion_filtered/ma8_21_no_profit_manage_201612_202012_filtered_top50vol.csv")