'''
Created on Jan 8, 2023

@author: spark
'''
import yfinance as yf
import pandas as pd


def get_option_dataframe(ticker, expiration, op_type):
    ticker_data = yf.Ticker(ticker)
    opt = ticker_data.option_chain(expiration)
    calls = opt.calls
    puts = opt.puts
    if op_type == 'call':
        calls.sort_values(by='strike', ascending=True, inplace=True)
        calls.reset_index(inplace=True, drop=True)
        return calls
    elif op_type == 'put':
        puts.sort_values(by='strike', ascending=True, inplace=True)
        puts.reset_index(inplace=True, drop=True)
        return puts
    else:
        print('wrong option type')
        

def gen_spread_combo(op_df, strike_price_max, strike_price_min):
    op_df_filtered = op_df[(op_df['strike'] >= strike_price_min) & (op_df['strike'] <= strike_price_max)]
    op_df_filtered.reset_index(inplace=True, drop=True)
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
            

def gen_op_combo_filter(combo_df, max_lose_win_rate, max_required_win_rate, min_pnl_spread_margin):
    combo_df = combo_df[combo_df['lose_win_rate'] < max_lose_win_rate]
    combo_df = combo_df[combo_df['required_win_rate'] < max_required_win_rate]
    return combo_df


ticker = 'SPY'
expiration = '2023-01-13'
op_type = 'call'
strike_price_max = 420.0
strike_price_min = 400.0

max_lose_win_rate = 10
min_required_win_rate = 1
min_pnl_spread_margin = 0

path = 'C:/f_data/random/option_date_test.csv'


op_df = get_option_dataframe(ticker, expiration, op_type)
combo_df= gen_spread_combo(op_df, strike_price_max, strike_price_min)
combo_df_filtered = gen_op_combo_filter(combo_df, max_lose_win_rate, min_required_win_rate, min_pnl_spread_margin)

combo_df_filtered.to_csv(path, index=False)