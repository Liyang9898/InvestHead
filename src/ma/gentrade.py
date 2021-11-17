'''
Created on Jan 29, 2020

@author: leon
'''

import copy 

from ma.plotindicator import plotpie
import pandas as pd


def gen_action_sequence_ab(df_day, ma_indicator):
    actions = {}
    # status could be long, short, close
    status = 'close'
    for index, day in df_day.iterrows():
        if day[ma_indicator] is 'long_sequence':
            if status is not 'long':
                status = 'long'
                actions[day['date']] = {'date':day['date'], 'action':'long', 'price':day['close']}
                continue
        if day[ma_indicator] is 'short_sequence':
            if status is not 'short':
                status = 'short'
                actions[day['date']] = {'date':day['date'], 'action':'short', 'price':day['close']}
                continue
    return actions

def gen_action_sequence_maintain_state(df_day, ma_indicator):
    actions = {}
    # status could be long, short, close
    status = 'close'
    for index, day in df_day.iterrows():
        if day[ma_indicator] is 'long_sequence':
            if status is not 'long':
                status = 'long'
                actions[day['date']] = {'date':day['date'], 'action':'long', 'price':day['close']}
                continue
        elif day[ma_indicator] is 'short_sequence':
            if status is not 'short':
                status = 'short'
                actions[day['date']] = {'date':day['date'], 'action':'short', 'price':day['close']}
                continue
        else:
            if status is 'long':
                status = 'close'
                actions[day['date']] = {'date':day['date'], 'action':'short', 'price':day['close']}
            elif status is 'short': 
                status = 'close'   
                actions[day['date']] = {'date':day['date'], 'action':'long', 'price':day['close']}
                
    return actions


def gen_action_sequence(df_day, ma_indicator):
    if ma_indicator is 'sequence_p_8_21':
        return gen_action_sequence_maintain_state(df_day, ma_indicator)
    else:
        return gen_action_sequence_ab(df_day, ma_indicator)

def gen_trade_specific(actions):    
    # gen trades
    trades = []
    status = 'close'     
    previous_enter_price = 0
    previous_enter_date = '-'
    for date, action in actions.items():
        if action['action'] is 'long':
            if status is 'short': #close previous position and create a trade
                trade = {
                    'direction':'short',
                    'enter_ts':previous_enter_date,
                    'exit_ts':date,
                    'pnl':previous_enter_price-action['price'],
                    'pnl %':(previous_enter_price-action['price']) / previous_enter_price,
                    'enter_p':previous_enter_price,
                    'exit_p':action['price'],
                }
                trade['label'] = True if trade['pnl'] > 0 else False
                trades.append(trade)
            previous_enter_price = action['price']
            previous_enter_date = date
            status = 'long'
        elif action['action'] is 'short':
            if status is 'long': #close previous position and create a trade
                trade = {
                    'direction':'long',
                    'enter_ts':previous_enter_date,
                    'exit_ts':date,
                    'pnl':action['price']-previous_enter_price,
                    'pnl %':(action['price']-previous_enter_price) / previous_enter_price,
                    'enter_p':previous_enter_price,
                    'exit_p':action['price'],
                }
                trade['label'] = True if trade['pnl'] > 0 else False
                trades.append(trade)
            previous_enter_price = action['price']
            previous_enter_date = date
            status = 'short'
            
    print('gen trades done')
    return trades

def gen_trades_always_in(df_day, ma_indicator):
    action_sequence = gen_action_sequence(df_day, ma_indicator)
  
    trades = gen_trade_specific(action_sequence)
    
#     trades = start_distance(df_day, trades)
#     trades = start_v(df_day, trades)
#     trades = gen_intrade_process_max_reach(df_day, trades)
# 
#     trades = gen_intrade_last_below_zero(df_day, trades)
# 
#     trades = max_down_pull_back(df_day, trades)

    return trades


def gen_intrade_process_single_direction(df_day, trades):
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        direction = trade['direction']
        previous_price = trade['enter_p']
        max_reach = trade['enter_p']
        for index, day in df_day.loc[(df_day['date']>s) & (df_day['date']<e)].iterrows():
            price = day['close']
            if direction is 'long':  
                if price >= previous_price:
                    max_reach = price
                else:
                    break
            elif direction is 'short':
                if price <= previous_price:
                    max_reach = price
                else:
                    break
            
            previous_price = price
        trade['max_reach'] = max_reach
        
        trade['pnl_max_reach'] = max_reach - trade['enter_p']
        if direction is 'short':
            trade['pnl_max_reach'] = trade['enter_p'] - max_reach
    return trades


