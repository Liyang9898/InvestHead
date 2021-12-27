'''
Created on Jul 20, 2020

@author: leon
'''

from strategy_lib.exit_lib.exit_strategy_legacy import gen_exit_legacy
from strategy_lib.exit_lib.exit_strategy_ma_macd import gen_exit_ma_macd
from strategy_lib.exit_lib.exit_strategy_ma_max_drawdown_cut import gen_exit_ma_max_drawdown_cut
from strategy_lib.exit_lib.exit_strategy_ma_only import gen_exit_ma_only
from strategy_lib.strategy_constant import EXIT_STRATEGY_LEGACY, \
    EXIT_STRATEGY_MA_ONLY, EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT, \
    EXIT_STRATEGY_MA_MACD, EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT_NEUTRAL_OUT
from strategy_lib.strategy_util.signal import channel_green_light, trend_start, \
    all_ma_upwards, macd, ma_enter_sequence, ribbon_expanding, \
    ema21_ma50_gap_percent
from strategy_lib.exit_lib.exit_strategy_ma_max_drawdown_cut_neutral_out import gen_exit_ma_max_drawdown_cut_neutral


class StrategySimpleMABase:
    def __init__(self, param_bundle):
        
        self.name='simple MA strategy'
        self.strategy_params=param_bundle
        self.exit_strategy = 'None'
        if 'exit_strategy' in param_bundle.keys():
            self.exit_strategy = param_bundle['exit_strategy']
        self.enter_ma_signal = param_bundle['enter_ma_signal']
        
        self.exit_duration_threshiold = param_bundle['exit_duration_threshiold']
        self.exit_profit_threshiold = param_bundle['exit_profit_threshiold'] # need to adjust based on time period, 4% is good for 1 day bar, 4%/24 for one hour bar
        self.neutual_exit_enable = True
#         self.stop_profit_percent = param_bundle['stop_profit_percent']
        if param_bundle['neutual_exit_enable'] == 0:
            self.neutual_exit_enable = False
            
        self.stop_profit_enable = True
        self.profit_management_enable_threshold = param_bundle['profit_management_enable_threshold'] 
        if param_bundle['profit_management_enable'] == 0:
            self.stop_profit_enable = False
            
        # take profit above x%
        self.take_profit_above_x = False
        self.take_profit_above_x_threshold = 0
        if 'take_profit_above_x' in param_bundle.keys() and param_bundle['take_profit_above_x'] == 1:
            self.take_profit_above_x = True
            self.take_profit_above_x_threshold = param_bundle['take_profit_above_x_threshold']
            
        # channel options
        self.enable_channel_enter = param_bundle["enable_channel_enter"]
        self.enable_channel_exit = param_bundle["enable_channel_exit"]
        self.optional_channel_enter_condition = True
        self.optional_channel_exit_condition = True
        
        # ribbon
        self.enable_ribbon_expand_start_enter = 0
        if 'enable_ribbon_expand_start_enter' in param_bundle.keys() and param_bundle['enable_ribbon_expand_start_enter'] == 1:
            self.enable_ribbon_expand_start_enter = 1
            
        # exit MA signal
        self.exit_ma_signal = 'none'
        if 'exit_ma_signal' in param_bundle.keys():
            self.exit_ma_signal = param_bundle['exit_ma_signal']        
            
        # trend start
        self.enter_on_trend_start = 0
        if 'enter_on_trend_start' in param_bundle.keys():
            self.enter_on_trend_start = param_bundle['enter_on_trend_start']     
        self.optional_enter_on_trend_start_condition = True
        
        # ema21 ma50 gap
        self.ema21_ma50_gap_percent_threshold = -1
        if 'ema21_ma50_gap_percent_threshold' in param_bundle.keys():
            self.ema21_ma50_gap_percent_threshold = param_bundle['ema21_ma50_gap_percent_threshold']

        
    def getStrategyParams(self):
        return self.strategy_params
    
 
    def gen_entry(self, df, bar_idx):
        bar = df.iloc[bar_idx,:]
        bar_today = bar

        bar_yesterday = df.iloc[(bar_idx-1),:]
#         print(bar_yesterday)
        if self.enable_channel_enter == 1:
            self.optional_channel_enter_condition = channel_green_light(
                percentile_bar=bar_yesterday['barlow_2_ema8_channel_mp50_pos'], 
                price_when_checking=bar_today['open'], 
                is_enter=True
            )
            
        if self.enter_on_trend_start == 1:
            is_trend_start = trend_start(bar_yesterday)
            if is_trend_start:
                self.optional_enter_on_trend_start_condition = True
            else:
                self.optional_enter_on_trend_start_condition = False
                
                

        all_ma_upward = all_ma_upwards(self.enter_ma_signal,bar_yesterday)
        macd_green = macd(self.enter_ma_signal, bar_yesterday)
        ma_sequence = ma_enter_sequence(self.enter_ma_signal, bar_yesterday) 
