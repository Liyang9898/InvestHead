'''
Created on Jul 20, 2020
@author: leon
'''


from api.api import api_gen_trades
from batch_20201214.batch_trade_lib import gen_trades_based_on_price_with_indicator
from global_constant.constant import folder_path_price_with_indicator, file_type_postfix, folder_path_trades_csv
from indicator_master.indicator_caching_lib import csv2df_indicator
from indicator_master.indicator_compute_lib import tsfilter
from indicator_master.plot_indicator_lib import plot_indicator
import pandas as pd
from plotting_lib.simple import plotTimeSerisDic, plotTimeSerisDic3
from strategy_lib.stratage_param import (
    strat_param_swing,
    strat_param_swing_2150in_821out,
    strat_param_swing_2150in_850out,
    strat_param_swing_2150in_2150out,
    strat_param_swing_2150in_2150out_trend_start,
    strat_param_channel_only_50in75out_21_50,
    strat_param_swing_2150in_2150out_channel_inout,
    strat_param_swing_2150in_2150out_ma_gap,
    strat_param_swing_2150in_2150out_ma_gap_4p_out,
    strat_param_swing_2150in_2150out_ma_gap_6p_out,
    strat_param_swing_2150in_2150out_ma_gap_8p_out,
    strat_param_swing_2150in_2150out_ma_gap_10p_out,
    strat_param_swing_2150in_2150out_ma_gap_12p_out,
    strat_param_swing_2150in_2150out_no_profit_manage,
    strat_param_swing_821in_821out_no_profit_manage,
    strat_param_swing_821in_821out_ma_gap,
    strat_param_swing_821in_821out_ma_gap_4p_out,
    strat_param_swing_821in_821out_ma_gap_8p_out,
    strat_param_swing_821in_821out_ma_gap_12p_out,
    spy_ma21_50_swing_cross_inout,
    spy_ma21_50in8_21out_swing_cross_inout
, strat_param_swing_2150in_2150out_plain, strat_param_long_8_21_50_only,
    strat_param_20211006,
    strat_param_20211006_ma_max_drawdown_cut, strat_param_20211006_ma_macd,
    strat_param_20211006_ma_max_drawdown_cut_neutral_out,
    strat_param_20211006_ma_only_exit, strat_param_20211030_ma_only_exit_8_21)
from trade_analysis_lib.cash_position_tool import genPositionHistory
from trading_floor.TradeInterface import merge_trade_summary, genTradingBundleFromCSV, merged_result_to_csv, print_merged_result
from trading_floor.TradePlot import plot_trades, plot_win_lose_trade_size
from util.util import plot_hist_from_df_col
from util.util_finance import trade_distribution_plot
from util.util_temp import ts_position_dict_to_csv, \
    ts_position_dicts_to_dataframe
from util.util_time import df_filter_dy_date


############################################source region start#############################################
# file_name = "SPY_1D_fmt"  # 1993.3 start
# file_name = "SPY_1W_fmt"  # 1993.3 start
# file_name = "BTC_1W_fmt"   # 2017.1 start
file_name = "BTC_1D_fmt"   # 2017.1 start
# file_name = "BTC_4H_fmt" # 2017.1 start
# file_name = "BTC_2H_fmt" # 2017.1 start

# file_name = "XLK_1W_fmt"
# file_name = "ACAD_1D_fmt"
# file_name = "GHSI_1D_fmt" 

# file_name = "FTNT_1D_fmt" 
# file_name = "GOOG_1D_fmt" 
# file_name = "AMZN_1D_fmt" 
# file_name = "TSLA_1D_fmt"  # 1993.3 start

file_name = "V_1D_fmt"  
# file_name = "IWF_1D_fmt"
# file_name = "IWF_1W_fmt"
# file_name = "AMD_1D_fmt"
# file_name = "GOLD_1D_fmt"
# file_name = "EURUSD_1D_fmt"
# file_name = "V_1D_fmt"
############################################source region end#############################################

ticker = 'SPY'
indicator_file_postfix = "_idc"

price_with_indicator_file=folder_path_price_with_indicator+file_name+indicator_file_postfix+"."+file_type_postfix


# price_with_indicator_file = "D:/f_data/sweep_20201214/indicator/2021-04-04/" + ticker +'_downloaded_raw.csv'

trades_csv_file = folder_path_trades_csv + file_name + "_trades.csv"

