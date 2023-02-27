'''
Created on Feb 24, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.sector_lib import get_one_sector_ts_scaled, \
    aggregate_ts, rebuild_etf, connect_ts_df_list
from util.util_pandas import df_to_dict



years = [2016,2017,2018,2019,2020,2021]
post_fix = '-01-01'

path = 'C:/f_data/sector/spy_sector_history_clean.csv'
df = pd.read_csv(path)

allocation = {}
ts_dict = {}
ts_list = []

for year in years:
    allocation[year] = df_to_dict(df, 'ticker', str(year))
    print(allocation[year])
    
    start_date = str(year) + post_fix
    end_date = str(year + 1) + post_fix

    ts_dict[year] = rebuild_etf(allocation[year], start_date, end_date)
    ts_list.append(ts_dict[year])


df_all = connect_ts_df_list(ts_list)
path_out = 'C:/f_data/sector/result/spy_rebuild.csv'
df_all.to_csv(path_out, index=False)


fig = px.line(df_all, x="date", y="ts", title='spy_rebuild')
fig.show()  