def gen_intrade_last_below_zero(df_day, trades):
    for trade in trades:
        last_below_zero_ts = 0
        s = trade['enter_ts']
        e = trade['exit_ts']
        direction = trade['direction']
        counter = 0
        trade['last_below_zero_ts'] = 0
        for index, day in df_day.loc[(df_day['date']>=s) & (df_day['date']<=e)].iterrows():
            counter = counter + 1
            if (direction is 'long' and min(day['close'],day['open']) < trade['enter_p']) or (direction is 'short' and max(day['close'],day['open']) > trade['enter_p']):
                trade['last_below_zero_ts'] = counter
            trade['total_duration'] = counter
    return trades

def max_down_pull_back(df_day, trades):
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        direction = trade['direction']
        max_bot = trade['enter_p']
        for index, day in df_day.loc[(df_day['date']>=s) & (df_day['date']<=e)].iterrows():
            if (direction is 'long' and day['low'] < max_bot):
                max_bot = day['low']
            if (direction is 'short' and day['high'] > max_bot):
                max_bot = day['low']
        trade['max_pullback'] = -(abs(max_bot - trade['enter_p'])) / trade['enter_p']
    return trades


def start_distance(df_day, trades):
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        
        for index, day in df_day.loc[(df_day['date']>=s) & (df_day['date']<=e)].iterrows():
            trade['p2ema8_diatance %'] = abs(day['ema8_p_distance %'])
            break
            
    return trades


def start_v(df_day, trades):
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        
        for index, day in df_day.loc[(df_day['date']>=s) & (df_day['date']<=e)].iterrows():
            trade['start_v'] = abs(day['ema8_v'])
            break
            
    return trades



def gen_intrade_process_max_reach(df_day, trades):
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        direction = trade['direction']

        max_reach = trade['enter_p']
        for index, day in df_day.loc[(df_day['date']>s) & (df_day['date']<e)].iterrows():
            price = day['close']
            if direction is 'long':  
                if price >= max_reach:
                    max_reach = price
            elif direction is 'short':
                if price <= max_reach:
                    max_reach = price

        trade['max_reach'] = max_reach
        
        trade['pnl_max_reach'] = max_reach - trade['enter_p']
        if direction is 'short':
            trade['pnl_max_reach'] = trade['enter_p'] - max_reach
    return trades


def exit_when_drop(df_day, trades, initial_count, breakout_threshold, remain_percent):
    for trade in trades:
        s = trade['enter_ts']
        e = trade['exit_ts']
        direction = trade['direction']

        max_reach = trade['enter_p']
        count = 0
        stop_price = max_reach
        is_breach= False
        for index, day in df_day.loc[(df_day['date']>s) & (df_day['date']<e)].iterrows():
            count = count + 1
            price = day['close']
            if direction is 'long':  
                if (day['high']-trade['enter_p']) / trade['enter_p'] > breakout_threshold and not is_breach:
                    is_breach = True
                if price >= max_reach:
                    max_reach = price
                    max_delta = abs(max_reach-trade['enter_p'])
                    stop_price = trade['enter_p'] + max_delta * remain_percent
            elif direction is 'short':
                if (day['low']-price) / trade['enter_p'] > breakout_threshold and not is_breach:
                    is_breach = True
                if price <= max_reach:
                    max_reach = price
                    max_delta = abs(max_reach-trade['enter_p'])
                    stop_price = trade['enter_p'] - max_delta * remain_percent
            
            if count > initial_count or is_breach:
                if direction is 'long':  
                    if price <= stop_price:
                        # close
                        new_exit_p = stop_price
                        new_exit_ts = day['date']
                        
                        trade['drop_exit_p'] = new_exit_p
                        trade['drop_exit_ts'] = new_exit_ts
                        trade['de_pnl'] = new_exit_p - trade['enter_p']
                        trade['de_pnl %'] = (new_exit_p-trade['enter_p']) / trade['enter_p']

                        break
                elif direction is 'short':
                    if price >= stop_price:
                        # close
                        new_exit_p = stop_price
                        new_exit_ts = day['date']
                        
                        trade['drop_exit_p'] = new_exit_p
                        trade['drop_exit_ts'] = new_exit_ts
                        trade['de_pnl'] =  trade['enter_p'] -new_exit_p
                        trade['de_pnl %'] = (trade['enter_p'] -new_exit_p) / trade['enter_p']
                        break

        
    return trades

            