# strategy_param_bundle=strat_param_swing_2150in_2150out
# strategy_param_bundle=spy_ma21_50_swing_cross_inout
# strategy_param_bundle=spy_ma21_50in8_21out_swing_cross_inout
# strategy_param_bundle=strat_param_swing_2150in_2150out_ma_gap_12p_out
# strategy_param_bundle=strat_param_swing_2150in_2150out_no_profit_manage
# strategy_param_bundle = strat_param_long_8_21_50_only


# strategy_param_bundle=strat_param_swing_2150in_2150out_plain # same as strat_param_20211006

# 2021-10-06
# strategy_param_bundle=strat_param_20211006 # same as strat_param_swing_2150in_2150out_plain
# strategy_param_bundle=strat_param_20211006_ma_max_drawdown_cut
# strategy_param_bundle=strat_param_20211006_ma_macd
# strategy_param_bundle=strat_param_20211006_ma_max_drawdown_cut_neutral_out
# strategy_param_bundle=strat_param_20211006_ma_only_exit
# strategy_param_bundle=strat_param_20211030_ma_only_exit_8_21
strategy_param_bundle=strat_param_swing_2150in_2150out_ma_gap #2021-11-18 prod


start_time="2006-01-01"

# start_time="2019-09-01 20:00:00"
end_time="2022-01-31"

ticker='default'

trade_result_all_entry_path=folder_path_trades_csv + file_name + "_trades_consecutive_2.csv"
trade_result_consecutive_entry_path=folder_path_trades_csv + file_name + "_trades_all_entry_2.csv"

#########################################################################################################################
# input: indicator, time range, strategy
# output: trades CSV (all entry and consecutive entry)
print('generating trades')
api_gen_trades(
    ticker=file_name,
    start_date=start_time, 
    end_date=end_time, 
    strategy=strategy_param_bundle,
    indicator_file_path=price_with_indicator_file, 
    trade_result_all_entry_path=trade_result_all_entry_path, 
    trade_result_consecutive_entry_path=trade_result_consecutive_entry_path, 
)
 
print('getting generated trades')
trades_all_entry = genTradingBundleFromCSV(trade_result_all_entry_path)
trades_consecutive = genTradingBundleFromCSV(trade_result_consecutive_entry_path)


df = csv2df_indicator(price_with_indicator_file)
price_with_indicator = df_filter_dy_date(df,'date', start_time,end_time)
# plot_indicator(price_with_indicator, 'sequence_8_21_50',ticker=file_name)
 
  
#########################################################################################################################
 
over_all_summary = merge_trade_summary(trades_consecutive.tradeSummary2dict(),trades_all_entry.tradeSummary2dict())
# printing logic
trades_consecutive.printWinTrades()
trades_consecutive.printLoseTrades()
trades_consecutive.printNeutralTrades()
print('Consecutive trade summary')
trades_consecutive.printTradesSummary()
print('All entry trade summary')
trades_all_entry.printTradesSummary()
 
print(over_all_summary)
merged_result_to_csv(over_all_summary, "D:/f_data/dump/result.csv")
 


cash_position = genPositionHistory(price_with_indicator, trades_consecutive.trades, start_time, end_time)


# dic to df
strategy_name = 'temp'
if 'name' in strategy_param_bundle:
    strategy_name = strategy_param_bundle['name']
path_position_record = f'D:/f_data/temp/position_list_{strategy_name}.csv'

# path_position_record = f'D:/f_data/temp/position_list_ma_drop_15p.csv'

# ts_position_dict_to_csv(cash_position['cash_rollover_position'], path) 
# print(cash_position['cash_rollover_position'].keys())
# path2 = 'D:/f_data/temp/price_cash_line.csv'
# ts_position_dict_to_csv(cash_position['price_position'], path2) 
# print(cash_position['price_position'].keys())

ts_position_dicts_to_dataframe(
    price_dict = cash_position['price_position'], 
    position_dict = cash_position['cash_rollover_position'],
    path=path_position_record
)

 
plotTimeSerisDic3(cash_position['price_position'],cash_position['cash_fixed_base_position'],cash_position['cash_rollover_position'])
 
 
# trades_consecutive
# trades_all_entry
plot_trades(price_with_indicator, '', trades_consecutive, entry_only=False,ticker=price_with_indicator_file)
print('all universe')
 
print_merged_result(over_all_summary)
 
print('all trade summary start')
# trades_all_entry.printWinTrades()
# trades_all_entry.printLoseTrades()
# trades_all_entry.printNeutralTrades()
print('all trade summary end')


trade_distribution_plot(trade_result_consecutive_entry_path, price_with_indicator_file)