'''
Created on Dec 25, 2020

@author: leon
'''


'''
Created on Dec 25, 2020

@author: leon
''' 

import pandas as pd
from batch_20201214.cash_history_lib import gen_cash_history_agg
from plotting_lib.simple import moving_window

def cash_history_to_df(cash_history):
    res = {}
    for dt, p in cash_history['price_position'].items():
        if dt not in res.keys():
            res[dt] = {
                'date':dt,
                'price_position':0,
                'cash_fixed_base_position':0,
                'cash_rollover_position':0
            }
        res[dt]['price_position'] = p
    
    for dt, p in cash_history['cash_fixed_base_position'].items():
        if dt not in res.keys():
            res[dt] = {
                'date':dt,
                'price_position':0,
                'cash_fixed_base_position':0,
                'cash_rollover_position':0
            }
        res[dt]['cash_fixed_base_position'] = p
        
    for dt, p in cash_history['cash_rollover_position'].items():
        if dt not in res.keys():
            res[dt] = {
                'date':dt,
                'price_position':0,
                'cash_fixed_base_position':0,
                'cash_rollover_position':0
            }
        res[dt]['cash_rollover_position'] = p
    
    l=[]
    for dt, v in res.items():
        l.append(v)
    df = pd.DataFrame(l)
    print(df)
    return df


    
def idle_position_cash_history(
    start_time,
    end_time,
    trade_folder,
    indicator_folder,
):

    moving_window_res_path = trade_folder + """merge/cash_history_idle_moving_window.csv"""
    cash_line_path = trade_folder + """merge/cash_history_idle_cash_history.csv"""
    
    cash_history=gen_cash_history_agg(
        trade_folder,
        indicator_folder,
        start_time,
        end_time
    )
    
    res_12 = moving_window(cash_history['cash_rollover_position'], window=260)
    res_1 = moving_window(cash_history['cash_rollover_position'], window=20)
    res_3 = moving_window(cash_history['cash_rollover_position'], window=60)
    res_6 = moving_window(cash_history['cash_rollover_position'], window=120)

    
    res = {
        'idle_up_rate_1_m': res_1['positive_rate'],
        'idle_up_rate_3_m': res_3['positive_rate'],
        'idle_up_rate_6_m': res_6['positive_rate'],
        'idle_up_rate_12_m': res_12['positive_rate'],
        
        'idle_window_pnl_p_1_m': res_1['window_pnl_p_avg'],
        'idle_window_pnl_p_3_m': res_3['window_pnl_p_avg'],
        'idle_window_pnl_p_6_m': res_6['window_pnl_p_avg'],
        'idle_window_pnl_p_12_m': res_12['window_pnl_p_avg'],
    }

    cash_history_df = cash_history_to_df(cash_history)
    cash_history_df.to_csv(cash_line_path,index=False)
    
    moving_window_df = pd.DataFrame([res])
    moving_window_df.to_csv(moving_window_res_path,index=False)
    