def trade_summary_direction(trades, direction):
    sum = 0
    pnl_p_total = 0
    count = 0
    count_p = 0
    count_p_single = 0
    for trade in trades:
        if trade['direction'] is direction:
            count = count + 1
            if trade['pnl'] > 0:
                count_p = count_p + 1
            if trade['pnl_max_reach'] > 0:
                count_p_single = count_p_single + 1    
            sum = sum + trade['pnl']
            pnl_p_total = pnl_p_total + trade['pnl %']
#             print_trade(trade)
    rate = count_p / count
    rate_single = count_p_single / count
    print(str(sum)  + ' pnl % total:' + str(round(pnl_p_total, 6)) + ' win rate: ' + str(round(rate,6)) + ' single_side_win_rate: ' + str(round(rate_single,6)))
    return {
        'pnl':pnl_p_total,
        'rate':rate,
        'rate_max':rate_single,
        'total_trade':count,
    }


     
def trade_summary_direction_early_exit(trades, direction):
    trades_early_exit = copy.deepcopy(trades)
    
    for trade in trades_early_exit:
        if 'de_pnl' in trade:
            trade['pnl'] = trade['de_pnl']
            trade['pnl %'] = trade['de_pnl %']
    sum = 0
    pnl_p_total = 0
    count = 0
    count_p = 0
    count_p_single = 0
    for trade in trades_early_exit:
        if trade['direction'] is direction:
            count = count + 1
            if trade['pnl'] > 0:
                count_p = count_p + 1
            if trade['pnl_max_reach'] > 0:
                count_p_single = count_p_single + 1    
            sum = sum + trade['pnl']
            pnl_p_total = pnl_p_total + trade['pnl %']
#             print_trade(trade)
    rate = count_p / count
    rate_single = count_p_single / count
    print(str(sum)  + ' pnl % total:' + str(round(pnl_p_total, 6)) + ' win rate: ' + str(round(rate,6)) + ' single_side_win_rate: ' + str(round(rate_single,6)))
    return {
        'pnl':pnl_p_total,
        'rate':rate,
#         'rate_max':rate_single,
        'total_trade':count,
    }
    

     
def trade_summary_direction_early_exit_high_v(trades, direction, v_threshold):
    trades_early_exit = copy.deepcopy(trades)
    
    high_v_entry_trade = []
    for trade in trades_early_exit:
        if trade['start_v'] > v_threshold:
            high_v_entry_trade.append(trade)
    
    
    for trade in high_v_entry_trade:
        if 'de_pnl' in trade:
            trade['pnl'] = trade['de_pnl']
            trade['pnl %'] = trade['de_pnl %']
    sum = 0
    pnl_p_total = 0
    count = 0
    count_p = 0
    count_p_single = 0
    for trade in high_v_entry_trade:
        if trade['direction'] is direction:
            count = count + 1
            if trade['pnl'] > 0:
                count_p = count_p + 1
            if trade['pnl_max_reach'] > 0:
                count_p_single = count_p_single + 1    
            sum = sum + trade['pnl']
            pnl_p_total = pnl_p_total + trade['pnl %']
            print_trade(trade)
    rate = count_p / count
    rate_single = count_p_single / count
    print(str(sum)  + ' pnl % total:' + str(round(pnl_p_total, 6)) + ' win rate: ' + str(round(rate,6)) + ' single_side_win_rate: ' + str(round(rate_single,6)))
    return {
        'pnl':pnl_p_total,
        'rate':rate,
#         'rate_max':rate_single,
        'total_trade':count,
    }
