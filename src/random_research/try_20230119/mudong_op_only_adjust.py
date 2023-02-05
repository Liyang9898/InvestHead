'''
Created on Feb 4, 2023

@author: spark
'''
'''
Created on Jan 28, 2023

@author: spark
'''
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
from random_research.try_20230119.pnl_fomular import mudong_op_pnl_conversion
from util.util_time import df_filter_dy_date 
from numpy.f2py.auxfuncs import throw_error


def get_year(date):
    date_str = str(date)
    year = int(date_str.split('-')[0])
    return year
    
    
def spy_weekly_ma21_50_seq_is_up(date, df):
    '''
    given a date, check if the weekly ema21 > ma50 
    '''
    for i in range(0, len(df)):
        weekly_date = df.loc[i, 'date']
        # print(weekly_date)
        if weekly_date > date:
            ema21 = df.loc[i, 'ema21']
            ma50 = df.loc[i, 'ma50']
            if ema21>ma50:
                return True
            else:
                return False
    print(date)
    raise Exception("can't locate a weekly date")


# constant
year_max = 2023
year_min = 1994

up_in_long = 0.175
low_in_long = -0.075

up_in_short = 0.075
low_in_short = -0.175

aum_start = 1
final_ts_chart_mudong_op_adjust = 'C:/f_data/random/mudong_op_ts_adjusted.csv'
first_trading_date = '01-01'

path_spy_weekly = 'C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'
path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'

def gen_op_swing_timeseries(
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
):
    # step 1: get stock data and weekly asset
    df = pd.read_csv(path)
    df_spy_weekly = pd.read_csv(path_spy_weekly)
    
    # step 2: get first_trading_day >= [year-xx-xx] info of each year
    '''
    Edge case:
    year min must has Jan 1 in it
    year max might not has the [year-xx-xx] in it, then year max will be ignored in final result
    '''

    
    
    df['year']=df.apply(lambda row : get_year(row['date']), axis = 1)
    first_trading_day_info = {}
    for year in range(year_min, year_max+1):
        # get first trading day >= [year-xx-xx]
        target_date = str(year) + '-' + first_trading_date
        df_year = df[df['year']==year]
        df_year_sub = df[df['date']>=target_date]
        if len(df_year_sub) == 0:
            break # year max does not has the [year-xx-xx] in it
        date_year_begin = df_year_sub['date'].min()
        
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
        date = bundle['first_trading_day']
        # if year == year_max:
        #     break
        
        ma21_50_seq_is_up = spy_weekly_ma21_50_seq_is_up(date, df_spy_weekly)
    
        if ma21_50_seq_is_up:
            gain = round(mudong_op_pnl_conversion(price, strike, up_in_long, low_in_long),2)
            end_price = round(strike + gain, 2)
            bundle['end_price_with_mudong_op'] = end_price
        else:
            gain = round(mudong_op_pnl_conversion(price, strike, up_in_short, low_in_short),2)
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
    df.to_csv(final_ts_chart_mudong_op_adjust, index=False)

    
    
gen_op_swing_timeseries(
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
df = pd.read_csv(final_ts_chart_mudong_op_adjust)

fig = px.line(df, x="first_trading_day", y="aum", title='mudong op timeseries')
fig.show()