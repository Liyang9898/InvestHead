'''
Created on Jun 28, 2020

@author: leon
'''

from trading_floor.trading_util import unfinished_bar_best_price


def gen_entry(df, bar_idx, strategy):
    bar = df.iloc[bar_idx,:]

    ############################ entry strategy logic start ###########################################
    entry_action = strategy.gen_entry(df, bar_idx)
    ############################ entry strategy logic end #############################################
    
    if entry_action != 0: # open position
        entry_price = abs(entry_action)
        entry_ts = bar['est_datetime']
        position_direction = 1 if entry_action > 0 else -1
        entry_bar_id = bar_idx
        best_price=entry_price
        best_price = unfinished_bar_best_price(bar['open'], bar['close'], bar['high'], bar['low'], entry_price, position_direction)

        entry_info={
            "valid_entry":True,
            "entry_price":entry_price,
            "entry_ts":entry_ts,
            "position_direction":position_direction,
            "entry_bar_id":entry_bar_id,
            "best_price":best_price
        }
        return entry_info
    
    else:
        return {
            "valid_entry":False
        }