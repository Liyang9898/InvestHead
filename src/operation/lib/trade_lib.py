'''
Created on Mar 11, 2021

@author: leon
'''

import pandas as pd

from trading_floor.EntryPointGenerator import gen_entry
from strategy_lib.strat_ma_swing import StrategySimpleMA
from batch_20201214.util_for_batch.batch_util import get_all_files
# from version_master.version import op_path_indicator
from version_master.version import op_path_base
from datetime import datetime
from version_master.version import op_path_base, op_record

BELOW_ENTER='BELOW_ENTER'
ABOVE_STOP='ABOVE_STOP'
BETWEEN_STOP_ENTER='BETWEEN STOP-ENTER'
ABOVE_ENTER_NO_STOP='ABOVE_ENTER_NO_STOP'

now = datetime.today()
now_str = now.strftime('%Y-%m-%d')

path_base = op_path_base + now_str
op_path_indicator = path_base + '/indicator/'



def tradable(df, strategy_param_bundle, offset):
#     print(df)
    bar_cnt = len(df)
    pos = bar_cnt - 1 - offset
    date = df.loc[pos, 'date']
#     print(date)
    strategy=StrategySimpleMA(strategy_param_bundle)
 
    entry_info = gen_entry(df, pos, strategy)
    return entry_info
    
    
def batch_tradable(
    indicator_path, 
    strategy_param_bundle,
    offset,
):
    res = {}
    files = get_all_files(indicator_path)
#     print(files)
    cnt = 1
    for ticker, file in files.items():

        if not file.endswith(".csv"):
            continue

#         print(cnt,' scanning ' ,ticker)
        path = indicator_path + ticker + '_downloaded_raw.csv'
        df = pd.read_csv(path)
#         print(df)
        entry_info = tradable(df, strategy_param_bundle, offset)

        if entry_info['valid_entry']:
            bar_today = df.iloc[len(df)-1,:]
            bar_yesterday = df.iloc[len(df)-2,:]
            res[ticker.lower()] = {
                'entry_info':entry_info,
                'bar_today':bar_today,
                'bar_yesterday':bar_yesterday
            }
            
#             plot_indicator(df, 'sequence_8_21_50',ticker)
            
        cnt=cnt+1
    return res
        
        
def process_trade_channel_position(trade):
    x = trade['bar_today']['close']
    
    f=trade['bar_yesterday']['barlow_2_ema8_channel_floor']
    p25 = trade['bar_yesterday']['barlow_2_ema8_channel_mp25_pos']
    p50 = trade['bar_yesterday']['barlow_2_ema8_channel_mp50_pos']
    p75 = trade['bar_yesterday']['barlow_2_ema8_channel_mp75_pos']
    c = trade['bar_yesterday']['barlow_2_ema8_channel_ceiling']
#     print(f,p25,p50,p75,c,'---',close)
    if x > c:
        return 120
    elif x > p75:
        return 75
    elif x > p50:
        return 50
    elif x > p25:
        return 25
    elif x > f:
        return 0    
    else:
        return -1
    
#     
# def process_trade_channel_position_ema21(trade):
#     x = trade['bar_today']['close']
#     
#     p0 = trade['bar_yesterday']['barlow_2_ema21_percent_oneyear_channel_0']
#     p25 = trade['bar_yesterday']['barlow_2_ema21_percent_oneyear_channel_25']
#     p50 = trade['bar_yesterday']['barlow_2_ema21_percent_oneyear_channel_50']
#     p75 = trade['bar_yesterday']['barlow_2_ema21_percent_oneyear_channel_75']
#     p100 = trade['bar_yesterday']['barlow_2_ema21_percent_oneyear_channel_100']
#     
#     pp0 = trade['bar_today']['ema21'] * (1+p0)
#     pp25 = trade['bar_today']['ema21'] * (1+p25)
#     pp50 = trade['bar_today']['ema21'] * (1+p50)
#     pp75 = trade['bar_today']['ema21'] * (1+p75)
#     pp100 = trade['bar_today']['ema21'] * (1+p100)
#     
# #     print(f,p25,p50,p75,c,'---',close)
#     if x > pp100:
#         return 120
#     elif x > pp75:
#         return 75
#     elif x > pp50:
#         return 50
#     elif x > pp25:
#         return 25
#     elif x > pp0:
#         return 0    
#     else:
#         return -1
    
    
def get_opened_position():
    path = op_record
    df = pd.read_csv(path)
    df_open_position = df[(df['status'] != 'win') & (df['status'] != 'win')]
    open_position = df_open_position['ticker'].to_list()
    res = []
    for ticker in open_position:
        print(ticker)
        res.append(ticker.lower())
    return res


