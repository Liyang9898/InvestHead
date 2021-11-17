'''
Created on Jan 10, 2021

@author: leon
'''

import pandas as pd

trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210126/20210126_21_50_channel_controlled_enter.csv"
output = "D:/f_data/sweep_20201214/conclusion_filtered/20210126_2b_1m_10trade_60win_positive_iwf_channel_controlled_enter.csv"
iwf = "D:/f_data/etf/iwf_20210115.csv"
stocks_trade_summary = pd.read_csv(trade_summary_bundle_path)
iwf_df = pd.read_csv(iwf)
iwf_list = list(iwf_df['ticker'])
print(iwf_list)
print(stocks_trade_summary)
blacklist = [
    'QQQ',
    'SQQQ',
    'TQQQ',
]
market_cap_threshold = 2000000000
volume_threshold= 1000000
anual_pnl = 0.06

# stock feature
stocks_trade_summary=stocks_trade_summary.loc[~stocks_trade_summary['ticker'].isin(blacklist)]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['ticker'].isin(iwf_list)]
# stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['MarketCapNum']>market_cap_threshold]
# stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['vol']>volume_threshold]

#performance
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['all_universe_win_rate']>0.6]#6/4 win rate happy
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_trades']>=10] # 5 year inflate 10%
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_pnl_fix']>=anual_pnl*5]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['total_pnl_rollover']>=anual_pnl*5]
stocks_trade_summary=stocks_trade_summary.loc[(stocks_trade_summary['all_universe_win_pnl_p']+stocks_trade_summary['all_universe_lose_pnl_p'])>0]
stocks_trade_summary=stocks_trade_summary.loc[stocks_trade_summary['ma50_up_rate']>0.60]

# try have better total_pnl_fix and total_pnl_rollover
#write result
print(stocks_trade_summary)
stocks_trade_summary.to_csv(output)