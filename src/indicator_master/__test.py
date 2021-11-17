'''
Created on Jul 19, 2020

@author: leon
'''
import plotly.express as px
from indicator_master.indicator_caching_lib import csv2df_indicator
from trading_floor.gen_trades import gen_trades
from strategy_lib.strat_ma_trend_20200707 import StrategySimpleMA
# strat_ma_trend_20200707
from indicator_master.indicator_compute_lib import tsfilter
from indicator_master.plot_indicator_lib import plot_indicator
from trading_floor.TradePlot import plot_trades
from global_constant.constant import folder_path_price_with_indicator,file_type_postfix,folder_path_trade_summary
import plotly.graph_objects as go

############################################source region start#############################################
# file_name = "SPY_1D_fmt"
# file_name = "SPY_1W_fmt"
file_name = "BTC_1D_fmt"
# file_name = "BTC_4H_fmt"
# file_name = "BTC_2H_fmt"
# file_name = "BTC_4H_0718_fmt"
############################################source region end#############################################

indicator_file_postfix = "_idc"
price_with_indicator_file=folder_path_price_with_indicator+file_name+indicator_file_postfix+"."+file_type_postfix

df = csv2df_indicator(price_with_indicator_file)
#time filter   Common BTC pattern start with "2017-01-01 20:00:00"
start_time="1993-07-15 00:00:00"
end_time="2019-08-01 00:00:00"

# start_time="2019-07-01 20:00:00"
# end_time="2020-07-01 19:00:00"


price_with_indicator = tsfilter(df,start_time,end_time)

threshold = 0.003
df_in_high=price_with_indicator.loc[(df['high_open_p']<=threshold)]
df_in_low=price_with_indicator.loc[(df['low_open_p']<=threshold)]
print('sample_size=', len(price_with_indicator))
print('sample_size_small_p=', len(df_in_high))
print('sample_size_small_p=', len(df_in_low))
print('chance high',len(df_in_high)/len(price_with_indicator))
print('chance low',len(df_in_low)/len(price_with_indicator))