import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout

import numpy as np
import plotly.express as px
path_out = """D:/f_data/es-1m_2007_to_2019end_changed3_inmarket.csv"""
path_in = """D:/f_data/es-1m_2007_to_2019end.csv"""
def load_df():
    path = path_in
    df = pd.read_csv(
        path,
        sep=';',
        header=None,
        names=['date','time', 'Open','High','Low','Close','volume']
    )
    return df
    
def formatter(df):
    # need to convert from CME time to NY time
    df['unixtime']=df.apply(lambda row : gendatetime_chi2ny(row['date'],row['time']), axis = 1)
    df['est_time_ny']=df.apply(lambda row : datetime.fromtimestamp(int(row['unixtime'])).strftime('%H:%M:%S'), axis = 1)
    df['year']=df.apply(lambda row : get_year(row['date']), axis = 1)
    
    
def get_year(a):
    b = a.split('-')
    year = b[0]
    return year

def gendatetime_chi2ny(date_str, time_str):
    s=date_str+' '+time_str
    p='%d/%m/%Y  %H:%M:%S'
    ts = datetime.timestamp(datetime.strptime(s, p))
    ts = ts + 3600
    return ts
 
df = load_df()
print(df)
print('mark')
df_formart = formatter(df)
print('add ny time')
print(df)
df_inmarket = df.loc[(df['est_time_ny']>= '09:30:00') & (df['est_time_ny'] <= '16:00:00')]
print('in market filter')
print(df_inmarket)
print('done')
df_inmarket.to_csv(path_out)
print('csv_done')
