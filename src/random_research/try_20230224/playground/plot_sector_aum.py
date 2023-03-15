'''
Created on Mar 15, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.helper.validate_allocation_lib import validation_allocation
from random_research.try_20230224.sector_lib import rebuild_etf, \
    connect_ts_df_list
from util.util_pandas import df_general_time_filter



sector_aum_path = 'C:/f_data/sector/debug/sector_line.csv'
df = pd.read_csv(sector_aum_path)
fig = px.scatter(df, x="date", y="ts", color='ticker', title='sector_remix')

fig.show()     



