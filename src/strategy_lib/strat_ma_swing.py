from strategy_lib.strat_ma_base import gen_strategy_bundle, StrategySimpleMABase


class StrategySimpleMAFactory:
    def __init__(self):
        self.name='simple MA strategy'
    
    def genStrategySimpleMA(self,param_bundle):
        strat_instance=StrategySimpleMA(param_bundle)
        return strat_instance
        
class StrategySimpleMA:
    def __init__(self, param_bundle):
        self.instance = StrategySimpleMABase(param_bundle)


    def getStrategyParams(self):
        return self.instance.getStrategyParams()
    

    # computing if we should perform an action on channel information
    def channel_green_light(self, percentile_bar, price_when_checking, is_enter):
        return self.instance.channel_green_light(percentile_bar, price_when_checking, is_enter)

            
    def gen_entry(self, df, bar_idx):
        return self.instance.gen_entry(df, bar_idx)

        
    def gen_exit(
            self, 
            df, 
            bar_idx, 
            direction, 
            entry_price, 
            entry_bar_id, 
            current_bar_id, 
            best_price_in_market,
            price_peak_since_entry,
            bars_totally_above_entry,
            valid_entry
        ):
        return self.instance.gen_exit(df, bar_idx, direction, entry_price, entry_bar_id, current_bar_id, best_price_in_market, price_peak_since_entry,bars_totally_above_entry,valid_entry)

def gen_strategy_bundles(exit_duration_threshiold_set, exit_profit_threshiold_set):
    res = gen_strategy_bundle(exit_duration_threshiold_set, exit_profit_threshiold_set)
    return res