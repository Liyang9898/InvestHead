'''
Created on Dec 25, 2020

@author: leon
'''

import os
import pandas as pd 

# user defined part
# folder_path_trade_results = "D:/f_data/sweep_20201214/yahoo_stock_trades_ma8_21_no_profit_manage/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion/ma8_21_no_profit_manage_201612_202012.csv"

# folder_path_trade_results = "D:/f_data/sweep_20201214/yahoo_stock_trades_ma21_50_with_profit_manage/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion/ma21_50_with_profit_manage_201612_202012.csv"

# folder_path_trade_results = "D:/f_data/sweep_20201214/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210108/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210108/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210110.csv"
# 'D:/f_data/sweep_20201214/all_ticker_meta/20210110_ticker_meta_with_vol.csv'
# meta_path = 'D:/f_data/sweep_20201214/all_ticker_meta/ticker_meta_with_vol.csv'

# folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210113_2150_4p_profit_cut_no_enutral_out/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210108/20210113_2150_4p_profit_cut_no_enutral_out.csv"
# 
# folder_path_trade_results = "D:/f_data/sweep_20201214/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210108/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210108/trades_summary_ma21_50_with_profit_manage_no_neutral_out_20210117.csv"


# folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210126_21_50_channel_controlled_enter/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210126/20210126_21_50_channel_controlled_enter.csv"


# folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210130_21_50_channel_only/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210201/20210130_21_50_channel_only.csv"

# 
# folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210201_8_21_channel_only/"
# trade_summary_bundle_path = "D:/f_data/sweep_20201214/conclusion_20210201/20210201_8_21_channel_only.csv"

folder_path_trade_results = "D:/f_data/sweep_20201214/trade_result/20210209_ribbion_start_iwf_only/"
trade_summary_bundle_path = "D:/f_data/sweep_20201214/merged/20210209_ribbon_start.csv"

meta_path = 'D:/f_data/sweep_20201214/all_ticker_meta/20210117_ticker_meta_with_vol.csv'


#####################

def merge_trade_summaries(folder_path_trade_results,trade_summary_bundle_path,meta_path):
    ticker_meta_with_vol = pd.read_csv(meta_path)
    cnt = 1
    l = []
    for file in os.listdir(folder_path_trade_results):
        if not file.endswith(".csv"):
            continue
          
        # extract ticker
        ticker = file.split('_')[0]
        print(cnt, ticker)
        # read data
        df = pd.read_csv(folder_path_trade_results+file)
        trade_summary_dic = df.to_dict('records')[0]
        trade_summary_dic['ticker'] = ticker
    #     print(trade_summary_dic)
        l.append(trade_summary_dic)
        cnt=cnt+1    
        
    df_trade_summary_bundle = pd.DataFrame(l)
    if 'Unnamed: 0' in df.columns:
        df_trade_summary_bundle.drop(columns=['Unnamed: 0'], inplace=True)
    
    trade_summary_with_st_info = pd.merge(df_trade_summary_bundle, ticker_meta_with_vol, on='ticker', how='inner')
    
    trade_summary_with_st_info.to_csv(trade_summary_bundle_path, index = False)
    print('done')



merge_trade_summaries(folder_path_trade_results, trade_summary_bundle_path,meta_path)