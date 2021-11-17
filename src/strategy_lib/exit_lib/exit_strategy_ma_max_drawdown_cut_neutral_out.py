from strategy_lib.strategy_util.signal import ma_exit_sequence


def gen_exit_ma_max_drawdown_cut_neutral(
        df, 
        bar_idx, 
        direction, 
        entry_bar_id, 
        entry_price,
        price_peak_since_entry,
        bars_totally_above_entry,
        valid_entry,
        # params
        exit_ma_signal,     
    ):
    MAX_DRAWDOWN_CUT_THRESHOLD=-0.2
    CONTINUES_ABOVE_ENTER_BAR_CNT_THRESHOLD = 4
    
    bar = df.iloc[bar_idx,:]
    bar_today = bar
    bar_yesterday = df.iloc[(bar_idx-1),:]
    exit_action = 0
    enter_bar = df.iloc[entry_bar_id,:]
    neutral_out_price = entry_price

    previous_peak = price_peak_since_entry
    
    lowest_price = bar_yesterday['low']
    cut_off_price = previous_peak * (1 + MAX_DRAWDOWN_CUT_THRESHOLD)
    
    d = bar_yesterday['date']
    enter_d = enter_bar['date']
    
    # ma sequence out
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
        
    
    touch_neutral_out_price = bar['low'] <= neutral_out_price
    neutral_out_enable = bars_totally_above_entry >= CONTINUES_ABOVE_ENTER_BAR_CNT_THRESHOLD
#     print(enter_d, d, bars_totally_above_entry, neutral_out_price, bar['low'], neutral_out_enable)
    # neutral out triggered
    if neutral_out_enable and touch_neutral_out_price and not valid_entry:
#         print('=================')
        return neutral_out_price * direction * -1    
        
        
    return exit_action

