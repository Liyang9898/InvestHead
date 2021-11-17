from strategy_lib.strategy_util.signal import ma_exit_sequence

# def macd(enter_ma_signal, bar_yesterday):
#     if enter_ma_signal == "8_21":
#         return bar_yesterday['ema8_ema21_MACD'] > 0
#     elif enter_ma_signal == "21_50":
#         return bar_yesterday['ema21_ma50_MACD'] > 0
#     elif enter_ma_signal == "long_8_21_50":
#         return bar_yesterday['ema21_ma50_MACD'] > 0
# 
# 
# def all_ma_upwards(bar_yesterday):
#     return bar_yesterday['ema8_delta'] > 0 and bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0

def gen_exit_ma_macd(
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
    
    d = bar_yesterday['date']


    macd_green = (bar_yesterday['ema21_ma50_MACD'] > 0)
    ma_up_green = (bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0)


    if direction == 1:
        ma_exit_sequence_flag = ma_exit_sequence("8_21", bar_yesterday)
        if ma_exit_sequence_flag:
            direction = -1
            
            # exit on opening when yesterday ma is crashed
            return bar_today['open'] * direction
        
    # exit on price falls x% below previous peak
    if lowest_price < cut_off_price:
#         print(d, cut_off_price, previous_peak,'exit============')
        return cut_off_price * direction * -1        
        
        
    return exit_action

