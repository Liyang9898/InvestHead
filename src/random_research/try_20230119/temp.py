'''
Created on Feb 5, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from util.util_pandas import insert_missing_date_val_to_df_cols

path = 'C:/f_data/random/mudong_op_long_seq_ts.csv'

start_date = '1994-01-01'
end_date = '2023-02-05'
date_col = 'first_trading_day'
val_col = 'aum'
df = pd.read_csv(path)

fig = px.line(df, x="first_trading_day", y="aum", title='mudong op timeseries')
fig.show()

df = insert_missing_date_val_to_df_cols(df, date_col, val_col, start_date, end_date)

fig2 = px.line(df, x="first_trading_day", y="aum", title='mudong op timeseries, interpolate')
fig2.show()

