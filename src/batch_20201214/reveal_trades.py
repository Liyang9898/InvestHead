'''
Created on Dec 29, 2020

@author: leon
'''

from indicator_master.indicator_caching_lib import csv2df_indicator
from trading_floor.gen_trades import gen_trades
from trade_analysis_lib.cash_position_tool import genPositionHistory
from strategy_lib.strat_ma_8_21spy import StrategySimpleMA as StrategySimpleMA_8_21
from strategy_lib.strat_ma_21_50spy import StrategySimpleMA as StrategySimpleMA_21_50
# strat_ma_trend_20200707
from indicator_master.indicator_compute_lib import tsfilter
from indicator_master.plot_indicator_lib import plot_indicator
from trading_floor.TradePlot import plot_trades
from global_constant.constant import folder_path_price_with_indicator,file_type_postfix,folder_path_trades_csv
from plotting_lib.simple import plotTimeSerisDic,plotTimeSerisDic3 
############################################strat region start#############################################
# ma = "8_21"
ma = "21_50"
############################################strat region start#############################################

############################################source region start#############################################

ticker='fb'
############################################source region end#############################################
price_with_indicator_file_path = "D:/f_data/sweep_20201214/indicator_stock_20210106/" + ticker +'_downloaded_raw.csv'
trade_summary_path = "D:/f_data/dump/"+ticker

df = csv2df_indicator(price_with_indicator_file_path)
#time filter   Common BTC pattern start with "2017-01-01 20:00:00"
#time
start_time="2016-01-01 20:00:00"
end_time="2020-12-31 19:00:00"


price_with_indicator = tsfilter(df,start_time,end_time)

# plot raw price with indicator
plot_indicator(price_with_indicator, 'sequence_8_21_50')
strategy_param_bundle={
    "exit_duration_threshiold": 4, # after x bar, allow neutral exit
    "exit_profit_threshiold": 0.001, # no specific meaning
    "neutual_exit_enable":0,
    "profit_management_enable":1,
    "profit_management_enable_threshold":0.04,
}

strategy=None
if ma is "8_21":
    strategy=StrategySimpleMA_8_21(strategy_param_bundle)
elif ma is "21_50":
    strategy=StrategySimpleMA_21_50(strategy_param_bundle)
    
trades_consecutive = gen_trades(df=price_with_indicator, strategy=strategy, all_bar_entry=False)
# trades_all_entry = gen_trades(df=price_with_indicator, strategy=strategy, all_bar_entry=True)
 
#print trades summary to csv
# path_out="""D:/f_data/trades_summary_test.csv"""
# trades_consecutive.tradeSummary2CSV(path_out)

# printing logic
trades_consecutive.printWinTrades()
trades_consecutive.printLoseTrades()
trades_consecutive.printNeutralTrades()
print('Consecutive trade summary')
trades_consecutive.printTradesSummary()
print('All entry trade summary')
# trades_all_entry.printTradesSummary()

#csv
# trades_consecutive.trades2CSV(trades_csv_file)

# price history chart
cash_history = genPositionHistory(price_with_indicator, trades_consecutive.trades, start_time, end_time)

plotTimeSerisDic3(cash_history['price_position'],cash_history['cash_fixed_base_position'],cash_history['cash_rollover_position'])


plot_trades(price_with_indicator, '', trades_consecutive, entry_only=False)
