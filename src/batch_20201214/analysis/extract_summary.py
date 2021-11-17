'''
Created on Feb 3, 2021

@author: leon
'''
import pandas as pd
# input_path = "D:/f_data/sweep_20201214/filtered/20210117_2b_1m_10trade_60win_positive_iwf.csv"
# input_path = "D:/f_data/sweep_20201214/filtered/20210130_21_50_channel_only_50in75out_filter_iwf200.csv"
# input_path = "D:/f_data/sweep_20201214/filtered/20210201_8_21_channel_only_50in75out_filter_iwf200.csv"
input_path = "D:/f_data/sweep_20201214/filtered/20210209_ribbon_start.csv"

trading_result = pd.read_csv(input_path)
# print(trading_result)
# print(trading_result.columns)
# avg_all = trading_result.mean().reset_index()
# print(avg_all)

all_u_avg_win_rate = trading_result['all_universe_win_rate'].mean()
all_u_avg_lose_rate = trading_result['all_universe_lose_rate'].mean()
fix = trading_result['total_pnl_fix'].mean()
roll = trading_result['total_pnl_rollover'].mean()
win_size = trading_result['average_trade_win_pnl_p'].mean()
lose_size = trading_result['average_trade_lose_pnl_p'].mean()
ratio = trading_result['each_trade_win_lose_rate'].mean()
total_trades = trading_result['total_trades'].mean()

# print(all_u_avg_win_rate,all_u_avg_lose_rate,fix,roll,win_size,lose_size,ratio,total_trades)

dic = {
    'all_u_avg_win_rate':all_u_avg_win_rate,
    'all_u_avg_lose_rate':all_u_avg_lose_rate,
    'fix':fix,
    'roll':roll,
    'win_size':win_size,
    'lose_size':lose_size,
    'ratio':ratio,
    'total_trades':total_trades
}

for k,v in dic.items():
    print(k,v)