#     


     
def trade_summary_direction_early_exit_high_v_close_ma(trades, direction, v_threshold,distance):
    trades_early_exit = copy.deepcopy(trades)
    
    high_v_entry_trade = []
    for trade in trades_early_exit:
        if trade['start_v'] > v_threshold and trade['p2ema8_diatance %'] < distance:
            high_v_entry_trade.append(trade)
    
    
    for trade in high_v_entry_trade:
        if 'de_pnl' in trade:
            trade['pnl'] = trade['de_pnl']
            trade['pnl %'] = trade['de_pnl %']
    sum = 0
    pnl_p_total = 0
    count = 0
    count_p = 0
    count_p_single = 0
    for trade in high_v_entry_trade:
        if trade['direction'] is direction:
            count = count + 1
            if trade['pnl'] > 0:
                count_p = count_p + 1
            if trade['pnl_max_reach'] > 0:
                count_p_single = count_p_single + 1    
            sum = sum + trade['pnl']
            pnl_p_total = pnl_p_total + trade['pnl %']
            print_trade(trade)
    rate = count_p / count
    rate_single = count_p_single / count
    print(str(sum)  + ' pnl % total:' + str(round(pnl_p_total, 6)) + ' win rate: ' + str(round(rate,6)) + ' single_side_win_rate: ' + str(round(rate_single,6)))
    return {
        'pnl':pnl_p_total,
        'rate':rate,
#         'rate_max':rate_single,
        'total_trade':count,
    }

     
def trade_summary_direction_high_v_entry(trades, direction, v_threshold):
    high_v_entry_trade = []
    for trade in trades:
        if trade['start_v'] > v_threshold:
            high_v_entry_trade.append(trade)
    
    sum = 0
    pnl_p_total = 0
    count = 0
    count_p = 0
    count_p_single = 0
    for trade in high_v_entry_trade:
        if trade['direction'] is direction:
            count = count + 1
            if trade['pnl'] > 0:
                count_p = count_p + 1
            if trade['pnl_max_reach'] > 0:
                count_p_single = count_p_single + 1    
            sum = sum + trade['pnl']
            pnl_p_total = pnl_p_total + trade['pnl %']
#             print_trade(trade)
    rate = count_p / count
    rate_single = count_p_single / count
    print(str(sum)  + ' pnl % total:' + str(round(pnl_p_total, 6)) + ' win rate: ' + str(round(rate,6)) + ' single_side_win_rate: ' + str(round(rate_single,6)))
    return {
        'pnl':pnl_p_total,
        'rate':rate,
#         'rate_max':rate_single,
        'total_trade':count,
    }


def trade_summary_direction_close_ma(trades, direction, distance_threshold):
    close_ma_entry_trade = []
    for trade in trades:
        if trade['p2ema8_diatance %'] < distance_threshold:
            close_ma_entry_trade.append(trade)
    
    sum = 0
    pnl_p_total = 0
    count = 0
    count_p = 0
    count_p_single = 0
    for trade in close_ma_entry_trade:
        if trade['direction'] is direction:
            count = count + 1
            if trade['pnl'] > 0:
                count_p = count_p + 1
            if trade['pnl_max_reach'] > 0:
                count_p_single = count_p_single + 1    
            sum = sum + trade['pnl']
            pnl_p_total = pnl_p_total + trade['pnl %']
#             print_trade(trade)
    rate = count_p / count
    rate_single = count_p_single / count
    print(str(sum)  + ' pnl % total:' + str(round(pnl_p_total, 6)) + ' win rate: ' + str(round(rate,6)) + ' single_side_win_rate: ' + str(round(rate_single,6)))
    return {
        'pnl':pnl_p_total,
        'rate':rate,
#         'rate_max':rate_single,
        'total_trade':count,
    }


    
def print_trade(trade):
        print(trade['enter_ts'] + ' pnl%:' + percent_str(trade['pnl %']) + ' ' + trade['direction'] + ' v %:' + percent_str(trade['start_v']) + ' p2ema8_diatance %:' + percent_str(trade['p2ema8_diatance %']) + ' max_pullback:' + percent_str(trade['max_pullback'])  + '%  bz:' + str(trade['last_below_zero_ts']) + ' duration:' + str(trade['total_duration']) + ' enter:' + str(trade['enter_p']) + ' exit:' + str(trade['exit_p']))

