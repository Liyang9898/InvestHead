'''
Created on Feb 7, 2020

@author: leon
'''

OVERLAP_EMA21 = 'price overlap ema21'
BELOW_ENTRY = 'x% below entry'
HALF_MAX = 'drop to x% of max reach'
BREACH_RETURN = 'drop to entry after breach'
JUMP_RETURN = 'drop to entry after breach jump over'

SPEED = 'speed_ema8'
NEAR = 'near_ema8'

def speed_entry_price(day,trade, start_v, distance):
    if day['ema8_v'] < start_v:
        return None
    else:
        return day['close']
    

def near_ma_entry_price(day,trade, start_v, distance):
    if day['date'] is trade['enter_ts']:
        if abs(day['ema8'] - day['close']) / day['ema8'] > distance:
            return None
    else:
        if trade['direction'] is 'long':
            if day['low'] > day['ema8'] * (1+distance):
                return None
            else:
                if day['open'] < day['ema8'] * (1+distance):
                    return day['open']
                else:
                    return day['ema8'] * (1+distance)
        elif trade['direction'] is 'short':
            if day['high'] < day['ema8'] * (1-distance):
                return None
            else:
                if day['open'] > day['ema8'] * (1-distance):
                    return day['open']
                else:
                    return day['ema8'] * (1-distance)
    

def invalid_entry_condition(day,trade, start_v, distance, strat):
    enter_price_option = [day['close']]
    
    # not enough initial speed
    if SPEED in strat:
        p_speed = speed_entry_price(day,trade, start_v, distance)
        if p_speed is None:
            return None
        enter_price_option.append(p_speed)
    
    # too far away from ema
    if NEAR in strat:
        p_near = near_ma_entry_price(day,trade, start_v, distance)
        if p_near is None:
            return None
        enter_price_option.append(p_near)
    
    best_price = 0
    min_distance = 100
    for p in enter_price_option:
        distance = abs(day['ema8'] - p) / day['ema8']

        if distance < min_distance:
            min_distance = distance
            best_price = p

    return best_price
        

        

def improve_entry(df_day, trades, start_v, distance, strat):
    # we enter on bar close
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        trade['valid_entry'] = False

        for _index, day in df_day.loc[(df_day['date']>=s) & (df_day['date']<e)].iterrows():
            new_enter_price = invalid_entry_condition(day,trade, start_v, distance, strat)
            if new_enter_price is not None:
                trade['entry_ts_improved'] = day['date']
                trade['entry_p_improved'] = new_enter_price
                trade['valid_entry'] = True
                trade['entry_ema8_v'] = day['ema8_v']
                mid = (day['open'] + day['close']) / 2
                trade['entry_p2ema8_distance'] = abs(day['ema8'] - mid) / day['ema8']
                break
    
    return trades


def price_drop_x_percent(day, trade, threshold):
    enter_price = trade['entry_p_improved']
    if trade['direction'] is 'long':
        stoploss_p = enter_price - threshold * enter_price
        if day['low'] < stoploss_p:
            return stoploss_p
    elif trade['direction'] is 'short':
        stoploss_p = enter_price + threshold * enter_price
        if day['high'] > stoploss_p:
            return stoploss_p 
    return None


def price_drop_ma(day, trade):
    mid = (day['open'] + day['close']) / 2
    if trade['direction'] is 'long':
        if mid < day['ema21']:
            return day['ema21']
    elif trade['direction'] is 'short':
        if mid > day['ema21']:
            return day['ema21'] 
    return None


def price_breach_x_percent(day, trade, threshold):
    enter_price = trade['entry_p_improved']
    if trade['direction'] is 'long':
        breach = enter_price + threshold * enter_price
        if day['high'] > breach:
            return True
    elif trade['direction'] is 'short':
        breach = enter_price - threshold * enter_price
        if day['low'] < breach:
            return True 
    return False


def price_jump_over_positive(day, trade):
    enter_price = trade['entry_p_improved']
    if trade['direction'] is 'long':
        if min(day['open'], day['close']) > enter_price:
            return True
    elif trade['direction'] is 'short':
        if max(day['open'], day['close']) < enter_price:
            return True
    return False


def price_drop_x_percent_max_reach(day, trade, max_reach, percent):
    enter_price = trade['entry_p_improved']
    margin = abs(enter_price - max_reach) * (1 - percent)
    if trade['direction'] is 'long':
        stop = enter_price + margin
        if day['low'] < stop:
            if stop > day['high']:
                return day['high']
            else:
                return stop
    elif trade['direction'] is 'short':
        stop = enter_price - margin
        if day['high'] > stop:
            if stop < day['low']:
                return day['low']
            else:
                return stop 
    return None


def price_touch_entry(day, trade):
    enter_price = trade['entry_p_improved']
    if trade['direction'] is 'long':
        if day['low'] < enter_price:
            return True
    elif trade['direction'] is 'short':
        if day['high'] > enter_price:
            return True 
    return False


