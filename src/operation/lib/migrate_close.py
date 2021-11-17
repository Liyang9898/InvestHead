from datetime import datetime

import os

import pandas as pd
from util.util import float_to_percent_str
from version_master.version import (

    op_path_base,

)

from shutil import copyfile


def status(x):
    if x == 0:
        return 'neutral'
    elif x > 0:
        return 'win'
    else:
        return 'lose'


def file_closed_check():
    path_record = op_path_base+'record.csv'
    path_closed = op_path_base+'closed.csv'
    
    try:
        open(path_closed, "r+")
        open(path_record, "r+")
    except IOError:
        print("Please close all csv!!!!!")


def back_up_record():
    
    path_record = op_path_base+'record.csv'
    path_closed = op_path_base+'closed.csv'

    # process time period
    now = datetime.today()
    now_str = now.strftime('%Y-%m-%d')
    
    back_up_folder_path = op_path_base+'record_backup/' + now_str
    if not os.path.exists(back_up_folder_path):
        os.mkdir(back_up_folder_path) 

    # copy
    pd.read_csv(path_record)
    copyfile(path_record, back_up_folder_path+'/'+'record.csv')
    copyfile(path_closed, back_up_folder_path+'/'+'closed.csv')
    

def list_match(a,b):
    assert len(a) == len(b)
    for x in a:
        assert x in b


def move_closed_positions():
    path_record = op_path_base+'record.csv'
    path_closed = op_path_base+'closed.csv'
    df_record = pd.read_csv(path_record)
    df_closed = pd.read_csv(path_closed)
    list_match(df_record.columns, df_closed.columns)

    x = len(df_record)
    y = len(df_closed)

    still_opened_df = df_record[df_record['exit_price'].isnull()]
    new_closed_df_origin = df_record[df_record['exit_price'].notnull()]
    new_closed_df=new_closed_df_origin.copy()

    # process closed_df
    new_closed_df['close_rate'] = new_closed_df['exit_price'] * 1.0 / new_closed_df['enter_price'] - 1
    new_closed_df['status'] = new_closed_df.apply(lambda row : status(row['close_rate']), axis = 1)
    new_closed_df['close_rate'] = new_closed_df.apply(lambda row : float_to_percent_str(row['close_rate']), axis = 1)

    # merge closed df
    merged_closed_df = pd.concat([df_closed, new_closed_df])
    assert len(df_record) + len(df_closed) == len(merged_closed_df) + len(still_opened_df)
    merged_closed_df.reset_index()

    # write back
    
    merged_closed_df.to_csv(path_closed, index=False)
    still_opened_df.to_csv(path_record, index=False)
    

    df_record_new = pd.read_csv(path_record)
    df_closed_new = pd.read_csv(path_closed)
    x2 = len(df_record_new)
    y2 = len(df_closed_new)
    list_match(df_record_new.columns, df_closed_new.columns)
    list_match(df_record_new.columns, df_record.columns)
    # row count validation
    assert x+y==x2+y2
    assert x>=x2