def print_trade_early_exit(trade):
        print(trade['enter_ts'] + ' ' + trade['direction'] + ' pnl:' + percent_str(trade['pnl %'])  + ' NEW pnl:' + percent_str(trade['de_pnl %']) + ' bz:' + str(trade['last_below_zero_ts']) + ' duration:' + str(trade['total_duration']) + ' enter:' + str(trade['enter_p']) + ' exit:' + str(trade['exit_p']) + ' early_exit:' + str(trade['drop_exit_p']))


def trade_win_lose_v_diff(trades):

    win_duration = {}
    lose_duration = {}
    for trade in trades:
        if trade['pnl'] > 0:
            if trade['start_v'] not in win_duration.keys():
                win_duration[trade['start_v']] = 0
            win_duration[trade['start_v']] = win_duration[trade['start_v']] + 1
        else:    
            if trade['start_v'] not in lose_duration.keys():
                lose_duration[trade['start_v']] = 0
            lose_duration[trade['start_v']] = lose_duration[trade['start_v']] + 1
    return {
        'w':win_duration,
        'l':lose_duration,
    }


def trade_win_lose_diff(trades):

    win_duration = {}
    lose_duration = {}
    for trade in trades:
        if trade['pnl'] > 0:
            if trade['total_duration'] not in win_duration.keys():
                win_duration[trade['total_duration']] = 0
            win_duration[trade['total_duration']] = win_duration[trade['total_duration']] + 1
        else:    
            if trade['total_duration'] not in lose_duration.keys():
                lose_duration[trade['total_duration']] = 0
            lose_duration[trade['total_duration']] = lose_duration[trade['total_duration']] + 1
    return {
        'w':win_duration,
        'l':lose_duration,
    }
    
    
def trade_win_lose_p2ema_diff(trades):

    win_duration = {}
    lose_duration = {}
    for trade in trades:
        if trade['pnl'] > 0:
            if trade['p2ema8_diatance %'] not in win_duration.keys():
                win_duration[trade['p2ema8_diatance %']] = 0
            win_duration[trade['p2ema8_diatance %']] = win_duration[trade['p2ema8_diatance %']] + 1
        else:    
            if trade['p2ema8_diatance %'] not in lose_duration.keys():
                lose_duration[trade['p2ema8_diatance %']] = 0
            lose_duration[trade['p2ema8_diatance %']] = lose_duration[trade['p2ema8_diatance %']] + 1
    return {
        'w':win_duration,
        'l':lose_duration,
    }
    
def trade_win_lose_bz(trades):

    win_duration = {}
    lose_duration = {}
    for trade in trades:
        if trade['pnl'] > 0:
            if trade['last_below_zero_ts'] not in win_duration.keys():
                win_duration[trade['last_below_zero_ts']] = 0
            win_duration[trade['last_below_zero_ts']] = win_duration[trade['last_below_zero_ts']] + 1
        else:    
            if trade['last_below_zero_ts'] not in lose_duration.keys():
                lose_duration[trade['last_below_zero_ts']] = 0
            lose_duration[trade['last_below_zero_ts']] = lose_duration[trade['last_below_zero_ts']] + 1
    return {
        'w':win_duration,
        'l':lose_duration,
    }


def df2dic(trades_df, colume_name):
    res = {}
    for index, trade in trades_df.iterrows():
        val = trade[colume_name]
        if val not in res:
            res[val] = 0
        res[val] = res[val] + 1
    return res


def percent_str(num):
    return (str(round(num * 100, 2)) + '%')


def early_exit_improvement(trades):
    win = 0
    lose = 0
    improved = 0
    for trade in trades:
        if 'drop_exit_p' in trade:
#             print_trade_early_exit(trade)
            improved = improved + 1
        if trade['pnl'] > 0:
            win = win + 1
        else:
            lose = lose + 1
    print('win:'+str(win)+ ' lose:'+str(lose)+' improved:'+str(improved))
    

def max_pullback(trades):
    print('==================win===============')
    for trade in trades:
        if trade['pnl'] >0:
            print_trade(trade)
    print('==================lose===============')
    for trade in trades:
        if trade['pnl'] <0:
            print_trade(trade)


def trade_summary(trades):
    long =trade_summary_direction(trades, 'long')
    short =trade_summary_direction(trades, 'short')