#         info = {
#             'yesterday_date':bar_yesterday['date'],
#             'all_ma_upward':all_ma_upward,
#             'macd_green':macd_green,
#             'ma_sequence':ma_sequence,
#             'ema8_ema21_gap':bar_yesterday['ema21_ma50_gap'],
#             'ema8_ema21_gap_ma':bar_yesterday['ema21_ma50_gap_ma'],
#             
#         }
#         print(info)
# df['ema8_ema21_gap_ma'] = df['ema8_ema21_gap'].rolling(window=3).mean()
# df['ema8_ema21_MACD'] = df['ema8_ema21_gap'] - df['ema8_ema21_gap_ma']
        
        
        # ribbon expanding
        optional_ribbon_expanding = True
        if self.enable_ribbon_expand_start_enter:
            optional_ribbon_expanding = ribbon_expanding(bar_yesterday)
        
        # ema21_ma50_gap_percent
        optional_ema21_ma50_gap = ema21_ma50_gap_percent(
            bar_yesterday, 
            self.ema21_ma50_gap_percent_threshold
        )
        
        
        if ma_sequence and \
            macd_green and \
            all_ma_upward and \
            optional_ribbon_expanding and \
            self.optional_channel_enter_condition and \
            self.optional_enter_on_trend_start_condition and \
            optional_ema21_ma50_gap:
            
            direction = 1
            # you always enter on 9:30 when market open

            return bar_today['open'] * direction  

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
            best_price_in_market,# best price until last bar
            price_peak_since_entry,
            bars_totally_above_entry,
            valid_entry,
        ):
        if self.exit_strategy == EXIT_STRATEGY_LEGACY:
            res = gen_exit_legacy(
                df, 
                bar_idx, 
                direction, 
                entry_price, 
                entry_bar_id, 
                current_bar_id, 
                best_price_in_market,
                ###
                self.exit_ma_signal,
                self.enable_channel_exit,
                self.optional_channel_exit_condition,
                self.stop_profit_enable,
                self.profit_management_enable_threshold,
                self.neutual_exit_enable,
                self.exit_duration_threshiold,
                self.take_profit_above_x,
                self.take_profit_above_x_threshold  
            )
        
        elif self.exit_strategy == EXIT_STRATEGY_MA_ONLY:
            res = gen_exit_ma_only(
                df, 
                bar_idx, 
                direction, 
                self.exit_ma_signal,    
            )
        elif self.exit_strategy == EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT:
            res = gen_exit_ma_max_drawdown_cut(
                df, 
                bar_idx, 
                direction, 
                entry_bar_id, 
                price_peak_since_entry,
                self.exit_ma_signal,    
            )
        elif self.exit_strategy == EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT_NEUTRAL_OUT:
            res = gen_exit_ma_max_drawdown_cut_neutral(
                df, 
                bar_idx, 
                direction, 
                entry_bar_id, 
                entry_price,
                price_peak_since_entry,
                bars_totally_above_entry,
                valid_entry,
                self.exit_ma_signal,    
            )
        elif self.exit_strategy == EXIT_STRATEGY_MA_MACD:
            res = gen_exit_ma_macd(
                df, 
                bar_idx, 
                direction, 
                entry_bar_id, 
                price_peak_since_entry,
                self.exit_ma_signal,    
            )
        else:
#             raise Exception("Exit strategy not found")
            # default using original exit
            res = gen_exit_legacy(
                df, 
                bar_idx, 
                direction, 
                entry_price, 
                entry_bar_id, 
                current_bar_id, 
                best_price_in_market,
                ###
                self.exit_ma_signal,
                self.enable_channel_exit,
                self.optional_channel_exit_condition,
                self.stop_profit_enable,
                self.profit_management_enable_threshold, # over this one, half gain is stop los
                self.neutual_exit_enable,
                self.exit_duration_threshiold,
                self.take_profit_above_x, # take profit when it reach 'take_profit_above_x_threshold'
                self.take_profit_above_x_threshold  
            )
        
        return res

    
    
def gen_strategy_bundle(exit_duration_threshiold_set, exit_profit_threshiold_set):
    res = []
    for exit_duration_threshiold in exit_duration_threshiold_set:
        for exit_profit_threshiold in exit_profit_threshiold_set:
            param = {
                "exit_duration_threshiold": exit_duration_threshiold,
                "exit_profit_threshiold": exit_profit_threshiold
            }
            res.append(param)
    return res