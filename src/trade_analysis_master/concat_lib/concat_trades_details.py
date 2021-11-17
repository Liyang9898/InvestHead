'''
Created on Feb 21, 2021

@author: leon
'''
import os

import pandas as pd
from util.util import holding_days


def concat_trade_all(trade_path):
    concat_trade_detail(
        trade_detail_path=trade_path+'detail/', 
        output_path=trade_path+'merge/all_trades_all_entry.csv', 
        file_post_fix="_all_entry.csv"
    )
    print('written to:', trade_path+'merge/all_trades_all_entry.csv')
    
    concat_trade_detail(
        trade_detail_path=trade_path+'detail/', 
        output_path=trade_path+'merge/all_trades_consecutive.csv', 
        file_post_fix="_consecutive.csv"
    )
    print('written to:', trade_path+'merge/all_trades_consecutive.csv')
    

def concat_trade_detail(trade_detail_path, output_path, file_post_fix):
    dfs = []
    cnt = 1
    empty_cnt = 1
    for file in os.listdir(trade_detail_path):
        if not file.endswith(file_post_fix):
            continue
          
        # extract ticker
        ticker = file.split('_')[0]
        
        # read data
        path = trade_detail_path+file

        try:
            df = pd.read_csv(path)
            df['ticker'] = ticker
            df['holding_days'] = df.apply(lambda row : holding_days(row['entry_ts'], row['exit_ts']), axis = 1)
            dfs.append(df)
        except:
            empty_cnt = empty_cnt + 1
            continue

#         print(cnt, empty_cnt, ticker)
        cnt = cnt + 1
    df_merged = pd.concat(dfs)    
    df_merged.to_csv(output_path, index=False)
    

def join_trades_with_indicator(trade_path, indicator_path, output_path):
    df_trade = pd.read_csv(trade_path)
    df_indicator = pd.read_csv(indicator_path)
    
    
    merged_df = df_trade.merge(df_indicator, how='left', left_on=["ticker", "entry_ts"], right_on=["ticker","est_datetime"])
    
    merged_df.to_csv(output_path)

    assert len(df_trade) == len(merged_df)
    