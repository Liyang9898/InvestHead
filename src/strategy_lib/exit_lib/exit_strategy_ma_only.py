from strategy_lib.strategy_util.signal import ma_exit_sequence


def gen_exit_ma_only(
        df, 
        bar_idx, 
        direction, 

        # params
        exit_ma_signal,     
    ):

    bar = df.iloc[bar_idx,:]
    bar_today = bar
    bar_yesterday = df.iloc[(bar_idx-1),:]
    exit_action = 0

    if direction == 1:
        ma_exit_sequence_flag = ma_exit_sequence(exit_ma_signal, bar_yesterday)
        if ma_exit_sequence_flag:
            direction = -1
            
            # exit on opening when yesterday ma is crashed
            return bar_today['open'] * direction
        
    return exit_action

