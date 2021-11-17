'''
Created on Feb 14, 2021

@author: leon
'''
import pandas as pd
from batch_20201214.reuse_position.fill_price_in_track_lib import get_date_list
import plotly.express as px


def price_in_track_df_to_dic(df):
    tracks = {}
    for i in range(0, len(df)):
        track_id = df.loc[i, 'track_id']
        date = df.loc[i, 'date']
        ticker = df.loc[i, 'ticker']
        price = df.loc[i, 'price']
        
        entry = {
            'ticker':ticker,
            'price':price
        }
        
        if track_id not in tracks.keys():
            tracks[track_id] = {}
        tracks[track_id][date] = entry
    return tracks

def roll_over_position(start_date, end_date, track, track_id, debug_info=False):
    if track_id == 0:
        print('===========')
        print(track)
    date_list = get_date_list(start_date, end_date)
    fix_base = 1
    
    # update all these tracking state
    position_roll = {}
    position_fix = {} # Important: this is only asset in market, not include ideal cash. Real position is position_fix + profit_fix
    profit_fix = {} # ideal cash
    action = {}
    
    pre_position_roll = 1
    pre_position_fix = 0
    pre_profit_fix = fix_base
    in_market = False
    pre_ticker = '-1'
    pre_st_price = -1
    
    for date in date_list:
        has_trade = True if date in track.keys() else False
        if in_market:
            # last trading day in market
            if has_trade:
                
                cur_ticker = track[date]['ticker']
                if cur_ticker == pre_ticker: # holding same stock, no action
                    action[date] = 'same holding'
                    cur_st_price = track[date]['price']
                    # roll: cur_position_roll / pre_position_roll =  cur_st_price/ pre_st_price
                    position_roll[date] = (cur_st_price *1.0) / (pre_st_price * 1.0) * (pre_position_roll * 1.0)
                    
                    # fix: today_asset / yesterday_asset = today_price / yesterday_price
                    profit_fix[date] = pre_profit_fix
                    position_fix[date] = (cur_st_price *1.0) / (pre_st_price * 1.0) * (pre_position_fix * 1.0)
                    
                    pre_st_price = cur_st_price
                    pre_position_roll = position_roll[date]
                    pre_position_fix = position_fix[date]
                    in_market = True
                    pre_ticker = pre_ticker
                    pre_profit_fix = pre_profit_fix
                else: # swapping stock
                    action[date] = 'change holding'
                    position_roll[date] = pre_position_roll
                    position_fix[date] = pre_position_fix
                    
                    # close fix position
                    profit_fix[date] = pre_profit_fix + position_fix[date]
                    position_fix[date] = 0 # clear position
                    
                    # open position
                    position_fix[date] = fix_base
                    profit_fix[date] = profit_fix[date] - fix_base
                    
                    
                    pre_ticker = track[date]['ticker']
                    pre_st_price = track[date]['price']
                    in_market = True
                    pre_position_roll = pre_position_roll
                    pre_position_fix = position_fix[date]
                    pre_profit_fix = profit_fix[date]
            else: # return to no position
                action[date] = 'close all'
                position_roll[date] = pre_position_roll
                
                profit_fix[date] = pre_profit_fix + pre_position_fix
                position_fix[date] = 0 # clear position
                
                in_market = False
                pre_st_price = -1
                pre_ticker = -1
                pre_position_roll = pre_position_roll
                pre_position_fix = 0
                pre_profit_fix = profit_fix[date]
        else:
            # last trading day not in market
            if has_trade: # start a new trade from nothing, buy in
                action[date] = 'open position'
                position_roll[date] = pre_position_roll
                position_fix[date] = fix_base
                profit_fix[date] = pre_profit_fix - fix_base
                
                in_market = True
                pre_ticker = track[date]['ticker']
                pre_st_price = track[date]['price']
                pre_position_roll = pre_position_roll
                pre_position_fix = position_fix[date]
                pre_profit_fix = profit_fix[date]
            else: # keep nothing
                action[date] = 'keep nothing'
                position_roll[date] = pre_position_roll
                position_fix[date] = 0
                profit_fix[date] = pre_profit_fix
                
                in_market = False
                pre_position_roll = pre_position_roll
                pre_position_fix = 0
                pre_profit_fix = pre_profit_fix
                pre_ticker = '-1'
                pre_st_price = -1
        if track_id == 0:
            today_holding = track[date]['ticker'] if date in track.keys() else '-1'
            print(date, today_holding)
    rows = {}
    for date, p in position_roll.items():
        today_holding = track[date]['ticker'] if date in track.keys() else '-1'
        row = {
            'track_id': track_id,
            'date':date,
            'cash_roll': p,
            'cash_fix': position_fix[date] + profit_fix[date],
            'action': action[date],
            'today_holding': today_holding
        }
        rows[date] = row
        
        #debug info
        if debug_info:
            print(row['date'], row['cash_roll'], row['cash_fix'], row['action'], row['today_holding'])
    
    # to csv debug#########
    debug_df = pd.DataFrame(list(rows.values()))
    path = 'D:/f_data/temp/cashline_' + str(track_id) + '.csv'
    debug_df.to_csv(path, index=False)
    #######################
    return rows        
            
def roll_over_position_all_tracks(start_date, end_date, tracks):
    cash_fix = {}   
    cash_roll = {}   
    track_cnt = len(tracks)
    track_base = 1
    factor = track_base * 1.0 / track_cnt
    for idx, track in tracks.items():

        cash_df_one = roll_over_position(start_date, end_date, track, idx)
        
        for date, row in cash_df_one.items():
            if date not in cash_fix.keys():
                cash_fix[date] = 0
            if date not in cash_roll.keys():
                cash_roll[date] = 0
            cash_fix[date] = cash_fix[date] +  row['cash_fix']
            cash_roll[date] = cash_roll[date] +  row['cash_roll']
    # validation
    assert len(cash_fix) == len(cash_roll)
    for date in cash_fix.keys():
        assert date in cash_roll.keys()
    
    # reformat output
    rows = []
    for date, fix in cash_fix.items():
        roll = cash_roll[date]
        row = {
            'date': date,
            'fix': fix * factor,
            'roll': roll * factor
        }
        rows.append(row)
        
    rows_df = pd.DataFrame(rows)

    return rows_df
    