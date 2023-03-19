import time
import pandas as pd
from datetime import datetime, timedelta


"""
useful conversion example
date = datetime.strptime(date_str, '%Y-%m-%d')
date_str = date.strftime("%Y-%m-%d")
"""


PERIOD_CALENDAR_MONTH = 'calendar_month'
PERIOD_CALENDAR_YEAR = 'calendar_year'

def get_today_date_str():
    now = datetime.now()
    now_str = str(now)
    date_str = now_str.split(' ')[0]
    return date_str


def date_to_datetime_obj(date_str):
    dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return dt_obj


def datetime_obj_to_date_str(dt_obj):
    date_str = dt_obj.strftime("%Y-%m-%d")
    return date_str


def df_filter_dy_date(df,date_col,s,e):
    # create a copy of input df and filter by date range, and return
    df = df.loc[(df[date_col]>=s) & (df[date_col]<=e)]
    df_filtered = df.copy()
    df_filtered.reset_index(inplace=True,drop=True)
    return df_filtered


def date_to_unixtime(date):
    unixtime = time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())
    return unixtime


def get_most_recent_monday(dt_obj):
    dt_obj_mon = dt_obj + timedelta(days=-dt_obj.weekday())
    return dt_obj_mon


def unixtime_to_date(unixtime):
    timestamp = datetime.fromtimestamp(int(unixtime))
    date = str(timestamp.strftime('%Y-%m-%d'))
    return date


def date_formatter_1(date):
    datetime_object = datetime.strptime(date, '%m/%d/%Y')
#     tokens = date.split('/')
    return datetime_object.strftime("%Y-%m-%d")


def time_format_slash_string_to_unixtime(date):
    date_str_bar = date_formatter_1(date)
    return date_to_unixtime(date_str_bar)


def days_gap_date_str(date_str_s, date_str_e):
    dt_s = datetime.strptime(date_str_s, '%Y-%m-%d')
    dt_e = datetime.strptime(date_str_e, '%Y-%m-%d')
    gap = dt_e - dt_s
    return gap.days 


def date_add_days(date_str, delta_days):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    dt_new = dt + timedelta(days=delta_days)
    return dt_new.strftime("%Y-%m-%d")


def gen_date_list_in_range(start_date, end_date, end_inclusive=True):
    """
    input: start end date in YYYY-MM-DD format
    output: a list of date in YYYY-MM-DD format in range
    if end_inclusive is false, the end is not included in result list
    """
    res = []
    s = datetime.strptime(start_date, '%Y-%m-%d')
    e = datetime.strptime(end_date, '%Y-%m-%d')
    cur = s
    while cur<e:
        cur_date_date_str = cur.strftime("%Y-%m-%d")
        res.append(cur_date_date_str)
        cur = cur + timedelta(days=1)
    if end_inclusive:
        res.append(end_date)
    return res


def mark_year_month_week_start(df, date_col):
    df['year_start'] = False
    df['week_start'] = False
    df['month_start'] = False
    
    df.sort_values(by=[date_col], inplace=True)
    df.reset_index(inplace=True, drop=True) 
    
    year_pre = -1
    month_pre = -1
    week_pre = -1
    
    for i in range(0, len(df)):
        date_str = df.loc[i, date_col]
        
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        year = dt.year
        month = dt.month
        week = dt.isocalendar()[1]
        
        if year != year_pre:
            # today is begin of a new year
            df.loc[i, 'year_start'] = True
            year_pre = year
        
        if month != month_pre:
            # today is begin of a new year
            df.loc[i, 'month_start'] = True
            month_pre = month

        if week != week_pre:
            # today is begin of a new year
            df.loc[i, 'week_start'] = True
            week_pre = week 
                   
    return df      


def extract_period_start_from_df(df, date_col, period):
    """
    input: a df with date_col has format yyyy-mm-dd
    """
    period_id = -1
    last_processed_date = ''
    df = df.sort_values(by=date_col, ascending=True)
    serieses = []
    for i in range(0, len(df)):
        date = df.loc[i, date_col]
        
        tokens = date.split('-')
        year = int(tokens[0])
        month = int(tokens[1])
        
        if period == PERIOD_CALENDAR_MONTH:
            if month != period_id:
                # extract row add to 
                row = df.loc[i]
                serieses.append(row)
                period_id = month
                last_processed_date = date
                
        elif period == PERIOD_CALENDAR_YEAR:
            if year != period_id:
                # extract row add to 
                row = df.loc[i]
                serieses.append(row)
                period_id = year
                last_processed_date = date
    
    last_idx = len(df) - 1
    last_date = df.loc[last_idx, date_col]
    if last_date != last_processed_date:
        serieses.append(df.loc[last_idx])
    
    df_res = pd.DataFrame(serieses)
    df_res.reset_index(inplace=True, drop=True)
    return df_res


def get_year_str(date_obj):
    date_str = str(date_obj)
    year = int(date_str.split('-')[0])
    return year


def get_year_from_dt(dt):
    date_str = str(dt)
    dt = date_to_datetime_obj(date_str)
    return dt.year


def get_month_from_dt(dt):
    date_str = str(dt)
    dt = date_to_datetime_obj(date_str)
    return dt.month


def count_weekday(start_date, end_date):
    res = 0
    s = datetime.strptime(start_date, '%Y-%m-%d')
    e = datetime.strptime(end_date, '%Y-%m-%d')
    cur = s
    
    while cur<e:
        weekday = cur.weekday()
        if weekday < 5:
            res = res + 1
        cur = cur + timedelta(days=1)
    return res

