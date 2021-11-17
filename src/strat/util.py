'''
Created on Jan 26, 2020

@author: leon
'''
def update_low_up(in_market_bound, bar):
#     print(in_market_bound)
    if bar['high'] > in_market_bound['high']:
        in_market_bound['high'] = bar['high']
    if bar['low'] < in_market_bound['low']:
        in_market_bound['low'] = bar['low']
    return in_market_bound

def threshold_breach(threshold, in_market_bound, bar_cnt):
    for position, bar_cnt in threshold.items():
        if bar_cnt > -1:
            continue
        if position < in_market_bound['high'] and position > in_market_bound['low']:
            threshold[position] = bar_cnt
    return threshold