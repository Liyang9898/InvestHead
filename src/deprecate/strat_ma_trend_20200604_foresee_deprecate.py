'''
Created on Jun 4, 2020

@author: leon
'''
# Strategy Description:

# enter:
# 1.Price hitting closer MA (EMA 8 in my case)  -- of course you need to know the trend direction

# exit:
# 1.always exit on further MA (EMA 21 in my case)
# 2.after x bars or price already went over x%, exit when hitting entry price


class StrategySimpleMAFactory:
    def __init__(self):
        self.name='simple MA strategy'
    
    def genStrategySimpleMA(self,param_bundle):
        strat_instance=StrategySimpleMA(param_bundle)
        return strat_instance
        
class StrategySimpleMA:
    def __init__(self, param_bundle):
        self.name='simple MA strategy'
        self.strategy_params=param_bundle
        self.exit_duration_threshiold = param_bundle['exit_duration_threshiold']
        self.exit_profit_threshiold = param_bundle['exit_profit_threshiold'] # need to adjust based on time period, 4% is good for 1 day bar, 4%/24 for one hour bar
        self.neutual_exit_enable = True
        if param_bundle['neutual_exit_enable'] == 0:
            self.neutual_exit_enable = False
        
    def getStrategyParams(self):
        return self.strategy_params
    
    def gen_entry(self, bar, bar_yesterday):
        # determine entry price    
        bardirection = 1 if bar['open']<bar['close'] else -1
        
        
        if bar['cover_lh_8'] == 1 and (bar_yesterday['sequence_8_21'] == 'short_sequence' or bar_yesterday['sequence_8_21'] == 'long_sequence'):
#         if bar['cover_lh_8'] == 1:
            direction = 1
            if bar_yesterday['sequence_8_21'] == 'short_sequence':
                direction = -1
#             print(bar['est_datetime']+"  "+bar['sequence_8_21']+"  direction="+str(direction))
            return bar['ema8']*direction
        else:
            return 0
        
    
    def gen_exit(
            self, 
            bar, 
            direction, 
            entry_price, 
            entry_bar_id, 
            current_bar_id, 
            best_price_in_market
        ):
        # check MA exit fisrt, if exit is worse than entry price, then check if exit on entry price is possible
        bar_duration = current_bar_id-entry_bar_id
        max_history_potential_profit = abs(best_price_in_market - entry_price) / entry_price
        exit_on_entry_price_permission = False
        
        if self.neutual_exit_enable:
            if bar_duration>self.exit_duration_threshiold or max_history_potential_profit > self.exit_profit_threshiold:
                exit_on_entry_price_permission = True
            
#         print(bar['est_datetime']+"  "+str(bar['cover_lh_21'])+"  direction="+str(direction)+" bar duration="+str(bar_duration)+" max_history_potential_profit="+str(max_history_potential_profit))  
           
        # determine exit price    
        exit_action = 0
        
        # penetrate MA
        if (direction==1 and bar['ema21'] > bar['low']) or (direction==-1 and bar['ema21'] < bar['high']): # must close position
            exit_action = bar['ema21'] * direction * (-1)
            # see if there is opportunity to exit on entry price, if it's better than MA price
            if (direction==1 and bar['ema21'] < entry_price) or (direction==-1 and bar['ema21'] > entry_price): 
                if exit_on_entry_price_permission: 
                    # improve exit price
                    exit_action = entry_price * -1 * direction
        
        # penetrate entry price but not MA
        if exit_on_entry_price_permission:
            if (direction==1 and bar['ema21'] < bar['low'] and bar['low'] <= entry_price) or (direction==-1 and bar['ema21'] > bar['high'] and bar['high']>= entry_price): 
                exit_action = entry_price * -1 * direction
            
        return exit_action
    
    
def gen_strategy_bundles(exit_duration_threshiold_set, exit_profit_threshiold_set):
    res = []
    for exit_duration_threshiold in exit_duration_threshiold_set:
        for exit_profit_threshiold in exit_profit_threshiold_set:
            param = {
                "exit_duration_threshiold": exit_duration_threshiold,
                "exit_profit_threshiold": exit_profit_threshiold
            }
            res.append(param)
    return res