#     print(duration)
    return {
        'pnl_long %':percent_str(long['pnl']),
        'rate_long':percent_str(long['rate']),
        'rate_max_long':percent_str(long['rate_max']),
        'trade_cnt_long':str(long['total_trade']),
        
        'pnl_short %':percent_str(short['pnl']),
        'rate_short':percent_str(short['rate']),
        'rate_max_short':percent_str(short['rate_max']),
        'trade_cnt_short':str(short['total_trade']),
    }
    
def trade_summary_early_exit(trades):
    long =trade_summary_direction_early_exit(trades, 'long')
    short =trade_summary_direction_early_exit(trades, 'short')
#     duration = trade_win_lose_diff(trades)
#     bz = trade_win_lose_bz(trades)
#     plotpie(bz['w'], 'win_bz_duration')
#     plotpie(bz['l'], 'lose_bz_duration')
#     print(duration)
    return {
        'pnl_long %':percent_str(long['pnl']),
        'rate_long':percent_str(long['rate']),
#         'rate_max_long':percent_str(long['rate_max']),
        'trade_cnt_long':str(long['total_trade']),
        
        'pnl_short %':percent_str(short['pnl']),
        'rate_short':percent_str(short['rate']),
#         'rate_max_short':percent_str(short['rate_max']),
        'trade_cnt_short':str(short['total_trade']),
    }
    
    
def trade_summary_high_v_entry(trades,v_threshold):
    long =trade_summary_direction_high_v_entry(trades, 'long',v_threshold)
    short =trade_summary_direction_high_v_entry(trades, 'short', v_threshold)
#     duration = trade_win_lose_diff(trades)
#     bz = trade_win_lose_bz(trades)
#     plotpie(bz['w'], 'win_bz_duration')
#     plotpie(bz['l'], 'lose_bz_duration')
#     print(duration)
    return {
        'pnl_long %':percent_str(long['pnl']),
        'rate_long':percent_str(long['rate']),
#         'rate_max_long':percent_str(long['rate_max']),
        'trade_cnt_long':str(long['total_trade']),
        
        'pnl_short %':percent_str(short['pnl']),
        'rate_short':percent_str(short['rate']),
#         'rate_max_short':percent_str(short['rate_max']),
        'trade_cnt_short':str(short['total_trade']),
    }
    
    
def trade_summary_close_ma(trades,threshold):
    long =trade_summary_direction_close_ma(trades, 'long',threshold)
    short =trade_summary_direction_close_ma(trades, 'short', threshold)
#     duration = trade_win_lose_diff(trades)
#     bz = trade_win_lose_bz(trades)
#     plotpie(bz['w'], 'win_bz_duration')
#     plotpie(bz['l'], 'lose_bz_duration')
#     print(duration)
    return {
        'pnl_long %':percent_str(long['pnl']),
        'rate_long':percent_str(long['rate']),
#         'rate_max_long':percent_str(long['rate_max']),
        'trade_cnt_long':str(long['total_trade']),
        
        'pnl_short %':percent_str(short['pnl']),
        'rate_short':percent_str(short['rate']),
#         'rate_max_short':percent_str(short['rate_max']),
        'trade_cnt_short':str(short['total_trade']),
    }    
    
    

def trade_summary_early_exit_high_v(trades,v_threshold):
    long =trade_summary_direction_early_exit_high_v(trades, 'long',v_threshold)
    short =trade_summary_direction_early_exit_high_v(trades, 'short', v_threshold)
#     duration = trade_win_lose_diff(trades)
#     bz = trade_win_lose_bz(trades)
#     plotpie(bz['w'], 'win_bz_duration')
#     plotpie(bz['l'], 'lose_bz_duration')
#     print(duration)
    return {
        'pnl_long %':percent_str(long['pnl']),
        'rate_long':percent_str(long['rate']),
#         'rate_max_long':percent_str(long['rate_max']),
        'trade_cnt_long':str(long['total_trade']),
        
        'pnl_short %':percent_str(short['pnl']),
        'rate_short':percent_str(short['rate']),
#         'rate_max_short':percent_str(short['rate_max']),
        'trade_cnt_short':str(short['total_trade']),
    }


def trade_summary_early_exit_high_v_close_ma(trades,v_threshold,distance):
    long =trade_summary_direction_early_exit_high_v_close_ma(trades, 'long',v_threshold,distance)
    short =trade_summary_direction_early_exit_high_v_close_ma(trades, 'short', v_threshold,distance)
