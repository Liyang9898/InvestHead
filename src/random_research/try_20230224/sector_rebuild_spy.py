'''
Created on Feb 24, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.sector_lib import get_one_sector_ts_scaled, \
    aggregate_ts, rebuild_etf
from util.util_pandas import df_to_dict


tickers = []

path = 'C:/f_data/sector/spy_sector_history.csv'
df = pd.read_csv(path)
print(df)
allo = df_to_dict(df, 'ticker', '2020')

allo2 = {}
for k, v in allo.items():
    v_f = float(v.replace("%", ""))*0.01
    allo2[k]=v_f
    
    
print(allo2)


start_date = '2020-01-01'
end_date = '2021-01-01'


ts_agg = rebuild_etf(allo2, start_date, end_date)

fig = px.line(ts_agg, x="date", y="ts", title='hhh')
fig.show()


