import pandas as pd
import numpy as np


def df_unixtime_filter(df, date_col, s, e):
    df = df[(df[date_col] >= s) & (df[date_col] <= e)]
    df.reset_index(drop=True,inplace=True)
    return df


def df_general_time_filter(df, date_col, s, e):
    df = df[(df[date_col] >= s) & (df[date_col] <= e)]
    df.reset_index(drop=True,inplace=True)
    return df


def df_normalize(df, normalize_col):
    # normalize_col must be numerical and not null
    df.reset_index(drop=True,inplace=True)
    factor = df.loc[0, normalize_col]
    for i in range(0, len(df)):
        df.loc[i, normalize_col] = df.loc[i, normalize_col] / factor
        
        
def df_multiply_factor(df, normalize_col, factor):
    # normalize_col must be numerical and not null
    for i in range(0, len(df)):
        df.loc[i, normalize_col] = df.loc[i, normalize_col] * factor
        
        
def dict_to_one_row_df(dict_input):
    d = {}
    for k, v in dict_input.items():
        d[k] = [v]
    df = pd.DataFrame(data=d)
    return df


def percent_increase_of_current_row(df, val_col):
    df[val_col + '_pct_increase'] = df[val_col].pct_change()
    
    
def gen_csv_from_list_of_val(val_list, col_name, csv_path):
    """
    turn list val_list into a single column df with name col_name
    and save in csv in path csv_path
    """
    d = {col_name: val_list}
    df = pd.DataFrame(data=d)
    df.to_csv(csv_path, index=False)
    