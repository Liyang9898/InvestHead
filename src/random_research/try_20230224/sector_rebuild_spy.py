'''
Created on Feb 24, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
from random_research.try_20230224.sector_lib import get_one_sector_ts_scaled, \
    aggregate_ts
from util.util_pandas import df_to_dict


# def get_year(date):
#     date_str = str(date)
#     year = int(date_str.split('-')[0])
#     return year
#
#
#
# # ticker = 'XLK'
# # sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)  
# #
# # df = pd.read_csv(sector_idc_path)
# # df['year']=df.apply(lambda row : get_year(row['date']), axis = 1)
# # print(df['year'])
# # year = 2020
# # initial_aum = 0.13
#
# # df = get_one_sector_ts_scaled(df, year, initial_aum)
# # print(df[['date','ts']])
#
# # fig = px.line(df, x="date", y="ts", title='mudong op timeseries')
# # fig.show()
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

l = []
for ticker, initial_aum in allo2.items():
    sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)  
    df_sector = pd.read_csv(sector_idc_path)

    df_scaled = get_one_sector_ts_scaled(start_date, end_date, df_sector, initial_aum)
    l.append(df_scaled)
    # print(df_scaled)
    fig = px.line(df_scaled, x="date", y="ts", title=ticker)
    fig.show()

f = aggregate_ts(l)
fig = px.line(f, x="date", y="ts", title='hhh')
fig.show()
