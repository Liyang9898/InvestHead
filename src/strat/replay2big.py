

def replay2big(df_day,stop_gain,stop_loss,bigbarsize):
    
    in_market = False;
#     bigbarsize = 0.2
#     stop_loss = 2
#     stop_gain = 1
    threshold = 0.25
    box_high = -1;
    box_low = 99999;
    single_direction = True
    previous_direction = 0;
    direction = 0
    in_count = 0;

    long = False;
    entry_ts = ''
    entry_p = 0;
    exit_ts = ''
    exit_p = 0;
    pnl = 0;
    last_low = 0;
    last_high = 0;
    res_all = {}
    
    for index, row in df_day.iterrows():
        if row['est_time'] > '09:35:00' and not in_market:
            break
        if not in_market:
            if abs(row['open'] - row['close']) < bigbarsize:
                continue
            if row['open'] < row['close']:
                direction = 1
                long = True
            else:
                direction = -1
            entry_ts = row['est_time']
            entry_p = row['close']
            in_count = 1;
            in_market = True
        else:
            in_count = in_count + 1
            # stop loss
            if (direction == 1 and row['low'] < entry_p - stop_loss) or (direction == -1 and row['high'] > entry_p + stop_loss):
                exit_ts = row['est_time']
                exit_p = entry_p - stop_loss * direction
                pnl = -stop_loss
                res = {
                    'entry_ts':entry_ts,
                    'entry_p':entry_p,
                    'exit_ts':exit_ts,
                    'exit_p':exit_p,
                    'pnl':pnl,
                    'is_long':long
                }
                res_all[entry_ts] = res
                in_market = False
                continue
#                 print('stoploss dead')
            if in_count == 2:
                stop_gain_price = entry_p + direction * stop_gain
                
                # stop gain
                if (direction == 1 and row['high'] > stop_gain_price) or (direction == -1 and row['low'] < stop_gain_price):
                    exit_ts = row['est_time']
                    res = {
                        'entry_ts':entry_ts,
                        'entry_p':entry_p,
                        'exit_ts':exit_ts,
                        'exit_p':stop_gain_price,
                        'pnl':stop_gain,
                        'is_long':long
                    }
                    res_all[entry_ts] = res
                    in_market = False
#                     print('stop gain')
                    continue
                
                # 2nd bar positive close
                if (direction == 1 and row['close'] > entry_p) or (direction == -1 and row['close'] < entry_p):
                    exit_ts = row['est_time']
                    exit_p = entry_p + direction * abs(row['close'] - entry_p)
                    res = {
                        'entry_ts':entry_ts,
                        'entry_p':entry_p,
                        'exit_ts':exit_ts,
                        'exit_p':exit_p,
                        'pnl':abs(row['close'] - entry_p),
                        'is_long':long
                    }
                    res_all[entry_ts] = res
                    in_market = False
#                     print('positive close')
                    continue
                
                
            else:
                # neutral out
                if entry_p < row['high'] and entry_p > row['low']:
                    exit_ts = row['est_time']
                    exit_p = entry_p
                    res = {
                        'entry_ts':entry_ts,
                        'entry_p':entry_p,
                        'exit_ts':exit_ts,
                        'exit_p':exit_p,
                        'pnl':0,
                        'is_long':long
                    }
                    res_all[entry_ts] = res
                    in_market = False
                    continue

 
    return res_all
