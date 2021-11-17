'''
Created on Jan 1, 2021

@author: leon
'''

from global_constant import constant as constant2
import pandas as pd
import os


def pickcolumn(file, path_out, input_column):
    df = pd.read_csv(
        file,
        sep=',',
        header=0,
        names=input_column
    )
    df.to_csv(
        path_out,
    )

def batch_format(folder_path_raw_downloaded, folder_path_raw_price_formated):
    ############################################source region start#############################################
    cnt = 1
    for file in os.listdir(folder_path_raw_downloaded):
        if file.endswith(".csv"):
    #     if file.endswith("V_download_format.csv"):
            print(cnt,'  ' ,file)
            raw_price_files=folder_path_raw_downloaded+file
            path_out=folder_path_raw_price_formated+file
    
            input_column=['time', 'open','high','low','close','ma200','ma50','ema21','ema8']
             
            pickcolumn(raw_price_files, path_out, input_column)
            cnt=cnt+1
    ############################################source region end#############################################

