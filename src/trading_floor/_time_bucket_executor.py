'''
Created on Jul 9, 2020

@author: leon
'''

from indicator_master.indicator_caching_lib import csv2df_indicator
from trading_floor.gen_trades import gen_trades
from strategy_lib.strat_ma_trend_20200707 import StrategySimpleMA
from indicator_master.indicator_compute_lib import tsfilter
from global_constant.constant import folder_path_price_with_indicator,file_type_postfix
from util.util import plus_day,make_date_chain,bracket_value_in_dict,plot_time_series
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from trading_floor.TradePlot import plot_trades

############################################source region start#############################################
# file_name = "BTC_1D_fmt"
file_name = "BTC_4H_fmt"
############################################source region end#############################################
start_time="2019-07-01"
end_time="2019-09-01"
time_gap = 15
dates = make_date_chain(start_time,end_time, time_gap)

indicator_file_postfix = "_idc"
price_with_indicator_file=folder_path_price_with_indicator+file_name+indicator_file_postfix+"."+file_type_postfix
df = csv2df_indicator(price_with_indicator_file)
 
 
strategy_param_bundle={
    "exit_duration_threshiold": 3,
    "exit_profit_threshiold": 1000,
    "neutual_exit_enable":1,
    "stop_profit_enable":1,
    "stop_profit_percent":0.004,
}
strategy=StrategySimpleMA(strategy_param_bundle)

def execute_strategy_one_time(start_time,end_time):     
    price_with_indicator = tsfilter(df,start_time,end_time)
 
    trades_consecutive = gen_trades(df=price_with_indicator, strategy=strategy, all_bar_entry=False)
#     trades_all_entry = gen_trades(df=price_with_indicator, strategy=strategy, all_bar_entry=True)
    plot_trades(price_with_indicator, '', trades_consecutive, entry_only=False)
 
    print("time period",start_time,end_time)
#      
#     print('Consecutive trade summary')
#     trades_consecutive.printTradesSummary()
#     print('All entry trade summary')
#     trades_all_entry.printTradesSummary()
    res = {
        'ts':start_time,
        'win_pnl':trades_consecutive.win_pnl_p,
        'lose_pnl':trades_consecutive.lose_pnl_p,
        'pnl':trades_consecutive.win_pnl_p+trades_consecutive.lose_pnl_p,
        'win_rate':trades_consecutive.win_rate,
        'lose_rate':trades_consecutive.lose_rate,
        'trades':len(trades_consecutive.trades)
    }
    return res

df_list=[]
for x in range(0,len(dates)-1,1):
    start_time=dates[x]+ " 00:00:00"
    end_time=dates[x+1]+ " 00:00:00"
    res = execute_strategy_one_time(start_time,end_time)
    bracket_value_in_dict(res)
    trade_sample_df = pd.DataFrame(data=res)
    df_list.append(trade_sample_df)
    merged = pd.concat(df_list)
    

time_gap_str = " - time gap: "+str(time_gap)
fig_pnl = go.Figure(data=go.Scatter(x=merged["ts"], y=merged['pnl'], mode="lines+markers",name="total pnl %"))
fig_pnl.add_scatter(x=merged["ts"], y=merged['lose_pnl'],mode="lines+markers",name="lose pnl %")
fig_pnl.add_scatter(x=merged["ts"], y=merged['win_pnl'],mode="lines+markers",name="win pnl %")
fig_pnl.update_layout(title='Percent PNL'+time_gap_str).show()


fig_rate = go.Figure(data=go.Scatter(x=merged["ts"], y=merged['win_rate'], mode="lines+markers",name="win rate %"))
fig_rate.add_scatter(x=merged["ts"], y=merged['lose_rate'],mode="lines+markers",name="lose rate %")
fig_rate.update_layout(title='Win Rate'+time_gap_str).show()

fig_tradeds = go.Figure(data=go.Scatter(x=merged["ts"], y=merged['trades'], mode="lines+markers",name="win rate %"))
fig_tradeds.update_layout(title='Trade Count'+time_gap_str).show()
