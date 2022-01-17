import time
from datetime import datetime, timedelta


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