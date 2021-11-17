import datetime

from blake_shore.lib.blake_shore_core import get_option_price, \
    get_implied_volatility
from blake_shore.lib.helper import delta_meta_of_option_trail, \
    price_trail_impute, option_jacker_negation_price
import pandas as pd
from util.util import day_gap


def get_op_price_trail_assuming_v(
    st_price_trail, 
    strike_p, 
    mature_date,
    op_type, 
    risk_free_rate,
    implied_volatility,  
):
    
    dt_mature = datetime.datetime.strptime(mature_date, '%Y-%m-%d')
    op_trail = {}
    rows = []
    for t, price_st in st_price_trail.items():
        dt_t = datetime.datetime.strptime(t, '%Y-%m-%d')
        delta = dt_mature - dt_t
        days_util_mature = delta.days
        
        op_p_est = get_option_price(implied_volatility, price_st, strike_p, days_util_mature, risk_free_rate, op_type)
        op_trail[t] = op_p_est
        row = {
            'date': t,
            'day_left': days_util_mature,
            'stock_price': price_st,
            'option_price': op_p_est
        }
        rows.append(row)
    df =  pd.DataFrame(rows)
    delta_meta_of_option_trail(df)
    return df


def gen_option_trail_from_today_option(
    ticker,
    strike_price,
    option_price,
    date_mature,
    ##########
    date_today,
    stock_price_today,
    stock_price_on_mature,
    ##########
    risk_free_rate,
    op_type='c'
):
    expire_days=day_gap(date_today, date_mature)
    implied_volatility = get_implied_volatility(option_price, stock_price_today, strike_price, expire_days, risk_free_rate, op_type)
    
    price_trail = price_trail_impute(dt_s=date_today, dt_e=date_mature, p_s=stock_price_today, p_e=stock_price_on_mature)
    
    df = get_op_price_trail_assuming_v(
        st_price_trail=price_trail, 
        strike_p=strike_price, 
        mature_date=date_mature, 
        op_type=op_type,
        risk_free_rate=risk_free_rate,
        implied_volatility=implied_volatility,  
    )
    
    initial_leverage= df.loc[1, 'leverage_ab']
#     print(f'implied_volatility:{implied_volatility}, initial_leverage:{initial_leverage}')
    
    df['ticker']=ticker
    df['implied_volatility']=implied_volatility
    df['initial_leverage']=initial_leverage
    
    return df


def batch_gen_option_trail_from_today_option(options, negative_growth=False):
    if negative_growth:
        options = option_jacker_negation_price(options)

    all_res = {}
    for tag, ticker_row in options.items():
#         print('processing:', tag)
        res_df = gen_option_trail_from_today_option(
            ticker=ticker_row['ticker'],
            strike_price=ticker_row['strike'],
            option_price=ticker_row['op_p'],
            date_mature=ticker_row['mature'],
            ##########
            date_today=ticker_row['today'],
            stock_price_today=ticker_row['p_s'],
            stock_price_on_mature=ticker_row['p_e'],
            ##########
            risk_free_rate=ticker_row['risk_free_rate']
        )
        all_res[tag] = res_df
    return all_res