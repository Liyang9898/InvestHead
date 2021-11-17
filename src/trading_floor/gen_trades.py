'''
Created on Jun 4, 2020

@author: leon
'''

from trading_floor.TradeInterface import Trade, TradeBundle
from trading_floor.trading_util import unfinished_bar_best_price
from trading_floor.EntryPointGenerator import gen_entry
from trading_floor.ExitPointGenerator import gen_exit_given_entry


def gen_trades(df, strategy, all_bar_entry=False):
    # df start idx from 0
    df.reset_index(drop=True, inplace=True)

    trades = TradeBundle()
    trades.setStrategyParams(strategy.getStrategyParams())
    trades.setBarCount(len(df))
    
    # we start trading on bar 1, although bar idx start from 0
    bar_cnt = 1
    while bar_cnt < len(df.index):
        # check if current bar is a valid entry  
        entry_info = gen_entry(df, bar_cnt, strategy)
        
        if entry_info['valid_entry']: # open position
            
            new_trade = gen_exit_given_entry(df, strategy, entry_info) # close position
            
            # add finished trade to trade bundle
            if new_trade.complete is True:
                trades.addTrade(new_trade)
            else: 
                # close unfinished trade
                trades.addTrade(new_trade)
        
            if not all_bar_entry:
                # bar_duration=exit_bar_idx-entry_bar_id,
                closing_bar_idx = new_trade.bar_duration + entry_info['entry_bar_id']
                # move pointer to the exit bar of last trade
                bar_cnt = closing_bar_idx
        
        bar_cnt = bar_cnt + 1
    
    
  
    # a necessary post process of tradeBundle
    trades.genTradesSummary()
    return trades


def gen_entries(df, strategy):
    # df start idx from 0
    df.reset_index(drop=True, inplace=True)

    trades = TradeBundle()
    trades.setStrategyParams(strategy.getStrategyParams())
    trades.setBarCount(len(df))
    
    # we start trading on bar 1, although bar idx start from 0
    bar_cnt = 1
    entries = []
    while bar_cnt < len(df.index):
        # check if current bar is a valid entry  
        entry_info = gen_entry(df, bar_cnt, strategy)
        
        if entry_info['valid_entry']: # open position
            entries.append(entry_info)

        bar_cnt = bar_cnt + 1
    
    return entries


