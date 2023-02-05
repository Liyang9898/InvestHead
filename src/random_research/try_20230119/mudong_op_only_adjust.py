'''
Created on Feb 4, 2023

@author: spark
'''
'''
Created on Jan 28, 2023

@author: spark
'''

import pandas as pd
import plotly.express as px
from random_research.try_20230119.constant import final_ts_chart_mudong_op_adjust
from random_research.try_20230119.mudong_lib import gen_op_swing_timeseries


year_max = 2023
year_min = 1994

up_in_long = 0.175
low_in_long = -0.075

up_in_short = 0.075
low_in_short = -0.175

aum_start = 1

first_trading_date = '01-01'

path_spy_weekly = 'C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'
path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'


df = gen_op_swing_timeseries(
    path,
    path_spy_weekly,
    year_max,
    year_min,
    
    up_in_long,
    low_in_long,
    
    up_in_short,
    low_in_short,
    
    aum_start,
    final_ts_chart_mudong_op_adjust,
    first_trading_date,
)    

df.to_csv(final_ts_chart_mudong_op_adjust, index=False)

fig = px.line(df, x="first_trading_day", y="aum", title='mudong op timeseries')
fig.show()