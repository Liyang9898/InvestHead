import numpy as np
from util.util import get_all_weekdays, get_certain_weekdays


def delta_meta_of_option_trail(df):
    # this is in place modification function
    # it add 3 new columns: 
    # 1.stock delta percent compared with yesterday
    # 2.option delta percent compared with yesterday
    # 3.leverage of option and stock
    # edge case
    if len(df) < 2:
        return df
    
    st_base = df.loc[0, 'stock_price']
    op_base = df.loc[0, 'option_price']    
    
    st_pre = st_base
    op_pre = op_base
    
    df['st_delta'] = np.nan
    df['op_delta'] = np.nan
    df['leverage'] = np.nan
    df['leverage_ab'] = np.nan
    for i in range(1,len(df)):
        st = df.loc[i, 'stock_price']
        op = df.loc[i, 'option_price']
        df.loc[i, 'st_delta'] = st / st_pre - 1
        df.loc[i, 'op_delta'] = op / op_pre - 1
        if df.loc[i, 'st_delta'] == 0:
            df.loc[i, 'leverage'] = np.nan
        else:
            df.loc[i, 'leverage'] = df.loc[i, 'op_delta'] / df.loc[i, 'st_delta']
        
        df.loc[i, 'st_delta_ab'] = st / st_base - 1
        df.loc[i, 'op_delta_ab'] = op / op_base - 1
        if df.loc[i, 'st_delta_ab'] == 0:
            df.loc[i, 'leverage_ab'] = np.nan
        else:
            df.loc[i, 'leverage_ab'] = df.loc[i, 'op_delta_ab'] / df.loc[i, 'st_delta_ab']
        
        st_pre = st
        op_pre = op


def price_trail_impute(dt_s, dt_e, p_s, p_e):    
    days = get_certain_weekdays(s=dt_s, e=dt_e, weekday_id=0)
    p_delta = (p_e - p_s) / (len(days) - 1)
    res = {}
    p = p_s
    
    for d in days:
        res[d] = p
        p += p_delta
        
    return res


def option_info_reformat(
    option_info
):
    rows = {}
    for k,v in option_info['option_chain'].items():
        rows[k] = {}
        # environment info
        rows[k]['tag'] = option_info['tag']
        rows[k]['increase_factor'] = option_info['increase_factor']
        rows[k]['risk_free_rate'] = option_info['risk_free_rate']
        
        # basic option info
        rows[k]['ticker'] = option_info['ticker']
        rows[k]['st_price_now'] = option_info['st_price_now']
        rows[k]['today'] = option_info['today']
        rows[k]['mature'] = option_info['mature']
        
        # option chain
        rows[k]['strike'] = v['strike']
        rows[k]['op_p'] = v['op_p']
        
        # stock price
        rows[k]['p_s'] = option_info['st_price_now']
        rows[k]['p_e'] = option_info['st_price_now'] * (option_info['increase_factor']+1)

    return rows


def iv_and_leverage_from_option_group(dfs):
    iv_sum = 0
    leverage_sum = 0
    res = {}

    for tag, df in dfs.items():
        implied_volatility = df.loc[0, 'implied_volatility']
        initial_leverage = df.loc[0, 'initial_leverage']
        ticker = df.loc[0, 'ticker']
        expire_month = int(df.loc[0, 'day_left'] / 30)
        
        print(f'{tag}:implied_volatility:{implied_volatility}, initial_leverage:{initial_leverage}')
        if tag == 'strike=0%':
            res['iv_0'] = implied_volatility
            res['leverage_0'] = initial_leverage
            res['ticker'] = ticker
            res['expire_month'] = expire_month
        iv_sum += implied_volatility
        leverage_sum += initial_leverage
        
    res['iv_avg'] = iv_sum / len(dfs)
    res['leverage_avg'] = leverage_sum / len(dfs)
    
    return res


def option_jacker_negation_price(options):
    # this function reverse the growth of option's underlying price
    options_neg = {}
    for tag, option in options.items():
        options_neg[tag] = option.copy()
        options_neg[tag]['increase_factor'] *= -1
        options_neg[tag]['p_e'] = options_neg[tag]['p_s'] * (1 + options_neg[tag]['increase_factor'])
    return options_neg 