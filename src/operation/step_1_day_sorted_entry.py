'''
Created on Mar 11, 2021

@author: leon
'''
from datetime import datetime, timedelta

from operation.lib.stock_ranking import get_stock_ranking
from operation.lib.trade_lib import batch_tradable, get_opened_position, \
    update_record_current_price, \
    price_section, BELOW_ENTER, ABOVE_STOP, ABOVE_ENTER_NO_STOP, \
    BETWEEN_STOP_ENTER
from operation.lib.trade_lib import process_trade_channel_position
from strategy_lib.stratage_param import (
#     strat_param_swing,
    strat_param_swing_2150in_2150out_ma_gap
)
from util.util import sort_dic_by_val
from version_master.version import op_path_base
from version_master.version import swing_set1, swing_set_20220103


"""
this process provides new training opportunities
"""

def pct_fmt(n):
    price_str = "{:.2f}%".format(n*100, 2)
    return price_str

position_cash = 10000

now = datetime.today()
# print(now)
# now = now - timedelta(days=1)
# print(now)
now_str = now.strftime('%Y-%m-%d')

path_base = op_path_base + now_str
op_path_indicator = path_base + '/indicator/'


strategy_param_bundle=strat_param_swing_2150in_2150out_ma_gap
offset=0


possible_entry = batch_tradable(
    op_path_indicator, 
    strategy_param_bundle,
    offset
)
"""
until here, I got a list of entry
"""

opened_position = get_opened_position() # lower case
stock_ranking = get_stock_ranking()

res = {}
price_info = {}

for ticker, trade in possible_entry.items():
    channel = process_trade_channel_position(trade)

    channel_ema21 = trade['bar_today']['barlow_2_ema21_percent_oneyear_channel_percentile']
    
    gap_ma50 = trade['bar_today']['close'] / trade['bar_today']['ma50'] - 1
    entry_info=trade['entry_info']

    res[ticker] = stock_ranking[ticker.upper()]
    price_info[ticker.lower()] = entry_info


possible_entry_sorted = sort_dic_by_val(res,descending=True)
"""
until here we got a list of possible entry ticker sorted by ma50_gap
"""

def print_tradable(opened):
    for ticker in possible_entry_sorted.keys():
        if opened and ticker not in opened_position:
            continue
        
        if not opened and ticker in opened_position:
            continue        
            

        # how many share to buy
        cnt = position_cash/price_info[ticker]['entry_price']
        cnt_str = "{:.2f}".format(round(cnt, 2))
        
        # price info
        price_str = str(round(price_info[ticker]['entry_price'], 2))
        ts_str = price_info[ticker]['entry_ts'].split(' ')[0]
        
        
        bar_today = possible_entry[ticker]['bar_today']
        bar_yesterday = possible_entry[ticker]['bar_yesterday']
        gap_ma50 = bar_today['close'] / bar_today['ma50'] - 1
        ema21_ma50_gap = bar_yesterday['ema21'] / bar_yesterday['ma50'] - 1
        ema21_ma50_gap_str = "{:.2f}".format(round(ema21_ma50_gap, 2))
        if ema21_ma50_gap>0.039:
            ema21_ma50_gap_str = '[[' + ema21_ma50_gap_str + ']]'
        # 
        channel_ema21 = bar_today['barlow_2_ema21_percent_oneyear_channel_percentile']
        lmt_price = price_info[ticker]['entry_price']*1.04
        lmt_price_str = "{:.2f}".format(lmt_price)
        rank = round(stock_ranking[ticker.upper()], 2)
        print(ticker,pct_fmt(channel_ema21),'||| rank=', rank,'||| quantity:(',cnt_str,'LMT:',lmt_price_str, ') algo_enter_ts:',ts_str,' enter price:',price_str, 'now_to_ma50:',pct_fmt(gap_ma50),'----ema21 ma50 gap:',ema21_ma50_gap_str)

# print opened
print('===========================opened (in current tradble)===========================')
print(len(opened_position), 'opened')
print_tradable(opened=True)

print('===========================new opportunity===========================')
print_tradable(opened=False)

    
# print('===========================update record===========================')    
# new_record = update_record_current_price(op_path_indicator)
# """
# until here we print out all opened position
# """


print('=======================Price Section=================================')  
ps = price_section(op_path_indicator)
"""
until here, we got conclusion status of all positions, what stock needs to be out (ma21 < ma50)
"""
def print_price_section(ps, section):
    print('-----------------------------'+section+'------------------------------------------')    
    cnt = 0
    for t, v in ps.items():
        if v['section'] == section:
            cnt = cnt + 1
            last_day = ''
            last_day_1 = ''
            if not v['today_ma_sequence']['hold']:
                last_day = v['today_ma_sequence']['date']+'-false'
            if not v['previous_day_ma_sequence']['hold']:
                last_day_1 = v['previous_day_ma_sequence']['date']+'-false'
            print(t,v['section'], '(',v['current_rate'],')',last_day, last_day_1)
    print('total in section:'+str(cnt))
    return cnt
    

a = print_price_section(ps, BELOW_ENTER)  
b = print_price_section(ps, ABOVE_STOP)  
c = print_price_section(ps, ABOVE_ENTER_NO_STOP)  
d = print_price_section(ps, BETWEEN_STOP_ENTER)          
 
assert len(opened_position)==(a+b+c+d)
