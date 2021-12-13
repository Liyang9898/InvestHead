from strategy_lib.strategy_util.signal import channel_green_light, \
    ma_exit_sequence


def gen_exit_legacy(
        df, 
        bar_idx, 
        direction, 
        entry_price, 
        entry_bar_id, 
        current_bar_id, 
        best_price_in_market,# best price until last bar
        # params
        exit_ma_signal,
        enable_channel_exit,
        optional_channel_exit_condition,
        stop_profit_enable,
        profit_management_enable_threshold,
        neutual_exit_enable,
        exit_duration_threshiold,
        take_profit_above_x,
        take_profit_above_x_threshold        
    ):
    
#     exit_ma_signal  
#     enable_channel_exit
#     optional_channel_exit_condition
#     stop_profit_enable
#     profit_management_enable_threshold
#     neutual_exit_enable
#     exit_duration_threshiold
#     take_profit_above_x
#     take_profit_above_x_threshold
    
    bar = df.iloc[bar_idx,:]
    bar_today = bar
    bar_yesterday = df.iloc[(bar_idx-1),:]
    exit_action = 0
    
    # 
    price_when_checking=bar_today['open']
    
    
    if enable_channel_exit == 1 and price_when_checking > entry_price:
        optional_channel_exit_condition = channel_green_light(
            percentile_bar=bar_yesterday['barhigh_2_ema8_channel_mp75_pos'], 
            price_when_checking=price_when_checking, 
            is_enter=False
        )
        if optional_channel_exit_condition:
            if direction == 1:
                direction = -1
                return price_when_checking * direction                
            
            
            
    if stop_profit_enable:
        print('stop profit========================================')
        ################### take profit ###################################
        best_profit_p = best_price_in_market / entry_price - 1
        current_profit_low = bar['low'] / entry_price - 1
              

        profit_management_threshold = profit_management_enable_threshold
        breaching_profit_threshold = False
              
        take_profit= 0 # questionable?

        if best_profit_p > profit_management_threshold:
            print(best_profit_p, profit_management_threshold)
            breaching_profit_threshold = True
            take_profit = best_profit_p / 2
          
        if breaching_profit_threshold:
            take_profit_price = (take_profit + 1) * entry_price
            if bar['open'] < take_profit_price and bar['open'] > entry_price:
                # this is a bad case:
                # if the open price has already dropped below take profit price, but above entry price take it.
                # even worse, if it drop below enter price, we keep holding
                return -bar['open']
            
            else:
                if current_profit_low < take_profit:
                    return -take_profit_price
        ################### take profit ###################################
    
    
    if neutual_exit_enable:
        #neutral out validation
        bar_duration = bar_idx - entry_bar_id
#             offset = 0.002
        offset = 0
        neutral_out_price = entry_price * (1+offset)
        if bar_duration > exit_duration_threshiold:
            # check neutral out
            if bar['low'] < neutral_out_price and neutral_out_price < bar['high']:
#                     if bar['ma50'] < entry_price:
                    return -neutral_out_price 

    if direction == 1:
        ma_exit_sequence_flag = ma_exit_sequence(exit_ma_signal, bar_yesterday)
        if ma_exit_sequence_flag:
            direction = -1
            
            # exit on opening when yesterday ma is crashed
            return bar_today['open'] * direction
        
        ################### take_profit_above_x ###################################
        if take_profit_above_x:
            if bar['high'] >= entry_price * (1 + take_profit_above_x_threshold):
                return entry_price * (1 + take_profit_above_x_threshold) * direction
            
    return exit_action

