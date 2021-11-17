'''
Created on Jun 28, 2020

@author: leon
'''


from trading_floor.TradeInterface import Trade
from trading_floor.EntryPointGenerator import gen_entry

def gen_exit_given_entry(df, strategy, entry_info):

    # parse entry info
    entry_price = entry_info['entry_price']
    entry_ts = entry_info['entry_ts']
    position_direction = entry_info['position_direction']
    entry_bar_id = entry_info['entry_bar_id']
    best_price = entry_info['best_price']
#     profit_management = 

    idx_s = entry_bar_id + 1
    idx_e = len(df.index)
    max_potential_profit = 0
    price_peak_since_entry = 0
    bars_totally_above_entry = 0
    # scan all bars
    for bar_idx in range(idx_s, idx_e, 1):
        bar = df.iloc[bar_idx,:] # check if exit on this bar
        bar_yeaterday = df.iloc[(bar_idx-1),:]
        max_potential_profit = abs(best_price - entry_price) / entry_price
        
        # how many continues bar are above entry price?
        if bar_yeaterday['low'] > entry_price:
            bars_totally_above_entry = bars_totally_above_entry + 1
        else:
            bars_totally_above_entry = 0
        
        # peak price since entry
        if price_peak_since_entry < bar_yeaterday['high']:
            price_peak_since_entry = bar_yeaterday['high']
        
        # is this exit enterable?
        valid_entry = False
        if bar_idx+1 <= idx_e-1:
            entry_info = gen_entry(df, bar_idx+1, strategy)
            valid_entry = entry_info['valid_entry']
        ############################ exit strategy logic start ###########################################
        exit_action = strategy.gen_exit(
            df=df, 
            bar_idx=bar_idx,
            direction=position_direction,
            entry_price=entry_price, 
            entry_bar_id=entry_bar_id, 
            current_bar_id=bar_idx, 
            best_price_in_market=best_price,
            price_peak_since_entry=price_peak_since_entry,
            bars_totally_above_entry=bars_totally_above_entry,
            valid_entry=valid_entry
        )
        ############################ exit strategy logic end #############################################
        
        if exit_action != 0: # close position

            exit_price = abs(exit_action)
            exit_ts = bar['est_datetime']
            # add trading action
            new_trade = Trade(
                entry_price=entry_price, 
                entry_ts=entry_ts, 
                exit_price=exit_price, 
                exit_ts=exit_ts, 
                direction=position_direction, 
                bar_duration=bar_idx-entry_bar_id,
                best_potential_pnl_percent=max_potential_profit
            )
            
            # ==================================for ML analysis purpose======================================
            bar_before_entry_bar = df.iloc[(entry_bar_id-1),:]
            new_trade.gen_trade_ml_sample(
                ema_8_v_yesterday=abs(bar_before_entry_bar['ema8_delta']),
                ema_21_v_yesterday=abs(bar_before_entry_bar['ema21_delta']),
                ema_8_21_gap_yesterday=abs(bar_before_entry_bar['ema8_delta']-bar_before_entry_bar['ema21_delta']),
                ema_8_strict_sequence_yesterday=1 if bar_before_entry_bar['sequence_8_21_strict'] != 'na' else 0,
                pnl_p_per_trade=(exit_price-entry_price)/entry_price*position_direction,
                entry_time=entry_ts.split(' ')[1]
            )
            # ==================================for ML analysis purpose======================================
            return new_trade
                    

        best_price = max(bar['high'], best_price) if position_direction==1 else min(bar['low'], best_price)

    last_bar = df.iloc[idx_e - 1,:]
    unfinished_trade = Trade(
        entry_price=entry_price, 
        entry_ts=entry_ts, 
        exit_price=last_bar['close'], 
        exit_ts=last_bar['est_datetime'], 
        direction=position_direction, 
        bar_duration=idx_e-entry_bar_id,
        best_potential_pnl_percent=max_potential_profit,
        complete=False
    )    
    return unfinished_trade
