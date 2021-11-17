'''
Created on Jun 7, 2020

@author: leon
'''

from indicator_master.indicator_caching_lib import csv2df_indicator

from strategy_lib.strat_ma_trend_20200604 import gen_strategy_bundles,StrategySimpleMAFactory
from indicator_master.indicator_compute_lib import tsfilter
from strategy_param_sweep.strategy_param_sweep_lib import strategy_param_sweep
from util import util

# price_with_indicator_file="D:/f_data/GOOG_1D_with_indicator_20200607.csv"
# price_with_indicator_file="""D:/f_data/BTC_4HOUR_fmt_with_indicator_20200607.csv"""
# price_with_indicator_file="""D:/f_data/BTC_1D_with_indicator_20200607.csv"""
# price_with_indicator_file="""D:/f_data/SPY_1D_fmt_with_indicator_20200607.csv"""
# price_with_indicator_file="""D:/f_data/SPY_1W_fmt_with_indicator_20200607.csv"""
price_with_indicator_file="""D:/f_data/BTC_4HOUR_fmt_with_indicator_20200607.csv"""


df = csv2df_indicator(price_with_indicator_file)
#time filter   Common BTC pattern start with "2017-01-01 20:00:00"
start_time="2001-05-01 20:00:00"
end_time="2020-07-26 19:00:00"
price_with_indicator = tsfilter(df,start_time,end_time)



exit_duration_threshiold_set=[3]
exit_profit_threshiold_set=[0.003,0.005,0.01,0.02,0.03,0.04]
strategy_param_bundle_set = gen_strategy_bundles(exit_duration_threshiold_set, exit_profit_threshiold_set)
# print(strategy_param_bundle_set)

path_out="""D:/f_data/strategy_param_sweep_test2.csv"""
strategy_simple_MA_factory=StrategySimpleMAFactory()
sweep_result=strategy_param_sweep(
    strategy_simple_MA_factory,
    price_with_indicator,
    strategy_param_bundle_set, 
    path_out
)

sweep_result_reindexed = sweep_result.reset_index()

for i in range(0, len(sweep_result_reindexed)):
    trade_summary_str = util.printTradesSummary(
        sweep_result_reindexed.loc[i, 'win_rate'],
        sweep_result_reindexed.loc[i, 'lose_rate'],
        sweep_result_reindexed.loc[i, 'neutral_rate'],
        sweep_result_reindexed.loc[i, 'total_trades'],
        sweep_result_reindexed.loc[i, 'win'],
        sweep_result_reindexed.loc[i, 'win_pnl_p'],
        sweep_result_reindexed.loc[i, 'lose'],
        sweep_result_reindexed.loc[i, 'lose_pnl_p'],
        sweep_result_reindexed.loc[i, 'neutral'],
        util.decode_dict(sweep_result_reindexed.loc[i, 'trading_params'])
        
    )
    print(trade_summary_str)

