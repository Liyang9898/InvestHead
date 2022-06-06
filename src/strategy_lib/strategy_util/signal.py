    
# computing if we should perform an action on channel information
def channel_green_light(percentile_bar, price_when_checking, is_enter):
    if is_enter:
        if price_when_checking < percentile_bar:
            return True
        else:
            return False
    else: # exit
        if price_when_checking > percentile_bar:
            return True
        else:
            return False


def ma_enter_sequence(enter_ma_signal, bar_yesterday):
    if enter_ma_signal == "8_21":
        return bar_yesterday['ema8'] > bar_yesterday['ema21']
    elif enter_ma_signal == "21_50":
        return bar_yesterday['ema21'] > bar_yesterday['ma50']
    elif enter_ma_signal == "long_8_21_50":
        return bar_yesterday['ema21'] > bar_yesterday['ma50'] and bar_yesterday['ema8'] > bar_yesterday['ema21']
    elif enter_ma_signal == "21_50_200":
        return bar_yesterday['ema21'] > bar_yesterday['ma50']


def ma_exit_sequence(exit_ma_signal, bar_yesterday):
    if exit_ma_signal == "not_long_8_21_50":
        return not (bar_yesterday['ema21'] > bar_yesterday['ma50'] and bar_yesterday['ema8'] > bar_yesterday['ema21'])
    elif exit_ma_signal == "8_21":
        return bar_yesterday['ema8'] < bar_yesterday['ema21']
    elif exit_ma_signal == "21_50":
        return bar_yesterday['ema21'] < bar_yesterday['ma50']
    elif exit_ma_signal == "8_50":
        return bar_yesterday['ema8'] < bar_yesterday['ma50']
    

def macd(enter_ma_signal, bar_yesterday):
    if enter_ma_signal == "8_21":
        return bar_yesterday['ema8_ema21_MACD'] > 0
    elif enter_ma_signal == "21_50":
        return bar_yesterday['ema21_ma50_MACD'] > 0
    elif enter_ma_signal == "long_8_21_50":
        return bar_yesterday['ema21_ma50_MACD'] > 0
    elif enter_ma_signal == "21_50_200":
        return bar_yesterday['ema21_ma50_MACD'] > 0


def trend_start(bar_yesterday):
    if bar_yesterday['ma_upcross_in_past_3days'] > 0:
        return True
    else:
        if bar_yesterday['ma_gap_reverse_in_past_6days'] > 0:
            return True
        else:
            return False
            
        
def all_ma_upwards(enter_ma_signal, bar_yesterday):
    if enter_ma_signal == "8_21":
        return bar_yesterday['ema8_delta'] > 0 and bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0

    elif enter_ma_signal == "21_50":
        return bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0

    elif enter_ma_signal == "21_50_200":
        return bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0 and bar_yesterday['ma200_delta'] > 0    


def ribbon_expanding(bar_yesterday):
    if bar_yesterday['ribbon_expand_seq'] >=1 and bar_yesterday['ribbon_expand_seq'] <=3:
#             print('catch')
        return True
    else:
#             print('not catch')
        return False
    
    
def ema21_ma50_gap_percent(bar_yesterday, ema21_ma50_gap_percent_threshold):
    if ema21_ma50_gap_percent_threshold < 0: # not enabled
        return True
    gap = bar_yesterday['ema21'] / bar_yesterday['ma50'] - 1
    if gap >= ema21_ma50_gap_percent_threshold:
        return True
    else: 
        return False