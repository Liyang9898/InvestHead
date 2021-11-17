'''
Created on Dec 25, 2020

@author: leon
'''
from plotting_lib.simple import plotTimeSerisDic,plotTimeSerisDic3 

def genPositionHistory(price_with_indicator, trades, start_time, end_time):

    # price_list is a dic[ts, close_price]
    price_list = {}
    for i in range(0, len(price_with_indicator)):
        est_time = price_with_indicator.loc[i, 'est_datetime']
        if est_time < start_time or est_time > end_time:
            continue
        price_list[est_time] = price_with_indicator.loc[i, 'close']
    first_price=list(price_list.values())[0]
    first_ts=list(price_list.keys())[0]
#     print(price_list)
    
    
    # return is a dic[ts, position]
#         plotTimeSerisDic(price_list)
        
    valid_trade = []
    for trade in trades:
        # skip out of range
        if not (trade.entry_ts >= start_time and trade.exit_ts <= end_time):
            continue
        if trade.pnl==0:
            continue
        valid_trade.append(trade)
    if len(valid_trade) == 0:
        return
    
    cur = 0
#         in_trade_price_list = {}
    in_trade_price_section = []
    token = {}
    for ts, price in price_list.items():
        if cur > len(valid_trade) -1:
            break
        cur_trade = valid_trade[cur]
        if ts < cur_trade.entry_ts:
            continue
        elif ts == cur_trade.entry_ts:
            token = {}
            token[ts] = cur_trade.entry_price
        elif ts > cur_trade.entry_ts and ts < cur_trade.exit_ts:
            token[ts] = price
        elif ts == cur_trade.exit_ts:
            token[ts] = cur_trade.exit_price
            in_trade_price_section.append(token)
            cur = cur + 1
    in_trade_price_list=mergeListOfDic(in_trade_price_section)
    
    pivot = 1
    price_list_calibrated = {}
    for ts, p in price_list.items():
        factor = 1.0/valid_trade[0].entry_price
        price_list_calibrated[ts] = factor * p
    
    cash_position_during_trade_rollover=calibrate_rollover(valid_trade,in_trade_price_section)
    cash_position_during_trade_fixed_base=calibrate_fixed_based(valid_trade,in_trade_price_section)
    rollover_impute=impute(price_list_calibrated,cash_position_during_trade_rollover)
    fixed_base_impute=impute(price_list_calibrated,cash_position_during_trade_fixed_base)
    
    res = {
        'price_position':price_list_calibrated,
        'cash_rollover_position':rollover_impute,
        'cash_fixed_base_position':fixed_base_impute,
    }
    return res


def mergeListOfDic(l):
    res = {}
    for dic in l:
        res.update(dic)
    return res
        
def impute(price_list, cash_list):
    cash_list_imputed={}
    pre_cash = 1
    for ts,_p in price_list.items():
        if ts in cash_list.keys():
            cash_list_imputed[ts]=cash_list[ts]
        else:
            cash_list_imputed[ts] = pre_cash
        pre_cash = cash_list_imputed[ts]
    return cash_list_imputed
        
def calibrate_rollover(valid_trade,in_trade_price_section):
#     print(len(valid_trade), valid_trade)
#     print(len(in_trade_price_section), in_trade_price_section)
    # snowball:
    pivot = 1.0
    idx = 0
    in_trade_price_section_rollover = []
    token_rollover = {}
    while(idx<=len(valid_trade)-1):
        trade = valid_trade[idx]
        section = in_trade_price_section[idx]
        
#         x/p = pre_exit/cur_enter
        
        factor = pivot/trade.entry_price
        for ts, p in section.items():
            x = factor * p
            token_rollover[ts] = x
        pivot=trade.exit_price * factor
        idx=idx+1
        
        in_trade_price_section_rollover.append(token_rollover)
        token_rollover = {}
        

    in_trade_price_section_rollover_list=mergeListOfDic(in_trade_price_section_rollover)
    return in_trade_price_section_rollover_list

def calibrate_fixed_based(valid_trade,in_trade_price_section):
    # snowball:
    pivot = 1.0
    offset = 0
    idx = 0
    in_trade_price_section_rollover = []
    token_rollover = {}
    pre=0
    while(idx<=len(valid_trade)-1):
        trade = valid_trade[idx]
        section = in_trade_price_section[idx]
        
        factor = pivot/trade.entry_price
        
        for ts, p in section.items():
            x = factor * p +offset
            token_rollover[ts] = x 
            pre = x
#         pivot=trade.exit_price * factor
        offset = pre - 1
#         print('pre=',previous_exit)
        idx=idx+1
        
        in_trade_price_section_rollover.append(token_rollover)
        token_rollover = {}
        

    in_trade_price_section_rollover_list=mergeListOfDic(in_trade_price_section_rollover)
    return in_trade_price_section_rollover_list




# 
# def is_trade_day(date_time_obj):
#     
# # New Year's Day: Wednesday, Jan. 1
# # Martin Luther King Jr. Day: Monday, Jan. 20
# # Presidents’ Day: Monday, Feb. 17
# # Good Friday: Friday, April 10
# # Memorial Day: Monday, May 25
# # Independence Day: Friday, July 3 (observed, because July 4 falls on a Saturday)
# # Labor Day: Monday, Sept. 7
# # Thanksgiving Day: Thursday, Nov. 26
# # Christmas Day: Friday, Dec. 25
#     blacklist = [
#         ''    
#     ]
#     
#     weekno = date_time_obj.weekday()
# 
#     if weekno < 5:
#         # print "Weekday"
#         return True
#     else:  # 5 Sat, 6 Sun
#         # print "Weekend"
#         return False
# 
# 
# date_time_str = '1991-09-01 20:00:00'
# start_time_str = '1991-08-01 20:00:00'
# def trading_day_list(date_time_str, start_time_str):
#     date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
#     start_time_obj = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
#     res = []
#     while(date_time_obj>=start_time_obj):
#         if (is_trade_day(date_time_obj)):
#             res.append(date_time_obj)
#         next_obj = date_time_obj - timedelta(days=1)
#         date_time_obj=next_obj
#     return res
#         
# l=trading_day_list(date_time_str, start_time_str)
# print(l)