def update_record_current_price(indicator_path):
    # retrieve all price
    path_files = get_all_files(indicator_path)
    latest_price = {}
    for ticker, file in path_files.items():
        if not file.endswith(".csv"):
            continue
 
        price_path = indicator_path + ticker + '_downloaded_raw.csv'
        ticker_df = pd.read_csv(price_path)
        end_bar_idx = len(ticker_df) - 1
        latest_price[ticker.lower()] = ticker_df.loc[end_bar_idx, 'close']
        

    record_path = op_record
    record_df = pd.read_csv(record_path)

    for i in range(0, len(record_df)):

        ticker = record_df.loc[i, 'ticker'].lower()
        if ticker not in latest_price.keys():
            print(ticker, 'does not exist')
            continue
        record_df.loc[i, 'current_price'] = latest_price[ticker]
        delta = record_df.loc[i, 'current_price']/record_df.loc[i, 'enter_price']-1
        delta_str = "{0:.2%}".format(delta)
        record_df.loc[i, 'current_rate'] = delta_str
    record_df.to_csv(record_path, index=False)
    print('portfolio record updated')


def price_section(path_indicator):
    # this method go over all opened position
    
    # part 1
    # check yesterday's MA
    # to see if ema21 is under ma50

    # part 2
    # current price can be categorized into 3 sections:
    # 1. BELOW_ENTER.  
    # 2. ABOVE_STOP   
    # 3. BETWEEN STOP-ENTER  ---SELL
    # 4. ABOVE_ENTER_NO_STOP
    
    res = {}
    record_path = op_record
    record_df = pd.read_csv(record_path)
    for i in range(0, len(record_df)):
        ticker = record_df.loc[i, 'ticker'].lower()
        current_rate = record_df.loc[i,'current_rate']
        status = record_df.loc[i, 'status']
        if status in ['win', 'lose', 'neutral']:
            # skip closed position
            continue
        enter_price = record_df.loc[i, 'enter_price']
        a_stop_price = record_df.loc[i, 'a_stop_price']
        limit_sell_price = record_df.loc[i, 'limit_order']
        
        # get indicator file
        price_path = path_indicator + ticker + '_downloaded_raw.csv'
        try:
            ticker_df = pd.read_csv(price_path)
        except:
            print(ticker, 'has no stock data')
            continue
        last_i = len(ticker_df) - 1
        current_price = ticker_df.loc[last_i, 'close']

        # section        
        section = ''
        if current_price <= enter_price:
            section = BELOW_ENTER
#         elif a_stop_price == 0:
#             section = ABOVE_ENTER_NO_STOP
#         elif a_stop_price > 0 and current_price >= a_stop_price:
#             section = ABOVE_STOP
#         elif a_stop_price > 0 and current_price < a_stop_price:
#             section = BETWEEN_STOP_ENTER
        elif current_price < limit_sell_price:
            section = BETWEEN_STOP_ENTER
        elif current_price >= limit_sell_price:
            section = ABOVE_STOP
            
        # MA
        last_i = len(ticker_df) - 1
        
        # last day
        today_ma_positive = True
        today_check_date = ticker_df.loc[last_i, 'date']
        if ticker_df.loc[last_i, 'ema21'] < ticker_df.loc[last_i, 'ma50']:
            today_ma_positive = False
        
        # last day -1
        previous_day_ma_positive = True
        idx = last_i - 1
        previous_check_date = ticker_df.loc[idx, 'date']
        if ticker_df.loc[idx, 'ema21'] < ticker_df.loc[idx, 'ma50']:
            previous_day_ma_positive = False

        
        row = {
            'ticker': ticker,
            'section': section,
            'current_rate': current_rate,
            'today_ma_sequence': {
                'date':today_check_date, 
                'hold':today_ma_positive, 
                'ema21':ticker_df.loc[last_i, 'ema21'] , 
                'ma50':ticker_df.loc[last_i, 'ma50']
            },
            'previous_day_ma_sequence': {
                'date':previous_check_date, 
                'hold':previous_day_ma_positive, 
                'ema21':ticker_df.loc[idx, 'ema21'], 
                'ma50':ticker_df.loc[idx, 'ma50']
            },
        }
        res[ticker] = row
    return res
        
