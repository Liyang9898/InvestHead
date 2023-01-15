'''
Created on Jan 15, 2023

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
        
                
def gen_op_combo_filter(combo_df, max_lose_win_rate, max_required_win_rate, min_pnl_spread_margin):
    combo_df = combo_df[combo_df['lose_win_rate'] < max_lose_win_rate]
    combo_df = combo_df[combo_df['required_win_rate'] < max_required_win_rate]
    return combo_df
