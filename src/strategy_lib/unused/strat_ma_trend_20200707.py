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
        # determine entry price    
        bardirection = 1 if bar['open']<bar['close'] else -1

        #==============================================optional manual filter===================================
        #Warning! they are just estimate, they don't 100% does what you are doing in reality
#         if bar_yesterday['sequence_8_21_strict'] == 'na':
#             return 0
#    
# #         print(bar['est_datetime'],abs(bar_yesterday['ema21_delta']))
#         if abs(bar_yesterday['ema21_delta'])<=3:
#             return 0
#  
        # we discovered that 50% of the lose are between 0.2%-0.25% PNL
#         stop_loss_pnl = abs(bar_yesterday['ema21']-bar_yesterday['ema8'])/bar_yesterday['ema8']
#         if stop_loss_pnl < 0.0025:
#             return 0

        #Warning! they are just estimate, they don't 100% does what you are doing in reality
        #==============================================optional manual filter===================================
        
        price_cross_ma8 = False
        if bar['ema8_1day_projectile'] < bar['high'] and bar['ema8_1day_projectile'] > bar['low']:
            price_cross_ma8 = True
        
        if price_cross_ma8 and (bar_yesterday['sequence_8_21'] == 'short_sequence' or bar_yesterday['sequence_8_21'] == 'long_sequence'):
#         if bar['cover_lh_8'] == 1:
            direction = 1
            if bar_yesterday['sequence_8_21'] == 'short_sequence':
                direction = -1
#             print(bar['est_datetime']+"  "+bar['sequence_8_21']+"  direction="+str(direction))
            return bar['ema8_1day_projectile']*direction
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
        
        # get stop profit price        
        stop_profit_price = entry_price * (1 + self.stop_profit_percent * direction) # <----stop profit price

        # get top loss price
        stop_loss_price = bar_yesterday['ema21'] # <----stop profit price
        
        ## neutual out condition
        if self.neutual_exit_enable:
            ## condition 1: how many bar since entry
            bar_duration = bar_idx - entry_bar_id
            ## condition 2: best price since entry
            max_profit = abs(best_price_in_market - entry_price) / entry_price
            if bar_duration > self.exit_duration_threshiold or max_profit > self.exit_profit_threshiold: # enable neutral out
                # need to check if neutral price is better then stop loss price
                if (direction == 1 and entry_price > stop_loss_price) or (direction == -1  and entry_price < stop_loss_price):
                    stop_loss_price = entry_price
        
        # judge if stop loss or stop profit
        stopprofit_touch = False
        stoploss_touch = False
        
        # need to cover jump case
        if (bar['low'] <= stop_profit_price and stop_profit_price <= bar['high']) or (direction == 1 and bar['low']>stop_profit_price) or (direction == -1 and bar['low']<stop_profit_price):  
            stopprofit_touch = True
            
        if (bar['low'] <= stop_loss_price and stop_loss_price <= bar['high']) or (direction == 1 and bar['high']<stop_loss_price) or (direction == -1 and bar['low']>stop_loss_price):
            stoploss_touch = True
        
        exit_action = 0
        if not stopprofit_touch and not stoploss_touch:
            exit_action = 0
        elif stopprofit_touch and not stoploss_touch:
            exit_action = stop_profit_price * -1 * direction
        elif not stopprofit_touch and stoploss_touch:
            exit_action = stop_loss_price * -1 * direction
        else: # both touch
            # it takes effort to tell whether stop profit or stop loss happens in same bar first. We do stop loss first to get floor performance
            # TODO: stop profit or stop loss first
            exit_action = stop_loss_price * -1 * direction # let's be worst case for now
            
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