#     duration = trade_win_lose_diff(trades)
#     bz = trade_win_lose_bz(trades)
#     plotpie(bz['w'], 'win_bz_duration')
#     plotpie(bz['l'], 'lose_bz_duration')
#     print(duration)
    return {
        'pnl_long %':percent_str(long['pnl']),
        'rate_long':percent_str(long['rate']),
#         'rate_max_long':percent_str(long['rate_max']),
        'trade_cnt_long':str(long['total_trade']),
        
        'pnl_short %':percent_str(short['pnl']),
        'rate_short':percent_str(short['rate']),
#         'rate_max_short':percent_str(short['rate_max']),
        'trade_cnt_short':str(short['total_trade']),
    }



def feature_distribution(trades_df,column_name):
    trades_df_win = trades_df.loc[trades_df['label'] == True]
    trades_df_lose = trades_df.loc[trades_df['label'] == False]
    trades_dic_win = df2dic(trades_df_win, 'p2ema8_diatance %')
    trades_dic_lose = df2dic(trades_df_lose, 'p2ema8_diatance %')

    plotpie(trades_dic_win, 'win')
    plotpie(trades_dic_lose, 'lose')

def gen_trade_df(trades):
    trades_df = pd.DataFrame(trades)
    trades_df['label'] = trades_df.apply(lambda row : gen_trade_label(row), axis = 1)
    return trades_df
    
    
def gen_trade_label(trade):
    if trade['pnl %'] > 0:
        return True
    else:
        if trade['de_pnl %'] > 0:
            return True
        else:
            return False
        
def gen_trade_summary(trades):
    win = 0
    lose = 0
    neu = 0
    pnl = 0
    for trade in trades:
        if not trade['valid_entry']:
            continue

        if trade['pnl%_improved']>0:
            win = win + 1
        elif trade['pnl%_improved']<0:
            lose = lose + 1
        else:
            neu=neu+1
            
        pnl = pnl + trade['pnl%_improved']  
    res = {
        'win rate':0,
        'lose rate':0,
        'neu rate':0,
        'total trades': win + lose,
        'win': win,
        'lose':lose,
        'pnl':pnl
    }
    if (win + lose + neu) !=0:
        res['win rate']=win / (win + lose + neu)
        res['lose rate']=lose / (win + lose + neu)
        res['neu rate']=neu / (win + lose + neu)
    return res


        
def gen_trade_summary_long(trades):
    win = 0
    lose = 0
    neu = 0
    pnl = 0
    for trade in trades:
        if trade['direction'] is 'short':
            continue
        
        if not trade['valid_entry']:
            continue

        if trade['pnl%_improved']>0:
            win = win + 1
        elif trade['pnl%_improved']<0:
            lose = lose + 1
        else:
            neu=neu+1
            
        pnl = pnl + trade['pnl%_improved']  
    res = {
        'win rate':0,
        'lose rate':0,
        'neu rate':0,
        'total trades': win + lose,
        'win': win,
        'lose':lose,
        'pnl':pnl
    }
    if (win + lose + neu) !=0:
        res['win rate']=win / (win + lose + neu)
        res['lose rate']=lose / (win + lose + neu)
        res['neu rate']=neu / (win + lose + neu)
    return res

    
def gen_trade_summary_raw(trades):
    win = 0
    lose = 0
    pnl = 0
    for trade in trades:
        if trade['label']:
            win = win + 1
        else:
            lose = lose + 1
            
        pnl = pnl + trade['pnl %']
        
        
    
    res = {
        'success rate':0,
        'total trades': win + lose,
        'win': win,
        'lose':lose,
        'pnl':pnl
    }
    if win + lose != 0:
        res['success rate'] = win / (win + lose)

    return res
        

def print_trades(trades):
    print('=======================win=====================')
    for trade in trades:
        if trade['label']:
            print(trade)
    print('=======================lose=====================')
    for trade in trades:
        if not trade['label']:
            print(trade)
            


def print_trades_long(trades):
    print('=======================win=====================')
    for trade in trades:
        if trade['label'] and trade['direction'] is 'long':
            print(trade)
    print('=======================lose=====================')
    for trade in trades:
        if not trade['label'] and trade['direction'] is 'long':
            print(trade)