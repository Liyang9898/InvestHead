# import numpy as np
import pandas as pd
from util.util_math import percentile
from util.util_time import df_filter_dy_date


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
    return df
        
        
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
    
    
def gen_csv_from_list_of_val(val_list, col_name, csv_path, start_date, end_date):
    """
    turn list val_list into a single column df with name col_name
    and save in csv in path csv_path
    """
    d = {col_name: val_list}
    df = pd.DataFrame(data=d)
    date_col = 'date'
    df = df_filter_dy_date(df,date_col,start_date,end_date)
    df.to_csv(csv_path, index=False)
    
def df_col_percentile(df, col, p, asc=True):
    '''
    compute value at a certain percentile for a col in dataframe
    l is a list values
    p is percentile
    asc means the l list is sorted in asc order
    p=90 will pick the 10% element from the right
    '''
    l = df[col].tolist()
    x = percentile(l, p, asc)
    return x


def insert_missing_date_to_df_col(df, date_col, start_date, end_date):
    df[date_col] = df[date_col].astype('datetime64[ns]')
    date_index = pd.date_range(start=start_date, end=end_date)
    df = df.set_index(date_col).reindex(date_index).rename_axis(date_col).reset_index()   
    return df


def insert_missing_date_val_to_df_cols(
    df, 
    date_col, 
    val_col, 
    start_date, 
    end_date, 
    method ='linear', 
    limit_direction ='forward'
):
    '''
    This method first interpolate the date_col with start and end date
    then interpolate val_col using the specified method
    '''
    df = insert_missing_date_to_df_col(df, date_col, start_date, end_date)
    df[val_col].interpolate(method=method, limit_direction=limit_direction, inplace=True)
    return df