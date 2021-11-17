
from ma.addindicator import load_df_add_indicator
from ma.gentrade import gen_trades_always_in, trade_summary, exit_when_drop, \
    early_exit_improvement, trade_summary_early_exit, max_pullback, \
    trade_summary_high_v_entry, trade_summary_early_exit_high_v, print_trade, \
    trade_win_lose_diff, trade_win_lose_bz, trade_win_lose_p2ema_diff, \
    trade_win_lose_v_diff, df2dic, feature_distribution, gen_trade_df, \
    trade_summary_close_ma, trade_summary_early_exit_high_v_close_ma, \
    gen_trade_summary, print_trades, gen_trade_summary_raw, \
    gen_trade_summary_long, print_trades_long
from ma.improve_trade import improve_entry_and_exit
from ma.plotindicator import plot_symbol, plotpie
import pandas as pd


# ma_indicator = 'sequence_p_8_21'
# ma_indicator = 'sequence_8_21'
ma_indicator = 'sequence_8_21_50'

# filename = 'BATS_SPY, 1W'
# filename = 'BATS_SPY, 1D_trend'
# 
# filename = 'BATS_NFLX, 1D'
# filename = 'BATS_HUYA, 1D (3)'
# filename = 'BATS_TSLA, 1D'
# filename = 'BATS_UBER, 1D (1)'
# filename = 'BATS_LYFT, 1D (1)'
# filename = 'BATS_USO, 1D'
# filename = 'download_yfinance/PCB_download_format'


# filename = 'BITSTAMP_BTCUSD, 1D'
# filename = 'BITSTAMP_BTCUSD, 1W'
# filename = 'BITSTAMP_BTCUSD, 240'
# filename = 'BITSTAMP_BTCUSD, 60'
# filename = 'BATS_TWTR, 1D'
# filename = 'BATS_BYND, 1D'
# filename = 'BATS_JD, 1D'
# filename = 'BATS_BABA, 1D'
filename = 'BATS_SPY, 1W'


path_in = """D:/f_data/{file_name}.csv""".format(file_name=filename)

path_in_download = """D:/f_data/download_yfinance/{ticker}_download_format.csv""".format(ticker='XEL')

df_with_indicator = load_df_add_indicator(path_in, '1994-01-03', '2020-010-01')
# plot_symbol(df_with_indicator, ma_indicator)
 
trades = gen_trades_always_in(df_with_indicator, ma_indicator)    
sum = gen_trade_summary_raw(trades)
print(sum)

OVERLAP_EMA21 = 'price overlap ema21'
BELOW_ENTRY = 'x% below entry'
HALF_MAX = 'drop to x% of max reach'
BREACH_RETURN = 'drop to entry after breach'
JUMP_RETURN = 'drop to entry after breach jump over'
 
SPEED = 'speed_ema8'
NEAR = 'near_ema8'

 
trades_improved = improve_entry_and_exit(
    df_day=df_with_indicator, 
    trades=trades, 
    # enter params
    start_v=0.02,  # must adjust according to stock!!! 
    distance=0.05,
    # exit params
    threshold_below_entry=0.05, 
    breach_threshold_above_entry=0.05,  # must adjust according to stock!!! 
    bar_count_threshold=11, 
    max_reach_drop_percent=0.5,
    enter_impro_strat=[
#         SPEED,
#         NEAR
    ],
    exit_impro_strat=[
#         OVERLAP_EMA21,
#         BELOW_ENTRY,
#         HALF_MAX,
#         BREACH_RETURN
    ]
)
 
print('============================improved==============================')
sum_improved = gen_trade_summary(trades_improved)
print(sum_improved)
plot_symbol(df_with_indicator, ma_indicator, trades_improved)
# print_trades(trades_improved)
print('============================long only==============================')
# print_trades_long(trades_improved)


trades_improved_profit_managed = improve_entry_and_exit(
    df_day=df_with_indicator, 
    trades=trades, 
    # enter params
    start_v=0.02,  # must adjust according to stock!!! 
    distance=0.05,
    # exit params
    threshold_below_entry=0.05, 
    breach_threshold_above_entry=0.02,  # must adjust according to stock!!! 
    bar_count_threshold=11, 
    max_reach_drop_percent=0.5,
    enter_impro_strat=[
#         SPEED,
#         NEAR
    ],
    exit_impro_strat=[
#         OVERLAP_EMA21,
#         BELOW_ENTRY,
#         HALF_MAX,
#         BREACH_RETURN
    ]
)

print('============================improved,  profit managed==============================')
sum_improved_profit_managed = gen_trade_summary(trades_improved_profit_managed)
print(sum_improved_profit_managed)

# sum_improved_profit_managed_long = gen_trade_summary_long(trades_improved_profit_managed)
# print(sum_improved_profit_managed_long)

# print_trades(trades_improved_profit_managed)

# 
# trades = exit_when_drop(df_with_indicator, trades, 11,0.01, 0.5)
# trade_sum = trade_summary(trades)
# trade_sum_early_exit = trade_summary_early_exit(trades)
# trade_sum_high_v_enter=trade_summary_high_v_entry(trades,0.02)
# trade_sum_close_ma_enter = trade_summary_close_ma(trades,0.05)
# trade_sum_high_v_enter_early_exit=trade_summary_early_exit_high_v(trades,0.02)
# trade_sum_high_v_enter_early_exit_close_ma=trade_summary_early_exit_high_v_close_ma(trades,0.02,0.05)
# 
# plot_symbol(df_with_indicator, ma_indicator, trades_improved_profit_managed)
# 
# trades_df=gen_trade_df(trades)
# trades_df_high_v = trades_df.loc[trades_df['start_v'] > 0.02]
# # feature_distribution(trades_df_high_v, 'p2ema8_diatance %')
# # 
# print('================== win  trade===============')
# print(trades_df_high_v.loc[trades_df_high_v['label'] == True][['enter_ts','p2ema8_diatance %']])
# print('==================  lose trade===============')
# print(trades_df_high_v.loc[trades_df_high_v['label'] == False][['enter_ts','p2ema8_diatance %']])
# 
# 
# print('==================summary===============')
# for k, v in trade_sum.items():
#     print(k + ':' + str(v))
#     
# print('==================summary high v enter + early exit===============')
# for k, v in trade_sum_high_v_enter_early_exit.items():
#     print(k + ':' + str(v))
# 
# 
# print('==================summary high v enter, close MA + early exit===============')
# for k, v in trade_sum_high_v_enter_early_exit_close_ma.items():
#     print(k + ':' + str(v))
#     
# 
# print('==================summary high v enter===============')
# for k, v in trade_sum_high_v_enter.items():
#     print(k + ':' + str(v))
# 
# print('==================summary close ma enter===============')
# for k, v in trade_sum_close_ma_enter.items():
#     print(k + ':' + str(v))
# 
# # 
# print('==================summary early exit===============')
# for k, v in trade_sum_early_exit.items():
#     print(k + ':' + str(v))


# print('==================early exit===============')
# early_exit_improvement(trades)
# 
# print('==================max pullback===============')
# max_pullback(trades)

# print('==================low speed trade===============')
# for trade in trades:
#     if trade['start_v'] < 0.02:
#         print_trade(trade)
