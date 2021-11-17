import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout

import numpy as np
import plotly.express as px

# path_in = """D:/f_data/BATS_SPY_1min_1120_1224.csv"""
# path_out = """D:/f_data/BATS_SPY_1min_1120_1224_format.csv"""
# 
# path_in = """D:/f_data/BATS_SPY_1min_1223_0107.csv"""
# path_out = """D:/f_data/BATS_SPY_1min_1223_0107_format.csv"""

# path_in = """D:/f_data/BATS_SPY_5min.csv"""
# path_out = """D:/f_data/BATS_SPY_5min_format.csv"""

path_in = """D:/f_data/BATS_SPY_1min_2020_01.csv"""
path_out = """D:/f_data/BATS_SPY_1min_2020_01_format.csv"""


def load_df():
    path = path_in
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['time', 'open','high','low','close']
    )
    return df
    
def formatter(df):
    df['open'] = df['open'] * 10
    df['high'] = df['high'] * 10
    df['low'] = df['low'] * 10
    df['close'] = df['close'] * 10
    df['date']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d'), axis = 1)
    df['est_time']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%H:%M:%S'), axis = 1)
    df['year']=df.apply(lambda row : get_year(row['date']), axis = 1)
    
def get_year(a):
    b = a.split('-')
    year = b[0]
    return year
  

df = load_df()
print(df)
formatter(df)
df.to_csv(path_out, index=False)
print('done')
    