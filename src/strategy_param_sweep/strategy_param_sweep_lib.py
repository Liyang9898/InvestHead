'''
Created on Jun 15, 2020

@author: leon
'''

from trading_floor.gen_trades import gen_trades
import pandas as pd
from indicator_master.constant import trade_summary_interface


def strategy_param_sweep(
    strategy_factory,
    price_with_indicator, 
    strategy_param_bundle_set, 
    path_out
):
    df_list=[]
    for strategy_param_bundle in strategy_param_bundle_set:
        strategy=strategy_factory.genStrategySimpleMA(strategy_param_bundle)
        trades = gen_trades(price_with_indicator, strategy)
        summary_one_param = trades.tradeSummary2dict()
        summary_one_param_df = pd.DataFrame(data=summary_one_param)
        df_list.append(summary_one_param_df)
    merged = pd.concat(df_list)
    merged.to_csv(
        path_out, 
        columns =trade_summary_interface,# must match d
        index=False
    )
    return merged