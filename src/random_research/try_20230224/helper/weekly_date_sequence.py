'''
Created on Mar 11, 2023

@author: spark
'''
from util.util_time import get_most_recent_monday
import pandas as pd
from datetime import datetime, timedelta

start_date = '2005-06-01'
end_date = '2024-01-01'


start_date_pad = '2004-06-01'
end_date_pad = '2025-01-01'


start_date_pad_obj = datetime.strptime(start_date_pad, '%Y-%m-%d')
end_date_pad_obj = datetime.strptime(end_date_pad, '%Y-%m-%d')

cur = get_most_recent_monday(start_date_pad_obj)


l = []
while(cur < end_date_pad_obj):
    mon = cur
    fri = mon + timedelta(days=4)
    assert mon.weekday() == 0
    assert fri.weekday() == 4
    year = mon.year


    mon_str = mon.strftime("%Y-%m-%d")
    fri_str = fri.strftime("%Y-%m-%d")
    
    cur = cur + timedelta(days=7)
    
    res = {
        'date':mon_str,
        'start_date':mon_str,
        'end_date':fri_str,
        'year':str(year),
    }
    l.append(res)

df_weekly_signal = pd.DataFrame(l)

path_weekly_signal = "C:/f_data/sector/feature/allocation_signal_ema21_below_ma50_weekly.csv"
df_weekly_signal.to_csv(path_weekly_signal, index=False)

