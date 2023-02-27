'''
Created on Feb 27, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.sector_lib import rebuild_etf, \
    connect_ts_df_list


# get allocation
path_allocation = "C:/f_data/sector/allocation/allocation_ema21_below_ma50.csv"
df_allo = pd.read_csv(path_allocation)
df_allo_list = df_allo.to_dict('records')


ts_list = []
for row in df_allo_list:
    start_date = row['start_date']
    end_date = row['end_date']
    allocation = row
    del allocation['start_date']
    del allocation['end_date']
    print(allocation)
    
    ts = rebuild_etf(allocation, start_date, end_date)
    ts_list.append(ts)

ts_connected = connect_ts_df_list(ts_list)
path_out = 'C:/f_data/sector/result/spy_remix1.csv'
ts_connected.to_csv(path_out, index=False)
    
fig = px.line(ts_connected, x="date", y="ts", title='spy_rebuild')
fig.show()      


