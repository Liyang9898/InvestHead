'''
Created on Mar 14, 2021

@author: leon
'''
from datetime import datetime, timedelta 
from batch_20201214.util_for_batch.batch_util import get_all_files, \
    get_all_all_entry_files
from version_master.version import (
    indicator_20210301,
    trade_swing_2150in_2150out_20210313_iwf_channel_in
)
import pandas as pd


# trade_path = trade_swing_2150in_2150out_20210313_iwf_channel_in
# indicator_path = indicator_20210301
# feature_sub_path = trade_path + 'feature/'


def trade_date(x):
    b= x.split(' ')[0]
    dt = datetime.strptime(b, "%Y-%m-%d")
    return dt.strftime("%Y-%m-%d")

def indicator_date(x):
    b= x.split(' ')[0]
    dt = datetime.strptime(b, "%Y-%m-%d")
    dt_yesterday = dt + timedelta(days=1)
    return dt_yesterday.strftime("%Y-%m-%d")

def gen_all_sub_feature(indicator_path, feature_sub_path, trade_path):
    indicator_file = get_all_files(indicator_path)
    all_entry_trade_file = get_all_all_entry_files(trade_path+'detail/')
    merged_feature_path = trade_path+'merge/feature.csv'
    
    # print(len(indicator_file), len(all_entry_trade_file))
    # print(indicator_file)
    # print(all_entry_trade_file)
    dfs = []
    cnt = 0
    for ticker, file_t in all_entry_trade_file.items():
        print('feature', ticker)
        file_i = indicator_file[ticker]
        try:
            df_t = pd.read_csv(trade_path+'detail/' + file_t)
            df_i = pd.read_csv(indicator_path + file_i)
        except:
            continue
        df_t['ticker'] = ticker
        df_i['ticker'] = ticker
        
        df_t['date_trade_enter']=df_t.apply(
            lambda row : trade_date(row['entry_ts']), 
            axis = 1
        )       
        
        df_i['date_indicator_tomorrow']=df_i.apply(
            lambda row : indicator_date(row['est_datetime']), 
            axis = 1
        )   
        
        merged_df = df_t.merge(df_i, how='left', left_on=["ticker", "date_trade_enter"], right_on=["ticker","date_indicator_tomorrow"])    
        merged_df['df_channel_width'] = merged_df["barlow_2_ema8_channel_ceiling"] - merged_df["barlow_2_ema8_channel_floor"]
        merged_df['df_channel_width_percent'] = merged_df['df_channel_width'] / merged_df["barlow_2_ema8_channel_floor"]
        
        
        # enable writing per ticker df
#         merged_df.to_csv(feature_sub_path + ticker + '.csv')

        assert len(df_t) == len(merged_df)
        dfs.append(merged_df)
        cnt = cnt + 1
    df_merged_all = pd.concat(dfs)    
    df_merged_all.to_csv(merged_feature_path, index=False)
    print(cnt, len(df_merged_all['ticker'].unique()))
    assert len(df_merged_all['ticker'].unique()) == cnt
    
