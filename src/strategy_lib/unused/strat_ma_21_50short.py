'''
Created on Jul 10, 2020

@author: leon
'''
'''
Created on Jun 4, 2020

@author: leon
'''
# Strategy Description:

# enter:
# todo

# exit:
# todo


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
        self.stop_profit_percent = param_bundle['stop_profit_percent']
        if param_bundle['neutual_exit_enable'] == 0:
            self.neutual_exit_enable = False
            
        self.stop_profit_enable = True
        if param_bundle['stop_profit_enable'] == 0:
            self.stop_profit_enable = False
        
    def getStrategyParams(self):
        return self.strategy_params
    
    def gen_entry(self, df, bar_idx):
        bar = df.iloc[bar_idx,:]
        bar_yesterday = df.iloc[(bar_idx-1),:]
        
#         if bar_yesterday['sequence_8_21_50'] == 'long_sequence':
#             direction = 1
#             return bar['open'] * direction
 
#         if bar_yesterday['low'] > bar_yesterday['ma50']:
#         if bar_yesterday['ema21'] > bar_yesterday['ma50'] and bar_yesterday['ema21_delta'] > 0:
#         if bar_yesterday['ema21'] > bar_yesterday['ma50'] and bar_yesterday['ema21_delta'] > 0 and bar_yesterday['ma50_delta'] > 0 and bar_yesterday['ema21_ma50_MACD']>0:
        if bar_yesterday['ema21'] < bar_yesterday['ma50'] and bar_yesterday['ma50_delta'] < 0 and bar_yesterday['ema21_delta'] < 0 and bar_yesterday['ema21_ma50_MACD']>0:
#         if bar_yesterday['ema21'] > bar_yesterday['ma50']:
            direction = -1
            return bar['open'] * direction
#         # long only on spy 500
#         elif bar_yesterday['sequence_8_21_50'] == 'short_sequence':
#             direction = -1
#             return bar['open'] * direction

#         if bar_yesterday['close'] > bar_yesterday['ma50']:
#             direction = 1
#             return bar['open'] * direction

        else:
            return 0
        
    def gen_exit(
            self, 
            df, 
            bar_idx, 
            direction, 
            entry_price, 
            entry_bar_id, 
            current_bar_id, 
            best_price_in_market
        ):
        bar = df.iloc[bar_idx,:]
        bar_yesterday = df.iloc[(bar_idx-1),:]
        exit_action = 0
        
        ################### take profit ###################################
#         best_profit_p = best_price_in_market / entry_price - 1
#         current_profit_high = bar['high'] / entry_price - 1
#         current_profit_low = bar['low'] / entry_price - 1
#                  
#         profit_arron = 0.08
#         profit_inflation = 0.04
#         profit_fixed_interest = 0.02
#         breaching_profit_threshold = False
#                  
#         take_profit= 0 # questionable?
#         if best_profit_p > profit_arron * 2:
#             take_profit = profit_arron
#             breaching_profit_threshold = True
#         elif best_profit_p > profit_inflation * 2:
#             take_profit = profit_inflation
#             breaching_profit_threshold = True
#         elif best_profit_p > profit_fixed_interest * 2:
#             take_profit = profit_fixed_interest
#             breaching_profit_threshold = True
#              
#         if breaching_profit_threshold:
#             if current_profit_low < take_profit:
#                 # take_profit = exit_price / entry_price - 1
#                 take_profit_price = (take_profit + 1) * entry_price
#                 return -take_profit_price
        ################### take profit ###################################
        
        if self.neutual_exit_enable:
            #neutral out validation
            bar_duration = bar_idx - entry_bar_id
#             offset = 0.002
            offset = 0
            neutral_out_price = entry_price * (1+offset)
            if bar_duration > self.exit_duration_threshiold:
                # check neutral out
                if bar['low'] < neutral_out_price and neutral_out_price < bar['high']:
#                     if bar['ma50'] < entry_price:
                        return -neutral_out_price 
        
#         stop_loss = bar['ma50']
#         if bar_idx-entry_bar_id>4 and entry_price>bar['ma50']:
#             stop_loss=entry_price
#         
        if direction == -1:
#             if bar['low']<stop_loss:
#                 exit_action = direction * (-1) * stop_loss
        # we long spy 500 only
#             if bar_yesterday['sequence_8_21_50'] != 'long_sequence':
#                 exit_action = direction * (-1) * bar['low']
#                 
            if bar_yesterday['ema21'] >= bar_yesterday['ma50']:
                direction = 1
                return bar_yesterday['close'] * direction
                
#             if bar['low'] <= bar['ma50']:
#                 direction = 1
#                 return bar['ma50'] * direction    
                
                
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