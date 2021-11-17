'''
Created on Jun 4, 2020

@author: leon
'''
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
from indicator_master.indicator_compute_lib import add_indicator
from indicator_master.plot_indicator_lib import plot_indicator
from indicator_master import constant
import pandas as pd

# structure of both dataframe and csv file in read and write: see global_constant file

def df2csv_indicator(df, path_out):
    
    assert len(constant.indicator_interface) == len(set(constant.indicator_interface))

    df.to_csv(
        path_out,
#         columns=constant.indicator_interface,
        index=False
    )
#     print('df2csv_indicator done')
    

def csv2df_indicator(filepath):
    path = filepath
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
#         names=constant.indicator_interface,
    )
    return df


############################################## test ###################################################
# input_data = """D:/f_data/BITSTAMP_BTCUSD, 60.csv"""
# output_indicator_csv = """D:/f_data/test_output1.csv"""
# 
# # df 2 csv
# df = load_df_from_csv(input_data)
# add_indicator(df)
# df2csv_indicator(df,output_indicator_csv)
# 
# # csv 2 df
# df_read_back=csv2df_indicator(output_indicator_csv)
# print(df_read_back)
# 
# #print df_read_back
# plot_indicator(df_read_back, 'sequence_8_21')
############################################## test ###################################################
