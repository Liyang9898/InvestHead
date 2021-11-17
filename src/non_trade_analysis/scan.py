'''
Created on Jul 10, 2020

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
from non_trade_analysis.scan_util import scanMinMax,assignBucket,bucket
from non_trade_analysis.bucket_massage_util import process_bucket
from non_trade_analysis.ui import draw_chat,draw_chat_6

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

bucket_contain = {}
for b in bucket:
    bucket_contain[b]=[]

bar_cnt = 0
while bar_cnt < df_len:
    # check max up and low in a range
    scan_res = scanMinMax(df, bar_cnt)
    
    if scan_res['tag'] in bucket:
        bucket_contain[scan_res['tag']].append(scan_res)
    
    bar_cnt = bar_cnt + 1
    

distribution_3_day_all = {}
distribution_7_day_all = {}
distribution_14_day_all = {}

# all days in same tag grouped together
for tag in bucket:
    a=process_bucket(bucket_contain[tag])

    x3 = a['3_list_min']
    x7 = a['7_list_min']
    x14 = a['14_list_min']
    
    distribution_3_day_all[tag] = x3
    distribution_7_day_all[tag] = x7
    distribution_14_day_all[tag] = x14

    pei =  draw_chat(x3, x7,x14, '3 days', '7 days', '14 days',tag)
    print(tag, a)



# print(bucket_contain['1000+'])
# for x in bucket_contain['1000+']:
#     print(x)

# bucket = [
#     '0-200',
#     '200-400',
#     '400-600',
#     '600-800',
#     '800-1000',
#     '1000+'
# ]
peix3 =  draw_chat_6(
    distribution_3_day_all['0-200'],
    distribution_3_day_all['200-400'],
    distribution_3_day_all['400-600'],
    distribution_3_day_all['600-800'],
    distribution_3_day_all['800-1000'],
    distribution_3_day_all['1000+'],
    '0-200',
    '200-400',
    '400-600',
    '600-800',
    '800-1000',
    '1000+',
    '3 days'
)

peix7 =  draw_chat_6(
    distribution_7_day_all['0-200'],
    distribution_7_day_all['200-400'],
    distribution_7_day_all['400-600'],
    distribution_7_day_all['600-800'],
    distribution_7_day_all['800-1000'],
    distribution_7_day_all['1000+'],
    '0-200',
    '200-400',
    '400-600',
    '600-800',
    '800-1000',
    '1000+',
    '7 days'
)

peix14 =  draw_chat_6(
    distribution_14_day_all['0-200'],
    distribution_14_day_all['200-400'],
    distribution_14_day_all['400-600'],
    distribution_14_day_all['600-800'],
    distribution_14_day_all['800-1000'],
    distribution_14_day_all['1000+'],
    '0-200',
    '200-400',
    '400-600',
    '600-800',
    '800-1000',
    '1000+',
    '14 days'
)
# print(distribution_3_day_all)
