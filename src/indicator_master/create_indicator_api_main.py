'''
Created on Jun 9, 2020

@author: leon
'''
'''
Created on Jun 4, 2020

@author: leon
'''
import pandas as pd
# input file must follow interface: see global_constant file
# output structure: see global_constant file

from indicator_master.indicator_caching_lib import df2csv_indicator
from indicator_master.indicator_compute_lib import add_indicator, tsfilter
from indicator_master.plot_indicator_lib import plot_indicator
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
from util.util_pandas import df_unixtime_filter
from util.util_time import date_to_unixtime

def plot_indicator_from_csv(indicator_path):
    df = pd.read_csv(indicator_path)
    plot_indicator(df, 'sequence_8_21_50', indicator_path)


def price_csv_append_indicator(input_file_path, output_file_path, start_time, end_time, plot_chart):
    unix_s = date_to_unixtime(start_time)
    unix_e = date_to_unixtime(end_time)
    
    # read price csv to df
    df = load_df_from_csv(input_file_path)
    # print(df.columns)
    # print(df.head(1))
    df = df_unixtime_filter(df, 'time', unix_s, unix_e)
    

    if len(df)<=10:
        print('price row count = ' + str(len(df)))
        return
    
    # add indicator
    add_indicator(df)
    
    # filter time
    df_range = tsfilter(df,start_time,end_time)
    
    # write df with indicator to file
    df2csv_indicator(df_range,output_file_path)
    
    # optional: plot
    if plot_chart:
        plot_indicator(df_range, 'sequence_8_21_50',input_file_path)
