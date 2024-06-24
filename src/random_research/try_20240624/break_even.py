'''
Created on Jun 24, 2024

@author: spark
'''
import pandas as pd
from util.util_time import days_gap_date_str

path_df_trades='C:/f_data/trades_csv/SPY_1W_fmt_trades_all_consecutive_2.csv'
path_df_st='C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'

df_trades = pd.read_csv(path_df_trades)
df_st = pd.read_csv(path_df_st) 


def search_break_even_dt(entry_ts, exit_ts, df_st, start_position, end_position):
    df_st_usable = df_st[(df_st['est_datetime'] >= entry_ts) & (df_st['est_datetime'] <= exit_ts)].copy()
    df_st_usable.reset_index(drop=True,inplace=True)
    start_price = df_st_usable.loc[0, 'close']
    
    for i in range(0, len(df_st_usable)):
        price = df_st_usable.loc[i, 'close']
        dt = df_st_usable.loc[i, 'est_datetime']
        if (price/start_price>end_position/start_position): # break even
            return dt
            # print('end')
            break
    return '?'


def gen_break_even_strategy(lose_trade, df_st, df_trades):
    res_trades = []
    
    start_date = lose_trade['exit_ts']
    pnl_percent_lose = float(lose_trade['pnl_percent'])
    required_gain = 1.0 / (1.0 + pnl_percent_lose) - 1.0 # we need this much gain to break even
    
    df_trades_usable = df_trades[df_trades['entry_ts'] >= start_date].copy()
    df_trades_usable.reset_index(drop=True,inplace=True)
    
    cur = 1
    cur = cur * (1 + pnl_percent_lose)
    for i in range(0, len(df_trades_usable)):
        entry_ts = df_trades_usable.loc[i, 'entry_ts']
        exit_ts = df_trades_usable.loc[i, 'exit_ts']
        pnl_percent = df_trades_usable.loc[i, 'pnl_percent']
        str_trade = entry_ts[0:10] + '_' + exit_ts[0:10] + '_' + str(pnl_percent)
         
        next = cur * (1 + pnl_percent)
        res_trades.append(str_trade)
        
        # check if current trade can break even
        if (next > 1): # even and exceed
            dt_even = search_break_even_dt(entry_ts, exit_ts, df_st, cur, next)
            df_trades_to_even = df_trades_usable[df_trades_usable['entry_ts'] <= entry_ts].copy()
            df_trades_to_even.reset_index(drop=True,inplace=True)
            gap = days_gap_date_str(start_date[0:10], dt_even[0:10])
            res = {
                # 'start_date':start_date[0:10],
                'even_date':dt_even[0:10],
                'days_to_even':gap,
                # 'lose_trade':lose_trade,
                'trades_to_even_start_dt':res_trades,
                # 'trades_to_even':df_trades_to_even,
                
            }
            return res
            
            
        else: # not even yet
            cur = next
            
    res = {
        # 'start_date':start_date[0:10],
        'even_date':'never even',
        'days_to_even':'never even',
        # 'lose_trade':lose_trade,
        'trades_to_even_start_dt':res_trades,
        # 'trades_to_even':df_trades_to_even,
        
    }
    return res        



path_all_trades='C:/f_data/trades_csv/SPY_1W_fmt_trades_all_entry_2.csv'  
path_all_trades_even='C:/f_data/trades_csv/SPY_1W_fmt_trades_all_entry_2_with_even.csv'  
df_all_trades = pd.read_csv(path_all_trades)
all_trades = df_all_trades.to_dict('record')


for trades in all_trades:
    entry_ts = trades['entry_ts']
    exit_ts = trades['exit_ts']
    pnl_percent = float(trades['pnl_percent'])
    
    if (pnl_percent >=0): # filter out win trades
        continue
    
    
    breakeven = gen_break_even_strategy(trades, df_st, df_trades)
    print(trades, breakeven)
    trades['even_date'] = breakeven['even_date']
    trades['days_to_even'] = breakeven['days_to_even']
    trades['trades_to_even_start_dt'] = breakeven['trades_to_even_start_dt']
    # print(trades, breakeven)

# print(all_trades)
df_all_trades_with_even = pd.DataFrame(all_trades)
# print(df_all_trades_with_even)
df_all_trades_with_even.to_csv(path_all_trades_even, index=False)
    
    
lose_trade={
    'entry_price':'', 
    'entry_ts':'', 
    'exit_price':'', 
    'exit_ts':'1998-09-07', 
    'direction':'',
    'bar_duration':'', 
    'pnl':'', 
    'pnl_percent':'-0.196736875789473', 
    'best_potential_pnl_percent':'',
    'complete':''
}

# res = gen_break_even_strategy(lose_trade, df_st, df_trades)
# print(res)


