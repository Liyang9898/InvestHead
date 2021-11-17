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
        if bar_yesterday['sequence_8_21_50'] == 'long_sequence':
            direction = 1
            return bar['open'] * direction
        elif bar_yesterday['sequence_8_21_50'] == 'short_sequence':
            direction = -1
            return bar['open'] * direction
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
        
        if direction == 1:
            if bar_yesterday['sequence_8_21_50'] != 'long_sequence':
                # exit
                exit_action = direction * (-1) * bar['open']
        elif direction == -1:
            if bar_yesterday['sequence_8_21_50'] != 'short_sequence':
                # exit
                exit_action = direction * (-1) * bar['open']
                
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