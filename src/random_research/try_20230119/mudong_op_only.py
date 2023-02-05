'''
Created on Jan 28, 2023

@author: spark
'''
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from random_research.try_20230119.constant import final_ts_chart_mudong_op_only
from random_research.try_20230119.pnl_fomular import mudong_op_pnl_conversion
from util.util_time import df_filter_dy_date 


year_max = 2023
year_min = 1994
up = 0.125
low = -0.125
aum_start = 1


# step 1: get spy data
path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df = pd.read_csv(path)


# step 2: get first_trading_day info of each year
def get_year(date):
    date_str = str(date)
    year = int(date_str.split('-')[0])
    return year

df['year']=df.apply(lambda row : get_year(row['date']), axis = 1)
first_trading_day_info = {}
for year in range(year_min, year_max+1):
    # get first trading day
    df_year = df[df['year']==year]
    date_year_begin = df_year['date'].min()
    
    # deal with info on that day
    first_day_df = df_year[df_year['date']==date_year_begin]
    first_day_price = first_day_df.iloc[0]['close']

    # create bundle
    bundle = {
        'year':year,
        'first_trading_day':date_year_begin,
        'first_day_price':first_day_price,
        'after_1_year_price': 0
    }
    first_trading_day_info[year] = bundle
    
    #handle previous year
    if year > year_min:
        first_trading_day_info[year-1]['after_1_year_price'] = first_day_price
        first_trading_day_info[year-1]['after_1_year_date'] = date_year_begin


# step3: apply option
for year, bundle in first_trading_day_info.items():
    strike = bundle['first_day_price']
    price = bundle['after_1_year_price']
    gain = round(mudong_op_pnl_conversion(price, strike, up, low),2)
    end_price = round(strike + gain, 2)
    bundle['end_price_with_mudong_op'] = end_price
    
    
# step4: connect
previous_aum = aum_start
for year, bundle in first_trading_day_info.items():
    s_p = bundle['first_day_price']
    e_p = bundle['end_price_with_mudong_op']
    s_d = bundle['first_trading_day']
    # e_d = bundle['after_1_year_date']
    s_p_cali = previous_aum
    e_p_cali = s_p_cali * (e_p / s_p)
    previous_aum = e_p_cali
    bundle['aum'] = s_p_cali


# step 5: plot
l = []
for year, bundle in first_trading_day_info.items():
    l.append(bundle)
df = pd.DataFrame(l)
df.to_csv(final_ts_chart_mudong_op_only, index=False)
fig = px.line(df, x="first_trading_day", y="aum", title='mudong op timeseries')
fig.show()
