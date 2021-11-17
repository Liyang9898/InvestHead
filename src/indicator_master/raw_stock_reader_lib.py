'''
Created on Jun 4, 2020

@author: leon
'''
import pandas as pd
from indicator_master import constant

# This library handles all logic which load CSV into a standard df with following inferface: see global_constant file

def load_df_from_csv(filepath):
    path = filepath
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=constant.price_interface
    )
    return df

############################################## test ###################################################
# path_test = """D:/f_data/BITSTAMP_BTCUSD, 60.csv"""
# df = load_df_from_csv(path_test)
# print(df)
############################################## test ###################################################