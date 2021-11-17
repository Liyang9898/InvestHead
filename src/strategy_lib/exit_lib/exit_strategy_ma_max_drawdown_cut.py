from strategy_lib.strategy_util.signal import ma_exit_sequence


def gen_exit_ma_max_drawdown_cut(
        df, 
        bar_idx, 
        direction, 
        entry_bar_id, 
        price_peak_since_entry,
        # params
        exit_ma_signal,     
    ):
    MAX_DRAWDOWN_CUT_THRESHOLD=-0.2

    bar = df.iloc[bar_idx,:]
    bar_today = bar
    bar_yesterday = df.iloc[(bar_idx-1),:]
    exit_action = 0


    previous_peak = price_peak_since_entry
    
    lowest_price = bar_yesterday['low']
    cut_off_price = previous_peak * (1 + MAX_DRAWDOWN_CUT_THRESHOLD)
    
#     d = bar_yesterday['date']
#     print(d, down_from_peak, previous_peak)

        

    if direction == 1:
        ma_exit_sequence_flag = ma_exit_sequence(exit_ma_signal, bar_yesterday)
        if ma_exit_sequence_flag:
            direction = -1
            
            # exit on opening when yesterday ma is crashed
            return bar_today['open'] * direction
        
    # exit on price falls x% below previous peak
    if lowest_price < cut_off_price:
#         print(d, cut_off_price, previous_peak,'exit============')
        return cut_off_price * direction * -1
        
        
    return exit_action

