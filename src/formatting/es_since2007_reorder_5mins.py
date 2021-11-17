import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout

import numpy as np
import plotly.express as px
path_out = """D:/f_data/es-5m_2007_to_2019end_nytime_format.csv"""
path_in = """D:/f_data/es-5m_2007_to_2019end_nytime.csv"""
def load_df():
    path = path_in
    df = pd.read_csv(
        path,
        sep=',',
        header=1,
        names=['date','time', 'Open','High','Low','Close','volume','unixtime','est_time_ny','year']
    )
    return df

     
def formatter(df):
#     df['Open'] = df['Open'] / 10
#     df['High'] = df['High'] / 10
#     df['Low'] = df['Low'] / 10
#     df['Close'] = df['Close'] / 10
    df['date'] = df.apply(lambda row : date_reformat(row['date']), axis = 1)

def date_reformat(ds):
    b = ds.split('/')
    new_ds = b[2] +'-' + b[1] + '-'+ b[0]
    return new_ds
 
df = load_df()
print(df)
formatter(df)
df.to_csv(path_out,columns =['unixtime','Open','High','Low','Close','date','est_time_ny','year'], index=False)
print('done')

# ['time', 'open','high','low','close','date','est_time','year']