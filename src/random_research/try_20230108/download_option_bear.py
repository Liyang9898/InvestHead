'''
Created on Jan 8, 2023

@author: spark
'''
import pandas as pd
from random_research.try_20230108.lib import get_option_dataframe, \
    gen_op_combo_filter
import yfinance as yf


def gen_spread_combo(op_df, strike_price_max, strike_price_min):
    op_df_filtered = op_df[(op_df['strike'] >= strike_price_min) & (op_df['strike'] <= strike_price_max)]
    op_df_filtered.reset_index(inplace=True, drop=True)
    print(op_df_filtered)
    combo_list = []
    
    for i in range(0, len(op_df_filtered)):
        strike_low = op_df_filtered.loc[i, 'strike'] ## your sell call
        bid_low = op_df_filtered.loc[i, 'bid'] # your trade in buy call
        ask_low = op_df_filtered.loc[i, 'ask'] 
        # print(strike_price, bid, ask)
        
        for j in range(i+1, len(op_df_filtered)):
            strike_high = op_df_filtered.loc[j, 'strike'] ## your buy call
            bid_high = op_df_filtered.loc[j, 'bid'] 
            ask_high = op_df_filtered.loc[j, 'ask'] # your trade in sell call
            
            # process combination
            strike_diff = abs(strike_high - strike_low)
            gain = round(bid_low - ask_high, 2)
            print(gain)
            if gain <= 0:
                continue

            lose = round(strike_diff - gain, 2)
            remain_profit = round(1-ask_high/bid_low, 2)
            lose_win_rate = round(lose / gain, 2)
            required_win_rate = round(lose_win_rate / (1+lose_win_rate), 4)
            pnl_spread_margin = round(gain / strike_diff, 6)
            pnl_underlying = round(gain / strike_low, 6)
            
            pnl_spread_margin_52x = pnl_spread_margin * 52

            combo = {
                'sell call': strike_low,
                'buy call': strike_high,
                'sell call prem': bid_low,
                'buy call prem': ask_high,
                'spread margin $': strike_diff * 100,
                'underlying $': strike_low * 100,
                'gain':gain,
                'lose':lose,
                'remain profit': remain_profit,
                'lose_win_rate': lose_win_rate,
                'required_win_rate': required_win_rate,
                'pnl_spread_margin': pnl_spread_margin,
                'pnl_underlying': pnl_underlying,
                'pnl_spread_margin_52x': pnl_spread_margin_52x
                
            }
            combo_list.append(combo)
    combo_df = pd.DataFrame(combo_list)
    return combo_df


ticker = 'SPY'
strike_price_max = 420.0
strike_price_min = 400.0

expiration = '2023-01-20'
op_type = 'call'
max_lose_win_rate = 10
min_required_win_rate = 1
min_pnl_spread_margin = 0

path = 'C:/f_data/random/option_date_test.csv'


op_df = get_option_dataframe(ticker, expiration, op_type)
print(op_df)
combo_df= gen_spread_combo(op_df, strike_price_max, strike_price_min)
print(combo_df)
combo_df_filtered = gen_op_combo_filter(combo_df, max_lose_win_rate, min_required_win_rate, min_pnl_spread_margin)

combo_df_filtered.to_csv(path, index=False)
print(combo_df_filtered)