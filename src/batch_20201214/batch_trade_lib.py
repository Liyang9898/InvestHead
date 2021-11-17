'''
Created on Dec 24, 2020

@author: leon
'''

from _overlapped import NULL
import os

from pandas._libs import index

from batch_20201214.util_for_batch.batch_util import check_ticker_exist
from indicator_master.create_indicator_api_main import price_csv_append_indicator
from indicator_master.indicator_caching_lib import csv2df_indicator
from indicator_master.indicator_compute_lib import tsfilter
import pandas as pd
from strategy_lib.param_per_ticker.lib import get_param_ema21_ma50_gap
from strategy_lib.strat_ma_swing import StrategySimpleMA
from trading_floor.TradeInterface import genTradingBundleFromCSV
from trading_floor.TradeInterface import merge_trade_summary, merged_result_to_csv
from trading_floor.gen_trades import gen_trades


# strat_ma_trend_20200707
# from batch_20201214.reveal_trades import trades_consecutive
# from batch_20201214 import cash_history_lib
# from plotting_lib.simple import plotTimeSerisDic,plotTimeSerisDic3 
# from trade_analysis_lib.cash_position_tool import genPositionHistory
# def check_ticker_exist(path,ticker):
#     for file in os.listdir(path):
#         if not file.endswith(".csv"):
#             continue
#         
#         # extract ticker
#         t = file.split('_')[0]
#         if t == ticker:
#             return True
#     return False
def single_trade_pull_result(
    ticker,
    trade_summary_path, 
    trade_detail_path,
):
    trades_consecutive_path=trade_detail_path+'/'+ticker+'_consecutive.csv'
    trades_all_entry_path=trade_detail_path+'/'+ticker+'_all_entry.csv'
    
    trades_consecutive_bundle = genTradingBundleFromCSV(trades_consecutive_path)
    trades_all_entry_bundle = genTradingBundleFromCSV(trades_all_entry_path)
    if trades_consecutive_bundle == None or trades_all_entry_bundle == None:
        return None
    
    over_all_summary = merge_trade_summary(
        trades_consecutive_bundle.tradeSummary2dict(),
        trades_all_entry_bundle.tradeSummary2dict()
    )
    merged_result_to_csv(over_all_summary, trade_summary_path)
    return trades_consecutive_bundle
    

def single_trade(
    ticker,
    price_with_indicator_file_path, 
    trade_summary_path, 
    trade_detail_path,
    ma, 
    strategy_param_bundle,
    start_time,
    end_time,
    trades_consecutive_to_csv=True,
    trades_all_entry_to_csv=True,
    pull_result=False
):
    if pull_result:
        res = single_trade_pull_result(
            ticker,
            trade_summary_path, 
            trade_detail_path,
        )
        return res
    df = csv2df_indicator(price_with_indicator_file_path)
 
    price_with_indicator = tsfilter(df,start_time,end_time)
    
    res = gen_trades_based_on_price_with_indicator(
        ticker,
        price_with_indicator, 
        ma, 
        strategy_param_bundle,
    )
    trades_consecutive = res['trades_consecutive']
    trades_all_entry = res['trades_all_entry']
    if trades_consecutive_to_csv:
        trades_consecutive_path=trade_detail_path+'/'+ticker+'_consecutive.csv'
        trades_consecutive.trades2CSV(trades_consecutive_path)
  
    if trades_all_entry_to_csv:
        trades_all_entry_path=trade_detail_path+'/'+ticker+'_all_entry.csv'
        trades_all_entry.trades2CSV(trades_all_entry_path)
     
#     trades.tradeSummary2CSV(trade_summary_path)
     
    over_all_summary = merge_trade_summary(res['trades_consecutive'].tradeSummary2dict(),res['trades_all_entry'].tradeSummary2dict())
    merged_result_to_csv(over_all_summary, trade_summary_path)
    return trades_consecutive


def gen_trades_based_on_price_with_indicator(
    ticker,
    price_with_indicator, 
    strategy_param_bundle,
):

    # set up ticker specific strategy parameter
    if 'ema21_ma50_gap_percent_threshold' in strategy_param_bundle.keys():
        param = get_param_ema21_ma50_gap(ticker)
        if param is not None:
            strategy_param_bundle['ema21_ma50_gap_percent_threshold'] = param
        else: 
            # this is equivalent to not having this signal 
            strategy_param_bundle['ema21_ma50_gap_percent_threshold'] = 0.0
        print('===============set up ema21_ma50_gap_percent_threshold = ', strategy_param_bundle['ema21_ma50_gap_percent_threshold'])
        
    strategy=StrategySimpleMA(strategy_param_bundle)
        
    trades_consecutive = gen_trades(df=price_with_indicator, strategy=strategy, all_bar_entry=False)
    trades_all_entry = gen_trades(df=price_with_indicator, strategy=strategy, all_bar_entry=True)

    return {
        'trades_consecutive': trades_consecutive,
        'trades_all_entry': trades_all_entry
    }

# batch_trade_lopper(
#     folder_path_price_with_indicator, 
#     folder_path_trade_results, 
#     trade_detail_path,
#     ma, 
#     strategy_param_bundle,
#     start_time,
#     end_time,
#     ticker_list = None
# )
    
def batch_trade_lopper(
    folder_path_price_with_indicator, 
    folder_path_trade_results, 
    trade_detail_path,
    ma, 
    strategy_param_bundle,
    start_time,
    end_time,
    ticker_list = None
):   
    cnt = 1
    for file in os.listdir(folder_path_price_with_indicator):
        if not file.endswith(".csv"):
            continue
#         if not (file=="V_download_format.csv"):
#             continue 
        # extract ticker
        ticker = file.split('_')[0]
        print('processing:', cnt,'  ' ,ticker) 
        if ticker_list is not None and ticker not in ticker_list:
            print(ticker, 'filter out')
            cnt=cnt+1    
            continue
        #check exist
        exist = check_ticker_exist(folder_path_trade_results,ticker)
        if exist:
            print(ticker, 'trading results already exist')
        else:
            price_with_indicator_file_path=folder_path_price_with_indicator+file
            trade_summary_path=folder_path_trade_results+ticker+'_trade_summary.csv'
            
            single_trade(
                ticker,
                price_with_indicator_file_path, 
                trade_summary_path, 
                trade_detail_path,
                ma, 
                strategy_param_bundle,
                start_time,
                end_time
            )
            
        cnt=cnt+1    
    