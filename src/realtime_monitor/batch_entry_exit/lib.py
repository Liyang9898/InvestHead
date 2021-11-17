'''
Created on Jan 3, 2021

@author: leon
'''
from trading_floor.gen_trades import gen_entries
from strategy_lib.strat_ma_8_21spy import StrategySimpleMA as StrategySimpleMA_8_21
from strategy_lib.strat_ma_21_50spy import StrategySimpleMA as StrategySimpleMA_21_50
import os
import pandas as pd


def append_entry_in_df(df_indicator,ma,strategy_param_bundle):

    strategy=None
    if ma is "8_21":
        strategy=StrategySimpleMA_8_21(strategy_param_bundle)
    elif ma is "21_50":
        strategy=StrategySimpleMA_21_50(strategy_param_bundle)
        
    entires = gen_entries(df=df_indicator, strategy=strategy)
    rows = []
    for entry in entires:
        row = {
            'est_datetime':entry['entry_ts'],
            'entry_price':entry['entry_price'],
        }
        rows.append(row)
    df_entry = pd.DataFrame(rows) 
#     print(df_entry)
    df_with_entry=df_indicator.merge(df_entry, on='est_datetime', how='left')
    print(df_with_entry['entry_price'])
    return df_with_entry

def batch_entries(ma,strategy_param_bundle, path_in,path_out):
    cnt = 1
#     entires_list = {}
    for file in os.listdir(path_in):
        if file.endswith(".csv"):
    #     if file=="V_download_format.csv":
            print(cnt,'  ' ,file)
            ticker = file.split('_')[0]
            strategy=None
            if ma is "8_21":
                strategy=StrategySimpleMA_8_21(strategy_param_bundle)
            elif ma is "21_50":
                strategy=StrategySimpleMA_21_50(strategy_param_bundle)
                
            price_with_indicator = pd.read_csv(path_in+ticker+'_downloaded_raw.csv')
            df_with_trades = append_entry_in_df(price_with_indicator,ma,strategy_param_bundle)
            print(df_with_trades['est_datetime'])
            df_with_trades.to_csv(path_out+ticker+'.csv',index = False)

            cnt=cnt+1
#     return entires_list
