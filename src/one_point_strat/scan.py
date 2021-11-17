'''
Created on Nov 19, 2020

@author: leon
'''

from indicator_master.indicator_caching_lib import csv2df_indicator
from trading_floor.gen_trades import gen_trades
# from strategy_lib.strat_ma_swing import StrategySimpleMA
from strategy_lib.strat_ma_8_21spy import StrategySimpleMA

from indicator_master.indicator_compute_lib import tsfilter
from indicator_master.plot_indicator_lib import plot_indicator
from trading_floor.TradePlot import plot_trades
from global_constant.constant import folder_path_price_with_indicator,file_type_postfix


############################################source region start#############################################
file_name = "SPY_1D_fmt"
# file_name = "SPY_1W_fmt"
# file_name = "BTC_1D_fmt"
# file_name = "BTC_4H_fmt"
# file_name = "XLK_1W_fmt"
############################################source region end#############################################

indicator_file_postfix = "_idc"
price_with_indicator_file=folder_path_price_with_indicator+file_name+indicator_file_postfix+"."+file_type_postfix

df = csv2df_indicator(price_with_indicator_file)
#time filter   Common5BTC pattern start with "2017-01-01 20:00:00"
start_time="1991-09-03 20:00:00"
end_time="2021-01-08 19:00:00"
 
# start_time="2010-01-05 20:00:00"
# end_time="2021-01-08 19:00:00"

price_with_indicator = tsfilter(df,start_time,end_time)

# plot raw price with indicator
# plot_indicator(price_with_indicator, 'sequence_8_21_50')


df_len = len(price_with_indicator.index)

print('total bars=', df_len)

# bucket_contain = {}
# for b in bucket:
#     bucket_contain[b]=[]

bar_cnt = 0
exceed_one_bi_dir = 0
positive = []
negative = []
while bar_cnt < df_len:
    bar_now = df.iloc[bar_cnt,:]
    low = bar_now['low']
    high = bar_now['high']
    open = bar_now['open']
    ts = bar_now['est_datetime']
    up = abs(high - open)
    down = abs(open - low)
    
    if up >= 0.1 and down >= 0.1:
        exceed_one_bi_dir=exceed_one_bi_dir+1
        positive.append(ts)
    else:
        negative.append(ts)
    
    bar_cnt = bar_cnt + 1
    
    ## log
    
    print(bar_cnt, low, high, open)
    


for t in negative:
    print(t)
    
print(len(negative),'/',bar_cnt)
print(float(len(negative))/float(bar_cnt))