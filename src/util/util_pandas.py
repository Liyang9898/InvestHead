# import numpy as np
import pandas as pd
from util.util_math import percentile
from util.util_time import df_filter_dy_date, get_year_from_dt, \
    get_month_from_dt


def df_unixtime_filter(df, date_col, s, e):
    df = df[(df[date_col] >= s) & (df[date_col] <= e)]
    df.reset_index(drop=True,inplace=True)
    return df


def df_general_time_filter(df, date_col, s, e):
    df = df[(df[date_col] >= s) & (df[date_col] <= e)]
    df.reset_index(drop=True,inplace=True)
    return df


def df_normalize(df, normalize_col, initial_val=1):
    # normalize_col must be numerical and not null
    df.reset_index(drop=True,inplace=True)
    factor = df.loc[0, normalize_col]
    for i in range(0, len(df)):
        df.loc[i, normalize_col] = df.loc[i, normalize_col] / factor * initial_val
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


def df_to_dict(df, key_col, val_col):
    res = {}
    record = df.to_dict('records')
    for r in record:
        res[r[key_col]] = r[val_col]
    return res


def dict_to_df(dic, key_col, val_col):
    res = []
    for k, v in dic.items():
        d = {key_col:k, val_col:v}
        res.append(d)
    df = pd.DataFrame(res)
    return df


def get_year_begin_rows(df):
    '''
    df must has a 'date' column
    get the first record of each year
    '''
    df['year']=df.apply(lambda row : get_year_from_dt(row['date']), axis = 1)
    rows_pick = []
    rows = df.to_dict('records')
    
    pre_year = rows[0]['year']
    for row in rows:
        year = row['year']
        if year != pre_year:
            rows_pick.append(row)
        pre_year = year
    
    df_res = pd.DataFrame(rows_pick)
    return df_res


def get_month_begin_rows(df):
    '''
    df must has a 'date' column
    get the first record of each month
    '''
    df['month']=df.apply(lambda row : get_month_from_dt(row['date']), axis = 1)
    rows_pick = []
    rows = df.to_dict('records')
    
    pre_month = rows[0]['month']
    for row in rows:
        month = row['month']
        if month != pre_month:
            rows_pick.append(row)
        pre_month = month
    
    df_res = pd.DataFrame(rows_pick)
    return df_res


def get_pnl_between_rows(df, benchmark_col, exp_col):
    '''
    df must has 'date', benchmark_col and exp_col columns
    it's computing the percent diff of benchmark and exp. then compute their diff
    '''
    rows = []
    for i in range(0, len(df) - 1):
        date = df.loc[i, 'date']
        benchmark_pnl = df.loc[i + 1, benchmark_col] / df.loc[i, benchmark_col] - 1
        exp_pnl = df.loc[i + 1, exp_col] / df.loc[i, exp_col] - 1
        diff_pnl = exp_pnl - benchmark_pnl
        row = {'date': date, benchmark_col: benchmark_pnl, exp_col: exp_pnl, 'diff_pnl': diff_pnl}
        rows.append(row)
    df_pnl = pd.DataFrame(rows)
    return df_pnl