def update_max_reach(day, trade, max_reach):
    if trade['direction'] is 'long' and day['high'] > max_reach:
        return day['high']
    elif trade['direction'] is 'short' and day['low'] < max_reach:
        return day['low']
    return max_reach

        
def improve_exit(df_day, trades, threshold_below_entry, breach_threshold_above_entry, bar_count_threshold, max_reach_drop_percent, strat):
    cases = {}
    cases['drop to entry after breach'] = []
    cases['drop to x% of max reach'] = []
    # we enter on bar close and exit on bar close or mid
    for trade in trades:
        if not trade['valid_entry']:
            continue
        
        breach = False
        jump_over = False
        s = trade['entry_ts_improved']
        e = trade['exit_ts']
        trade['exit_ts_improved'] = trade['exit_ts']
        trade['exit_p_improved'] = trade['exit_p']
        trade['exit_reason'] = 'No longer in trend'
        max_reach = trade['entry_p_improved']
#         previous_max_reach = max_reach
        bar_count = 0

        for _index, day in df_day.loc[(df_day['date']>s) & (df_day['date']<=e)].iterrows():
#             previous_max_reach = max_reach
            max_reach = update_max_reach(day, trade, max_reach)
#             print(day['date'] + ' high:' + str(day['high']) + ' low:' + str(day['low']) + ' max_reach:' + str(max_reach))
            bar_count = bar_count + 1
            if not breach and price_breach_x_percent(day, trade, breach_threshold_above_entry):
                breach = True
            if not jump_over and price_jump_over_positive(day, trade):
                jump_over = True
            
            # exit on stop loss - x% below entry price
            if BELOW_ENTRY in strat:
                below_entry_stoploss = price_drop_x_percent(day, trade, threshold_below_entry)
                if below_entry_stoploss is not None:
                    trade['exit_ts_improved'] = day['date']
                    trade['exit_p_improved'] = below_entry_stoploss
                    trade['exit_reason'] = 'x% below entry'
                    break
                 
             
            # exit on enter price after breach if price goes back
            if BREACH_RETURN in strat:
                if breach and price_touch_entry(day, trade):
                    trade['exit_ts_improved'] = day['date']
                    if trade['direction'] is 'long':
                        trade['exit_p_improved'] = trade['entry_p_improved'] * 1.01
                    elif trade['direction'] is 'short':
                        trade['exit_p_improved'] = trade['entry_p_improved'] * 0.99
                    trade['exit_reason'] = 'drop to entry after breach'
                    cases[trade['exit_reason']].append(day['date'])
                    break
                
            
            
            # exit on enter price after jump over if price goes back
            if JUMP_RETURN in strat:
                if jump_over and price_touch_entry(day, trade):
                    trade['exit_ts_improved'] = day['date']
                    trade['exit_p_improved'] = trade['entry_p_improved']
                    trade['exit_reason'] = 'drop to entry after jump over'
                    break
   
                
            # exit when price dropped to x percent of max reach
            if HALF_MAX in strat:
                below_x_percent_max_reach_stoploss = price_drop_x_percent_max_reach(day, trade, max_reach, max_reach_drop_percent)
                if bar_count > bar_count_threshold and below_x_percent_max_reach_stoploss is not None:
                    trade['exit_ts_improved'] = day['date']
                    trade['exit_p_improved'] = below_x_percent_max_reach_stoploss
                    trade['exit_reason'] = 'drop to x% of max reach'
                    cases[trade['exit_reason']].append(day['date'])
                    break
                
                
            # exit on stop loss - bar mid below ema 21
            if OVERLAP_EMA21 in strat:
                below_ema21_stoploss = price_drop_ma(day, trade)
                if below_ema21_stoploss is not None:
                    trade['exit_ts_improved'] = day['date']
                    trade['exit_p_improved'] = below_ema21_stoploss
                    trade['exit_reason'] = 'price overlap ema21'
                    break

        if trade['direction'] is 'long':
            trade['pnl_improved'] = trade['exit_p_improved'] - trade['entry_p_improved']
        elif trade['direction'] is 'short':
            trade['pnl_improved'] = - trade['exit_p_improved'] + trade['entry_p_improved']
            
        trade['pnl%_improved'] = trade['pnl_improved'] / trade['entry_p_improved']
        trade['duration_bar_cnt'] = bar_count    
        trade['label'] = True if trade['pnl%_improved'] >= 0 else False
    return trades

def improve_entry_and_exit(
    df_day, 
    trades, 
    # enter params
    start_v, 
    distance,
    # exit params
    threshold_below_entry, 
    breach_threshold_above_entry, 
    bar_count_threshold, 
    max_reach_drop_percent,
    enter_impro_strat=[],
    exit_impro_strat=[]
):
    trades_entry_improved = improve_entry(
        df_day, 
        trades, 
        start_v, 
        distance,
        enter_impro_strat
    )
    
    trades_entry_exit_improved = improve_exit(
        df_day, 
        trades_entry_improved, 
        threshold_below_entry, 
        breach_threshold_above_entry, 
        bar_count_threshold, 
        max_reach_drop_percent,
        exit_impro_strat
    )
    return trades_entry_exit_improved

