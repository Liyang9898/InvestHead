'''
Created on Jan 3, 2021

@author: leon
'''

from indicator_master.create_indicator_api_main import price_csv_append_indicator
import os
from batch_20201214.util_for_batch.batch_util import check_ticker_exist, get_all_files


############################################source region start#############################################
def batch_indicator(
    folder_path_price_with_indicator, 
    folder_path_raw_price_formated, 
    start_time, 
    end_time,
    ticker_list=None
):
    files = get_all_files(folder_path_raw_price_formated)
    cnt = 1
    for ticker, file in files.items():
        if file.endswith(".csv"):
    #     if file=="V_download_format.csv":
#             ticker = file.split('_')[0]
            if ticker_list is not None and ticker not in ticker_list:
                print('skip', ticker)
                cnt=cnt+1
                continue
            print(cnt,'  ' ,ticker)
    #         if cnt <0:
    #             cnt=cnt+1
    #             continue
            exist = check_ticker_exist(folder_path_price_with_indicator,ticker)
            if exist:
                print(ticker, 'trading results already exist')
            else:
                input_file=folder_path_raw_price_formated+file
                output_file=folder_path_price_with_indicator+file
        
                price_csv_append_indicator(
                    input_file_path=input_file, 
                    output_file_path=output_file,
                    start_time=start_time, 
                    end_time=end_time,
                    plot_chart=False
                )
            cnt=cnt+1

############################################source region end#############################################
# import os

# from batch_20201214.util_for_batch.batch_util import get_all_files
import pandas as pd
# from trade_analysis_master.concat_lib.concat_trades_details import join_trades_with_indicator


def build_indicator_collection(indicator_folder):
    output_path=indicator_folder+'merge/'
    os.mkdir(output_path)
    
    files = get_all_files(indicator_folder)
    dfs = []
    
    for ticker, file in files.items():
        print('merging indicator', ticker)
        path = indicator_folder + file
        df = pd.read_csv(path)
        df['ticker'] = ticker
        dfs.append(df)
        
    df_merged = pd.concat(dfs)    
    df_merged.to_csv(output_path+'all_indicator.csv', index=False)
    x = df_merged['ticker'].nunique()
    assert x == len(files)
    return df_merged
    
    