'''
Created on Feb 5, 2023

@author: spark
'''

from functools import reduce

import pandas as pd
import plotly.express as px
from random_research.try_20230119.constant import final_op_swing_adjusted_monthly, \
    mudong_op_swing_adjusted_monthly_125_125, \
    mudong_op_swing_adjusted_monthly_175_75
from random_research.try_20230119.mudong_lib import gen_op_swing_timeseries, \
    df_time_filter_and_normalize
from util.util_pandas import insert_missing_date_val_to_df_cols


ts_start_date = '1994-12-15'
ts_end_date = '2022-01-17'

start_date = '1994-01-01'
end_date = '2023-02-05'
date_col = 'first_trading_day'
val_col = 'aum'


year_max = 2023
year_min = 1994

# up_in_long = 0.175
# low_in_long = -0.075
#
# up_in_short = 0.075
# low_in_short = -0.175


up_in_long = 0.125
low_in_long = -0.125

up_in_short = 0.125
low_in_short = -0.125


aum_start = 1
final_ts_chart_mudong_op_adjust = 'C:/f_data/random/mudong_op_ts_adjusted.csv'
first_trading_date_list = ['01-15','03-15','06-15','09-15','12-15']

path_spy_weekly = 'C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'
path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'

path_out = mudong_op_swing_adjusted_monthly_125_125
# path_out = mudong_op_swing_adjusted_monthly_175_75

df_list = []
for first_trading_date in first_trading_date_list:
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
    df = insert_missing_date_val_to_df_cols(df, date_col, val_col, start_date, end_date)
    col_name = 'aum'+first_trading_date
    df[col_name] = df['aum']
    
    df = df[['first_trading_day', col_name]]
    df.reset_index(inplace=True, drop=True)
    df_list.append(df)


df_all = reduce(lambda x, y: pd.merge(x, y, on = 'first_trading_day'), df_list)
df_all['aum'] = (df_all['aum01-15'] + df_all['aum03-15'] + df_all['aum06-15'] + df_all['aum09-15'] + df_all['aum12-15']) / 5

df_all_filter = df_time_filter_and_normalize(df=df_all, date_col=date_col, normalize_col='aum', start_date=ts_start_date, end_date=ts_end_date)

df_all_filter.to_csv(path_out, index=False)


fig = px.line(df_all_filter, x="first_trading_day", y="aum", title='mudong op timeseries')
fig.show()
