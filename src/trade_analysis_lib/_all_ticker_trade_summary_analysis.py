'''
Created on Jun 9, 2020

@author: leon
'''
from util import util
from indicator_master.constant import trade_summary_interface

# ticker above half million
vol_map=util.get_volume_map()
ticker_above_half_million=util.get_ticker_larger_than_vol(500000, vol_map)
print(str(len(ticker_above_half_million))+' ticker above 0.5 M daily avg volume')


all_stocks_trade_summary_file="D:/f_data/download_yfinance_trades_summary_conclusion/trade_summaries.csv"
df=util.load_df_from_csv(all_stocks_trade_summary_file, ['ticker','avg_daily_volumn']+trade_summary_interface)

df = df.loc[(df['avg_daily_volumn'] > 0.5 *1000000)]

print("total stock: "+str(len(df)))

df = df.loc[(df['total_trades']>0)]
print("total stock has trades: "+str(len(df)))

df_positive_win_rate_st = df.loc[(df['win_rate']>df['lose_rate'])]
print("total stock has positive win rate: "+str(len(df_positive_win_rate_st)))

df_positive_win_pnl_p_st = df.loc[(df['win_pnl_p']>df['lose_pnl_p'])]
print("total stock has positive win pnl %(makes money): "+str(len(df_positive_win_pnl_p_st)))
