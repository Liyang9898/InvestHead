'''
Created on Dec 25, 2020

@author: leon
'''
import pandas as pd
from indicator_master.indicator_caching_lib import csv2df_indicator
from batch_20201214.batch_trade_lib import single_trade, single_trade_pull_result
from trade_analysis_lib.cash_position_tool import genPositionHistory
from trade_analysis_lib import cash_position_tool
from plotting_lib.simple import plotTimeSerisDic,plotTimeSerisDic3 
from version_master.version import (
    indicator_20210301,
    trade_swing_smooth_prod_20210221
)
from batch_20201214.util_for_batch.batch_util import get_all_files


def gen_cash_history(
    ticker,
    trade_path,
    indicator_path,
    start_time,
    end_time
):
    price_with_indicator_file_path = indicator_path + ticker + '_downloaded_raw.csv'
    trade_summary_path = "D:/f_data/dump/"+ticker
    trade_detail_path=trade_path + "detail"
    

    
    df_price_indicator = csv2df_indicator(price_with_indicator_file_path)

#     trade_bundle = single_trade(
#         ticker,
#         price_with_indicator_file_path, 
#         trade_summary_path, 
#         trade_detail_path,
#         ma, 
#         strategy_param_bundle,
#         start_time,
#         end_time
#     )
    
    trade_bundle = single_trade_pull_result(
        ticker,
        trade_summary_path, 
        trade_detail_path,
    )
    if trade_bundle == None:
        return None
    
    trades = trade_bundle.trades
    cash_history = genPositionHistory(df_price_indicator, trades, start_time, end_time)
    return cash_history

def add_dic(d1,d2):
    res = {}
    for k,v in d1.items():
        if k in d2.keys(): # overlap
            res[k] = d1[k]+d2[k]
        else: # d1 only
            res[k] = d1[k]
    for k,v in d2.items():
        if k not in d1.keys(): # d2 only
            res[k] = d2[k]
    return res

def normalize(dic):
    first = list(dic.values())[0]
    for t, val in dic.items():
        dic[t] = val / first
    return dic

def gen_cash_history_agg(
    trade_path,
    indicator_path,
    start_time,
    end_time
):
    file_dic = get_all_files(trade_path+'detail/')
    ticker_list = list(file_dic.keys())
#     print(len(ticker_list))
    
    bundle = {}
    cnt = 1
    for ticker in ticker_list:
#         print(cnt, ticker)
        bundle[ticker] = gen_cash_history(
            ticker,
            trade_path,
            indicator_path,
            start_time,
            end_time
        )

        cnt = cnt + 1

    res = {
        'price_position':{},
        'cash_rollover_position':{},
        'cash_fixed_base_position':{},
    }
#     print(bundle)
    for ticker, history in bundle.items():
        if history is None:
            continue
        res['price_position']=add_dic(res['price_position'], history['price_position'])
        res['cash_rollover_position']=add_dic(res['cash_rollover_position'], history['cash_rollover_position'])
        res['cash_fixed_base_position']=add_dic(res['cash_fixed_base_position'], history['cash_fixed_base_position'])
    
    res['price_position']=normalize(res['price_position'])
    res['cash_rollover_position']=normalize(res['cash_rollover_position'])
    res['cash_fixed_base_position']=normalize(res['cash_fixed_base_position'])
    return res