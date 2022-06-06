'''
Created on Jan 26, 2021

@author: leon
'''
from strategy_lib.strategy_constant import EXIT_STRATEGY_LEGACY, \
    EXIT_STRATEGY_MA_ONLY, EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT, \
    EXIT_STRATEGY_MA_MACD, EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT_NEUTRAL_OUT

"""
strat_param_swing_2150in_2150out_ma_gap -> current swing prod
strat_param_20211006_ma_max_drawdown_cut -> spy
strat_param_20211006_ma_macd -> btc
"""



strat_param_swing = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_swing_2150in_821out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_swing_2150in_850out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"8_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

##########major prod ############################
strat_param_swing_2150in_2150out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_swing_2150in_2150out_channel_enter = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":1,
    "enable_channel_exit":0,
}

strat_param_swing_2150in_2150out_channel_exit = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":1,
}

strat_param_swing_2150in_2150out_channel_inout = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":1,
    "enable_channel_exit":1,
}


strat_param_swing_2150in_2150out_trend_start = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "enter_on_trend_start":1,
}

strat_param_channel_optimized_swing = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":1,
    "enable_channel_exit":1,
}

strat_param_channel_only_50in75out_21_50 = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":1,
    "enable_channel_exit":1,
}

strat_param_channel_only_50in75out_8_21 = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":1,
    "enable_channel_exit":1,
}

ribbon_start={
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "enable_ribbon_expand_start_enter":1
}

strat_param_swing_2150in_2150out_4percent_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

# ema21 ma50 gap - prod since 2021/04
# profit managment = half best out
strat_param_swing_2150in_2150out_ma_gap = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}


strat_param_swing_2150in_2150out_ma_gap_4p_profit = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap - prod since 2021/04
strat_param_swing_2150in_2150out_ma_gap_no_take_profit = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}


# ema21 ma50 gap + 4% out
strat_param_swing_2150in_2150out_ma_gap_4p_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap - 4p investigate - no profit manage
strat_param_swing_2150in_2150out_no_profit_manage = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap + 3% out
strat_param_swing_2150in_2150out_ma_gap_3p_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.03,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap + 6% out
strat_param_swing_2150in_2150out_ma_gap_6p_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.06,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.06,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap + 8% out
strat_param_swing_2150in_2150out_ma_gap_8p_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.08,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.08,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap + 10% out
strat_param_swing_2150in_2150out_ma_gap_10p_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.1,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.1,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap + 12% out
strat_param_swing_2150in_2150out_ma_gap_12p_out = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.12,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.12,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# no profit 8-21
strat_param_swing_821in_821out_no_profit_manage = {
    "enter_ma_signal": "8_21",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

strat_param_swing_821in_821out_ma_gap = {
    "enter_ma_signal": "8_21",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

strat_param_swing_821in_821out_ma_gap_4p_out = {
    "enter_ma_signal": "8_21",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

strat_param_swing_821in_821out_ma_gap_8p_out = {
    "enter_ma_signal": "8_21",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.08,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.08,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

strat_param_swing_821in_821out_ma_gap_12p_out = {
    "enter_ma_signal": "8_21",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.12,
    "take_profit_above_x":1,
    "take_profit_above_x_threshold":0.12,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.039
}

# ema21 ma50 gap - prod since 2021/04
spy_ma21_50_swing_cross_inout = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.0
}

spy_ma21_50in8_21out_swing_cross_inout = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
    "ema21_ma50_gap_percent_threshold": 0.0
}

# enter on:
# 21>50
# 21 50 gap increase
# 21 50 all up
# 
# exit on:
# 21 < 50
strat_param_swing_2150in_2150out_plain = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

# for spy, usually, exit on 21 cross 50 is too late because the drop is fast
strat_param_long_8_21_50_only = {
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"not_long_8_21_50",
#     "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

################################################2021-10-06###################################################
strat_param_20211006 = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 8,21,50 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "name": 'strat_param_20211006',
    "exit_strategy": EXIT_STRATEGY_LEGACY,
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_20211006_ma_only_exit = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 8,21,50 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "exit_strategy": EXIT_STRATEGY_MA_ONLY,
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}


strat_param_20211030_ma_only_exit_8_21 = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 8,21,50 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "exit_strategy": EXIT_STRATEGY_MA_ONLY,
    "enter_ma_signal": "8_21",
    "exit_ma_signal":"8_21",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_20211006_ma_macd = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 8,21,50 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "name": 'strat_param_20211006_ma_macd',
    "exit_strategy": EXIT_STRATEGY_MA_MACD,
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_20220605_200ma_up_ma_macd = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 21,50,200 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "name": 'strat_param_20220605_200ma_up_ma_macd',
    "exit_strategy": EXIT_STRATEGY_MA_MACD,
    "enter_ma_signal": "21_50_200",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}

strat_param_20211006_ma_max_drawdown_cut = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 8,21,50 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "name": 'strat_param_20211006_ma_max_drawdown_cut',
    "exit_strategy": EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT,
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}


strat_param_20211006_ma_max_drawdown_cut_neutral_out = {
    # out: 21_50 ma, 
    # in: 21_50 ma, all 8,21,50 ma goes up, 21-50 macd
    # using field 'exit_strategy'
    "name": 'strat_param_20211006_ma_max_drawdown_cut_neutral_out',
    "exit_strategy": EXIT_STRATEGY_MA_MAX_DRAWDOWN_CUT_NEUTRAL_OUT,
    "enter_ma_signal": "21_50",
    "exit_ma_signal":"21_50",
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":0,
    "profit_management_enable_threshold":0.04,
    "take_profit_above_x":0,
    "take_profit_above_x_threshold":0.04,    
    "enable_channel_enter":0,
    "enable_channel_exit":0,
}


