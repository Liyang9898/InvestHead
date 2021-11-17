'''
Created on Jun 16, 2020

@author: leon
'''
from indicator_master.indicator_caching_lib import csv2df_indicator


from util import util

# from strategy_lib.strat_ma_trend_20200604 import gen_strategy_bundles,StrategySimpleMAFactory
from indicator_master.indicator_compute_lib import tsfilter
from strategy_param_sweep.strategy_param_sweep_lib import strategy_param_sweep
from trade_analysis_lib.sweep_result_select import valid_strategy_param_exist

stock_ticker_with_indicator_folder="D:/f_data/download_yfinance_trades_summary_params_sweep/"
filepath_list=util.get_all_csv_file_path_from_folder(stock_ticker_with_indicator_folder)
print("found "+ str(len(filepath_list))+" ticker with indicator files")

total_rate = 0.2
lose_rate=0.01

cnt = 0

valid_result = []
for ticker, file in filepath_list.items():
    cnt = cnt + 1
    ticker_name=util.extract_symbol_name(ticker)
    valid = valid_strategy_param_exist(file, total_rate, lose_rate)
#     print(ticker_name+' '+str(valid))
    if valid:
        valid_result.append(ticker_name)
    
print(str(len(valid_result))+" ticker satisfy the condition, win rate-lose rate>"+str(total_rate)+" lose_rate<"+str(lose_rate))
    