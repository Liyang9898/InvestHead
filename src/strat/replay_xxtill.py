from strat.util import update_low_up


def replay_xxtill(df_day, end_time, stop_gain, stop_loss, threshold):
    
#     stop_loss = 0.2
#     stop_gain = 0.3
#     threshold = 0.25
    in_market_bound = {
        'low':0,
        'high':0,
    }
    box_high = -1;
    box_low = 99999;
    single_direction = True
    previous_direction = 0;
    direction = 0
    bar_count = 0;
    in_market = False;
    long = False;
    entry_ts = ''
    entry_p = 0;
    exit_ts = ''
    exit_p = 0;
    pnl = 0;
    last_low = 0;
    last_high = 0;
    for index, row in df_day.iterrows():
#         bar_count
        bar_count = bar_count + 1;
        last_low = row['low']
        last_high = row['high']
        
        # in market bound update
        if in_market:
            in_market_bound = update_low_up(in_market_bound, row)
        
#         only use opening hour
        if row['est_time'] > end_time:
            break
        
#         get direction
        if bar_count > 1:
            previous_direction = direction
        direction = 0
        if row['close'] > row['open']:
            direction = 1
        elif row['close'] < row['open']:
            direction = -1
        if bar_count == 1 and abs(row['open'] - row['close']) < threshold:
#             print('first bar too small, open= '+ str(row['open']) + ' close=' + str(row['close']),  row['date'])
            direction = 0
        
        if bar_count > 1 and previous_direction != 0 and previous_direction != direction and single_direction == True:
            single_direction = False

        if not in_market:
            if direction == 1:
                if row['close'] > box_high + threshold and not single_direction:
                    # long in 
                    in_market = True
                    long = True
                    entry_ts = row['est_time']
                    entry_p = row['close']
            elif direction == -1:
                if row['close'] < box_low - threshold and not single_direction:
                    # short in 
                    in_market = True
                    long = False
                    entry_ts = row['est_time']
                    entry_p = row['close']
        else:
            if long: # long in market case
                if row['high'] > entry_p + stop_gain and row['close'] < row['open']: # stop gain
                    in_market = False
                    exit_ts = row['est_time']
                    exit_p = row['close']
                    pnl = exit_p-entry_p;
                    
                    
                elif row['low'] < entry_p - stop_loss: # stop loss
                    in_market = False
                    exit_ts = row['est_time']
                    exit_p = entry_p - stop_loss;
                    pnl = - stop_loss;
            else: # short in market case
                if row['low'] < entry_p - stop_gain and row['open'] < row['close']: # stop gain
                    in_market = False
                    exit_ts = row['est_time']
                    exit_p = row['close']
                    pnl = entry_p-exit_p
                    
                    
                elif row['high'] > entry_p + stop_loss: # stop loss
                    in_market = False
                    exit_ts = row['est_time']
                    exit_p = entry_p + stop_loss
                    pnl = - stop_loss
#         print(row['est_time'], box_high, box_low,single_direction,direction,'enter:', entry_ts,entry_p, 'exit:', exit_ts,exit_p,'pnl:',pnl)   

#  afk
        if exit_ts is not '':
            break
 
 #         box high low
        if max(row['open'], row['close']) > box_high:
            box_high = max(row['open'], row['close'])
        if min(row['open'], row['close']) < box_low:
            box_low = min(row['open'], row['close'])
    
#     still in market TODO: make it better
    if in_market:
        exit_ts = end_time
        if direction == 1:
            exit_p = last_high
        else:
            exit_p = last_low
        if long:
            pnl = 0
#             pnl = exit_p - entry_p
        else:
#             pnl = - exit_p + entry_p
            pnl = 0
            
    res = {
        'entry_ts':entry_ts,
        'entry_p':entry_p,
        'exit_ts':exit_ts,
        'exit_p':exit_p,
        'pnl':pnl,
        'is_long':long,
        'in_market_low':in_market_bound['low'],
        'in_market_high':in_market_bound['high']
    }
    return res
