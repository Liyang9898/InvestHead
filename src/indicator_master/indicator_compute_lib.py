'''
Created on Jun 4, 2020

@author: leon
'''
from bisect import bisect_left
import bisect
from datetime import datetime, timedelta

from indicator_master.feature_lib.max_drawdown import get_down_from_peak
from indicator_master.feature_lib.velocity import get_velocity_one_bar_on_close, \
    get_velocity_pct_on_metric
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
import numpy as np
from strategy_lib.strat_ma_base import StrategySimpleMABase
from strategy_lib.stratage_param import strat_param_swing_2150in_2150out
from strategy_lib.strategy_util.signal import all_ma_upwards, macd, \
    ma_enter_sequence


# This library add indicator to each bar, input df should has the following interface: see global_constant file
def add_indicator(df):
    instance = StrategySimpleMABase(strat_param_swing_2150in_2150out)
    # meta info
    df['est_datetime']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d %H:%M:%S'), axis = 1)
    df['date']=df.apply(lambda row : str(datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d')), axis = 1)
    df['est_time']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%H:%M:%S'), axis = 1)
    
    # ribbon
    df['ema55'] = df['close'].ewm(span=55,min_periods=0,adjust=False,ignore_na=False).mean()
    df['ema20'] = df['close'].ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()
    df['ema55_20_gap'] = df['ema20'] - df['ema55']
    
    for i in range(0, len(df)):
        if i >= 1:
            df.loc[i, 'ema55_20_gap_delta'] = abs(df.loc[i, 'ema55_20_gap']) - abs(df.loc[i-1, 'ema55_20_gap'])
    
    df['ema55_20_gap_delta_up']=df.apply(lambda row : mark_gap_ema_20_50_delta(row['ema55_20_gap_delta'], row['high'], True), axis = 1)
    df['ema55_20_gap_delta_down']=df.apply(lambda row : mark_gap_ema_20_50_delta(row['ema55_20_gap_delta'], row['high'], False), axis = 1)
    
    # ribbon plus, shrink_block
    df['shrink_block']=-1
    for i in range(0, len(df)):
        if i >= 2:
            if df.loc[i, 'ema55_20_gap_delta'] < 0 and df.loc[i-1, 'ema55_20_gap_delta'] < 0 and df.loc[i-2, 'ema55_20_gap_delta'] < 0:
                df.loc[i, 'shrink_block'] = 1
    df['shrink_block_mark'] = df.apply(lambda row : mark_shrink_block(row['shrink_block'], row['high']), axis = 1)
    
    df['ribbon_expand_seq'] = -1
    for i in range(0, len(df)):
        if i >= 5:
            if df.loc[i, 'ema55_20_gap_delta'] > 0 and df.loc[i-1, 'shrink_block']==1: # current 1st expend
                df.loc[i, 'ribbon_expand_seq'] = 1
            if df.loc[i, 'ema55_20_gap_delta'] > 0 and df.loc[i-1, 'ribbon_expand_seq']==1: # current 2st expend
                df.loc[i, 'ribbon_expand_seq'] = 2    
            if df.loc[i, 'ema55_20_gap_delta'] > 0 and df.loc[i-1, 'ribbon_expand_seq']==2: # current 3st expend
                df.loc[i, 'ribbon_expand_seq'] = 3                   
    df['ribbon_expand_seq_1st'] = df.apply(lambda row : mark_ribbon_expand(row['ribbon_expand_seq'], 1, row['high']), axis = 1)            
    df['ribbon_expand_seq_2st'] = df.apply(lambda row : mark_ribbon_expand(row['ribbon_expand_seq'], 2, row['high']), axis = 1)      
    df['ribbon_expand_seq_3st'] = df.apply(lambda row : mark_ribbon_expand(row['ribbon_expand_seq'], 3, row['high']), axis = 1)      

    # things related to precious ds
    base_projector='ema8'
    for i in range(0, len(df)):
        if i >= 1:
            df.loc[i, 'ema8_delta'] = df.loc[i, 'ema8'] - df.loc[i-1, 'ema8']
            df.loc[i, 'ema21_delta'] = df.loc[i, 'ema21'] - df.loc[i-1, 'ema21']
            df.loc[i, 'ma50_delta'] = df.loc[i, 'ma50'] - df.loc[i-1, 'ma50']
        if i >= 2:
            delta = df.loc[i-1, base_projector] - df.loc[i-2, base_projector]
            projectile=delta+df.loc[i-1, base_projector]
            df.loc[i, 'ema8_1day_projectile'] = projectile
    
    df['ema21_ma50_gap'] = abs(df['ema21']-df['ma50'])
    df['ema8_ema21_gap'] = abs(df['ema8']-df['ema21'])
    df['ema8_ma50_gap'] = abs(df['ema8']-df['ma50'])
    
    df['ema21_ma50_gap_ma'] = df['ema21_ma50_gap'].rolling(window=3).mean()
    df['ema21_ma50_MACD'] = df['ema21_ma50_gap'] - df['ema21_ma50_gap_ma']
    
    df['ema8_ema21_gap_ma'] = df['ema8_ema21_gap'].rolling(window=3).mean()
    df['ema8_ema21_MACD'] = df['ema8_ema21_gap'] - df['ema8_ema21_gap_ma']
    
    df['macd_positive']=df.apply(lambda row : macd_status(row['ema21_ma50_MACD'], row['high']+10, 'positive'), axis = 1)
    df['macd_negative']=df.apply(lambda row : macd_status(row['ema21_ma50_MACD'], row['high']+10, 'negative'), axis = 1)
    
    # return 'long short_sequence' or 'short_sequence'
    df['sequence_8_21_50']=df.apply(lambda row : sequence_8_21_50(row['ema8'],row['ema21'],row['ma50'],row['ema8_delta'],row['ema21_delta'],row['ma50_delta']), axis = 1)
    df['sequence_8_21_50_strict']=df.apply(lambda row : sequence_8_21_50(row['ema8'],row['ema21'],row['ma50'],row['ema8_delta'],row['ema21_delta'],row['ma50_delta'],strict=True), axis = 1)
    # return 'long short_sequence' or 'short_sequence'
    df['sequence_8_21']=df.apply(lambda row : sequence_8_21(row['ema8'],row['ema21'],row['ema8_delta'],row['ema21_delta']), axis = 1)
    df['sequence_8_21_strict']=df.apply(lambda row : sequence_8_21(row['ema8'],row['ema21'],row['ema8_delta'],row['ema21_delta'],strict=True), axis = 1)
    # return 'long short_sequence' or 'short_sequence', p is price
    df['sequence_p_8_21']=df.apply(lambda row : sequence_p_8_21(row['open'],row['close'],row['ema8'],row['ema21'],row['ma50']), axis = 1)
    
    # return 1 if the given MA is in the range of low and high of candle stick
    df['cover_lh_8']=df.apply(lambda row : cover(row['low'],row['high'],row['ema8']), axis = 1)
    df['cover_lh_21']=df.apply(lambda row : cover(row['low'],row['high'],row['ema21']), axis = 1)
    
    df['sequence_p_8_21']=df.apply(lambda row : sequence_p_8_21(row['open'],row['close'],row['ema8'],row['ema21'],row['ma50']), axis = 1)
    
    # UI marker
    # 8_21_50
    df['sequence_8_21_50_short']=df.apply(lambda row : mark_sequence_8_21_50_status(row['sequence_8_21_50'], row['high'], 'short'), axis = 1)
    df['sequence_8_21_50_long']=df.apply(lambda row : mark_sequence_8_21_50_status(row['sequence_8_21_50'], row['high'], 'long'), axis = 1)
    df['sequence_8_21_50_na']=df.apply(lambda row : mark_sequence_8_21_50_status(row['sequence_8_21_50'], row['high'], 'na'), axis = 1)
    
    # 8_21
    df['sequence_8_21_short']=df.apply(lambda row : mark_sequence_8_21_status(row['sequence_8_21'], row['high'], 'short'), axis = 1)
    df['sequence_8_21_long']=df.apply(lambda row : mark_sequence_8_21_status(row['sequence_8_21'], row['high'], 'long'), axis = 1)
    df['sequence_8_21_na']=df.apply(lambda row : mark_sequence_8_21_status(row['sequence_8_21'], row['high'], 'na'), axis = 1)
    
    # p_8_21
    df['sequence_p_8_21_short']=df.apply(lambda row : mark_sequence_p_8_21_status(row['sequence_p_8_21'], row['high'], 'short'), axis = 1)
    df['sequence_p_8_21_long']=df.apply(lambda row : mark_sequence_p_8_21_status(row['sequence_p_8_21'], row['high'], 'long'), axis = 1)
    
    # % difference between price bar middle and ema8
    df['ema8_p_distance %'] = ((df['low']+df['high']) / 2 - df['ema8']) / df['ema8']
    df['ema8_v'] = abs((df['ema8'] - df['ema8'].shift(5)) / df['ema8'])
    
    # how many bars has it kept being long or short
    df['consecutive_sequence_8_21_cnt'] = 0
    df['high_open_p'] = (abs(df['high'] - df['open']))/df['open']
    df['low_open_p'] = (abs(df['low'] - df['open']))/df['open']
    
    # channel indicator section bar low
    df['barlow_2_ema8'] = df.apply(lambda row : row['close'] - row['ema8'] if row['close'] < row['open'] else row['open'] - row['ema8'], axis = 1)
      
    barlow_2_ema8_channel_min = 999999
    barlow_2_ema8_channel_max = -999999
      
    df["barlow_2_ema8_channel_min"] = np.nan
    df["barlow_2_ema8_channel_max"] = np.nan
    df["barlow_2_ema8_channel_floor"] = np.nan
    df["barlow_2_ema8_channel_ceiling"] = np.nan
    df["barlow_2_ema8_channel_mp25_pos"] = np.nan
    df["barlow_2_ema8_channel_mp50_pos"] = np.nan
    df["barlow_2_ema8_channel_mp75_pos"] = np.nan
    history = []
    for i in range(0, len(df)):
        date = df.loc[i, 'date']
        if df.loc[i, 'sequence_8_21_50'] == 'long_sequence':
            barlow_2_ema8 = df.loc[i, 'barlow_2_ema8']
            if barlow_2_ema8 > barlow_2_ema8_channel_max:
                barlow_2_ema8_channel_max = barlow_2_ema8
            if barlow_2_ema8 < barlow_2_ema8_channel_min:
                barlow_2_ema8_channel_min = barlow_2_ema8
            df.loc[i, 'barlow_2_ema8_channel_min'] = barlow_2_ema8_channel_min
            df.loc[i, 'barlow_2_ema8_channel_max'] = barlow_2_ema8_channel_max
            bisect.insort(history, barlow_2_ema8)
#             df.loc[i, 'barlow_history'] = ','.join(str(x) for x in history)
            # index is from 0 to len(history) - 1
            p25 = int(len(history) * 0.25)
            p50 = int(len(history) * 0.5)
            p75 = int(len(history) * 0.75)
            df.loc[i, 'barlow_2_ema8_channel_mp25'] = history[p25]
            df.loc[i, 'barlow_2_ema8_channel_mp50'] = history[p50]
            df.loc[i, 'barlow_2_ema8_channel_mp75'] = history[p75]
              
            # UI 
            df.loc[i, 'barlow_2_ema8_channel_floor'] = df.loc[i, 'barlow_2_ema8_channel_min'] + df.loc[i, 'ema8']
            df.loc[i, 'barlow_2_ema8_channel_ceiling'] = df.loc[i, 'barlow_2_ema8_channel_max'] + df.loc[i, 'ema8']   
            df.loc[i, 'barlow_2_ema8_channel_mp25_pos'] = df.loc[i, 'barlow_2_ema8_channel_mp25'] + df.loc[i, 'ema8']            
            df.loc[i, 'barlow_2_ema8_channel_mp50_pos'] = df.loc[i, 'barlow_2_ema8_channel_mp50'] + df.loc[i, 'ema8']    
            df.loc[i, 'barlow_2_ema8_channel_mp75_pos'] = df.loc[i, 'barlow_2_ema8_channel_mp75'] + df.loc[i, 'ema8']    
        else:
            barlow_2_ema8_channel_min = 999999
            barlow_2_ema8_channel_max = -999999
            history = []
#             
# 
#     # channel indicator section bar high
#     df['barhigh_2_ema8'] = df.apply(lambda row : row['close'] - row['ema8'] if row['close'] > row['open'] else row['open'] - row['ema8'], axis = 1)
#     
#     barhigh_2_ema8_channel_min = 999999
#     barhigh_2_ema8_channel_max = -999999
#     
#     df["barhigh_2_ema8_channel_min"] = np.nan
#     df["barhigh_2_ema8_channel_max"] = np.nan
#     df["barhigh_2_ema8_channel_floor"] = np.nan
#     df["barhigh_2_ema8_channel_ceiling"] = np.nan
#     df["barhigh_2_ema8_channel_mp25_pos"] = np.nan
#     df["barhigh_2_ema8_channel_mp50_pos"] = np.nan
#     df["barhigh_2_ema8_channel_mp75_pos"] = np.nan
#     history = []
#     for i in range(0, len(df)):
#         if df.loc[i, 'sequence_8_21_50'] == 'long_sequence':
#             barhigh_2_ema8 = df.loc[i, 'barhigh_2_ema8']
#             if barhigh_2_ema8 > barhigh_2_ema8_channel_max:
#                 barhigh_2_ema8_channel_max = barhigh_2_ema8
#             if barhigh_2_ema8 < barhigh_2_ema8_channel_min:
#                 barhigh_2_ema8_channel_min = barhigh_2_ema8
#             df.loc[i, 'barhigh_2_ema8_channel_min'] = barhigh_2_ema8_channel_min
#             df.loc[i, 'barhigh_2_ema8_channel_max'] = barhigh_2_ema8_channel_max
#             bisect.insort(history, barhigh_2_ema8)
# 
#             p25 = int(len(history) * 0.25)
#             p50 = int(len(history) * 0.5)
#             p75 = int(len(history) * 0.75)
#             df.loc[i, 'barhigh_2_ema8_channel_mp25'] = history[p25]
#             df.loc[i, 'barhigh_2_ema8_channel_mp50'] = history[p50]
#             df.loc[i, 'barhigh_2_ema8_channel_mp75'] = history[p75]
#             
#             # UI 
#             df.loc[i, 'barhigh_2_ema8_channel_floor'] = df.loc[i, 'barhigh_2_ema8_channel_min'] + df.loc[i, 'ema8']
#             df.loc[i, 'barhigh_2_ema8_channel_ceiling'] = df.loc[i, 'barhigh_2_ema8_channel_max'] + df.loc[i, 'ema8']   
#             df.loc[i, 'barhigh_2_ema8_channel_mp25_pos'] = df.loc[i, 'barhigh_2_ema8_channel_mp25'] + df.loc[i, 'ema8']            
#             df.loc[i, 'barhigh_2_ema8_channel_mp50_pos'] = df.loc[i, 'barhigh_2_ema8_channel_mp50'] + df.loc[i, 'ema8']    
#             df.loc[i, 'barhigh_2_ema8_channel_mp75_pos'] = df.loc[i, 'barhigh_2_ema8_channel_mp75'] + df.loc[i, 'ema8']    
#         else:
#             barhigh_2_ema8_channel_min = 999999
#             barhigh_2_ema8_channel_max = -999999
#             history = []
#         if i >= 1:
#             df.loc[i, 'ema8_delta'] = df.loc[i, 'ema8'] - df.loc[i-1, 'ema8']
#             df.loc[i, 'ema21_delta'] = df.loc[i, 'ema21'] - df.loc[i-1, 'ema21']
#             df.loc[i, 'ma50_delta'] = df.loc[i, 'ma50'] - df.loc[i-1, 'ma50']
#         if i >= 2:
#             delta = df.loc[i-1, base_projector] - df.loc[i-2, base_projector]
#             projectile=delta+df.loc[i-1, base_projector]
#             df.loc[i, 'ema8_1day_projectile'] = projectile   
            
            
#     temporary disabled: bar count on continues trend
#     for i in range(1, len(df)):
#         if df.loc[i, 'sequence_8_21'] is not nan and df.loc[i-1, 'sequence_8_21'] == df.loc[i, 'sequence_8_21']:
#             x = df.loc[i-1, 'consecutive_sequence_8_21_cnt'] + 1
#             df.loc[i, 'consecutive_sequence_8_21_cnt'] = x
#            # debug only, plot for first x continues bar in one direction
#             if x<=2:
#                 df.loc[i, 'consecutive_sequence_8_21_cnt_plot'] = df.loc[i, 'high']
        
    # bar low one year, ma 21
    # channel indicator section bar low
    df['barlow_2_ema21'] = df.apply(lambda row : row['close'] - row['ema21'] if row['close'] < row['open'] else row['open'] - row['ema21'], axis = 1)
    df['barlow_2_ema21_percent'] = df['barlow_2_ema21'] / df['ema21'] 
    df['barlow_2_ema21_percent_oneyear_channel_percentile'] = np.nan
    df['barlow_2_ema21_percent_oneyear_channel_100'] = np.nan
    df['barlow_2_ema21_percent_oneyear_channel_75'] = np.nan
    df['barlow_2_ema21_percent_oneyear_channel_50'] = np.nan
    df['barlow_2_ema21_percent_oneyear_channel_25'] = np.nan
    df['barlow_2_ema21_percent_oneyear_channel_0'] = np.nan
    # pan jian
 
 
    queue_dt = []
    queue_val = []
    for i in range(0, len(df)):
        if i == 0:
            continue
         
        yesterday = df.loc[i-1, 'date']
        dt_object = datetime.strptime(yesterday, '%Y-%m-%d')
        val = df.loc[i, 'barlow_2_ema21_percent']
        bar_yesterday = df.loc[i-1]
        all_ma_upward = all_ma_upwards("21_50", bar_yesterday)
        macd_green = macd("21_50", bar_yesterday)
        ma_sequence = ma_enter_sequence("21_50", bar_yesterday)
         
        # skip not in condition
        record_condition =  ma_sequence and macd_green and all_ma_upward
        if not record_condition:
            continue
 
        df.loc[i, 'enter_ui'] = df.loc[i, 'open']
         
 
        queue_dt.append(dt_object)
        queue_val.append(val)
         
        # the queue only keep one year of data
        while dt_object - timedelta(days=253) > queue_dt[0]:
            queue_dt.pop(0)
            queue_val.pop(0)
             
        queue_val_sorted = queue_val.copy()
        queue_val_sorted.sort()
         
        # ui assist
        total = len(queue_val_sorted)
        p50 = int(total*0.5)
        p25 = int(total*0.25)
        p75 = int(total*0.75)
#         if i > 30:
        df.loc[i, 'barlow_2_ema21_percent_oneyear_channel_100'] = (1+queue_val_sorted[total-1]) * df.loc[i, 'ema21']
        df.loc[i, 'barlow_2_ema21_percent_oneyear_channel_75'] = (1+queue_val_sorted[p75]) * df.loc[i, 'ema21']
        df.loc[i, 'barlow_2_ema21_percent_oneyear_channel_50'] = (1+queue_val_sorted[p50]) * df.loc[i, 'ema21']
        df.loc[i, 'barlow_2_ema21_percent_oneyear_channel_25'] = (1+queue_val_sorted[p25]) * df.loc[i, 'ema21']
        df.loc[i, 'barlow_2_ema21_percent_oneyear_channel_0'] = (1+queue_val_sorted[0]) * df.loc[i, 'ema21']
 
        # percentile
        price_ema21_gap = df.loc[i, 'open'] /  df.loc[i, 'ema21'] - 1
        idx = bisect_left(queue_val_sorted, price_ema21_gap)
        percentile = idx * 1.0 / len(queue_val_sorted)
        df['barlow_2_ema21_percent_oneyear_channel_percentile'] = percentile
        

    # velocity: open-close, 1 day, 2 days, 3 days, 4 days, 5 days, 10 days, 20 days. 
    # Absolute price delta and % change compared to close price now
#     df['p_delta_oc'] = np.nan
#     df['p_delta_1d'] = np.nan
#     df['p_delta_2d'] = np.nan
#     df['p_delta_3d'] = np.nan
#     df['p_delta_4d'] = np.nan
#     df['p_delta_5d'] = np.nan
#     df['p_delta_10d'] = np.nan
#     df['p_delta_20d'] = np.nan
#      
#     df['p_delta_oc_pct'] = np.nan
#     df['p_delta_1d_pct'] = np.nan
#     df['p_delta_2d_pct'] = np.nan
#     df['p_delta_3d_pct'] = np.nan
#     df['p_delta_4d_pct'] = np.nan
#     df['p_delta_5d_pct'] = np.nan
#     df['p_delta_10d_pct'] = np.nan
#     df['p_delta_20d_pct'] = np.nan
#          
#     for i in range(0, len(df)):
#         df.loc[i, 'p_delta_oc'] = df.loc[i, 'close'] - df.loc[i, 'open']
#         df.loc[i, 'p_delta_oc_pct'] = df.loc[i, 'p_delta_oc'] / df.loc[i, 'close']
#          
#         if i > 0:
#             df.loc[i, 'p_delta_1d'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
#             df.loc[i, 'p_delta_1d_pct'] = df.loc[i, 'p_delta_1d'] / df.loc[i, 'close']    
#              
#         if i > 1:
#             df.loc[i, 'p_delta_2d'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
#             df.loc[i, 'p_delta_2d_pct'] = df.loc[i, 'p_delta_2d'] / df.loc[i, 'close']    
#              
#         if i > 2:
#             df.loc[i, 'p_delta_3d'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
#             df.loc[i, 'p_delta_3d_pct'] = df.loc[i, 'p_delta_3d'] / df.loc[i, 'close']   
#              
#         if i > 4:
#             df.loc[i, 'p_delta_5d'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
#             df.loc[i, 'p_delta_5d_pct'] = df.loc[i, 'p_delta_5d'] / df.loc[i, 'close']    
#                 
#         if i > 9:
#             df.loc[i, 'p_delta_10d'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
#             df.loc[i, 'p_delta_10d_pct'] = df.loc[i, 'p_delta_10d'] / df.loc[i, 'close']  
#              
#         if i > 19:
#             df.loc[i, 'p_delta_20d'] = df.loc[i, 'close'] - df.loc[i - 1, 'close']
#             df.loc[i, 'p_delta_20d_pct'] = df.loc[i, 'p_delta_20d'] / df.loc[i, 'close']  
#  
#     df['velocity_ui'] = df.apply(lambda row : threshold_display(row['p_delta_1d_pct'], -999, -0.01, row['high']), axis = 1) 
#   
#     # volocity start ################################################################################################################   
#     for i in range(0, len(df)):
#         if i >= 10:
#             df.loc[i, 'v_p_3d'] = (df.loc[i, 'open'] - df.loc[i-3, 'open']) * 1.0 / df.loc[i-3, 'open']
#             df.loc[i, 'v_p_1w'] = (df.loc[i, 'open'] - df.loc[i-5, 'open']) * 1.0 / df.loc[i-5, 'open']
#             df.loc[i, 'v_p_2w'] = (df.loc[i, 'open'] - df.loc[i-10, 'open']) * 1.0 / df.loc[i-10, 'open']
#  
#     for i in range(0, len(df)-12):
#         if i >= 10:
#             df.loc[i, 'delta_p_3d'] = (df.loc[i+3, 'open'] - df.loc[i, 'open']) * 1.0 / df.loc[i, 'open']
#             df.loc[i, 'delta_p_1w'] = (df.loc[i+5, 'open'] - df.loc[i, 'open']) * 1.0 / df.loc[i, 'open']
#             df.loc[i, 'delta_p_2w'] = (df.loc[i+10, 'open'] - df.loc[i, 'open']) * 1.0 / df.loc[i, 'open']
#  
#     for i in range(3, len(df)-4):
#         df.loc[i, 'ema8_local_min'] = 0
#         if df.loc[i-2, 'ema8'] > df.loc[i-1, 'ema8'] and df.loc[i-1, 'ema8'] > df.loc[i, 'ema8'] and df.loc[i, 'ema8'] < df.loc[i+1, 'ema8'] and df.loc[i+1, 'ema8'] < df.loc[i+2, 'ema8']:
#             df.loc[i, 'ema8_local_min'] = 1
#   
#         df.loc[i, 'ema8_ma50_gap_local_min'] = 0
#         if df.loc[i-2, 'ema8_ma50_gap'] > df.loc[i-1, 'ema8_ma50_gap'] and df.loc[i-1, 'ema8_ma50_gap'] > df.loc[i, 'ema8_ma50_gap'] and df.loc[i, 'ema8_ma50_gap'] < df.loc[i+1, 'ema8_ma50_gap'] and df.loc[i+1, 'ema8_ma50_gap'] < df.loc[i+2, 'ema8_ma50_gap']:
#             df.loc[i, 'ema8_ma50_gap_local_min'] = 1
#  
#         df.loc[i, 'ema21_local_min'] = 0
#         if df.loc[i-2, 'ema21'] > df.loc[i-1, 'ema21'] and df.loc[i-1, 'ema21'] > df.loc[i, 'ema21'] and df.loc[i, 'ema21'] < df.loc[i+1, 'ema21'] and df.loc[i+1, 'ema21'] < df.loc[i+2, 'ema21']:
#             df.loc[i, 'ema21_local_min'] = 1
#              
#         df.loc[i, 'ema21_ma50_gap_local_min'] = 0
#         if df.loc[i-2, 'ema21_ma50_gap'] > df.loc[i-1, 'ema21_ma50_gap'] and df.loc[i-1, 'ema21_ma50_gap'] > df.loc[i, 'ema21_ma50_gap'] and df.loc[i, 'ema21_ma50_gap'] < df.loc[i+1, 'ema21_ma50_gap'] and df.loc[i+1, 'ema21_ma50_gap'] < df.loc[i+2, 'ema21_ma50_gap']:
#             df.loc[i, 'ema21_ma50_gap_local_min'] = 1
#  
#         df.loc[i, 'ema21_ma50_upcross'] = 0
#         if df.loc[i, 'ema21'] > df.loc[i, 'ma50'] and df.loc[i-1, 'ema21'] < df.loc[i-1, 'ma50'] :
#             df.loc[i, 'ema21_ma50_upcross'] = 1
#  
#  
#     for i in range(10, len(df)-2):
#         df.loc[i, 'ma_upcross_in_past_3days'] = 0
#         if df.loc[i, 'ema21_ma50_upcross'] == 1 or df.loc[i-1, 'ema21_ma50_upcross'] == 1 or df.loc[i-2, 'ema21_ma50_upcross'] == 1 or df.loc[i-3, 'ema21_ma50_upcross'] == 1:
#             df.loc[i, 'ma_upcross_in_past_3days'] = 1
#              
#         df.loc[i, 'ma_gap_reverse_in_past_6days'] = 0
#         if df.loc[i-1, 'ema21_ma50_gap_local_min'] == 1 or df.loc[i-2, 'ema21_ma50_gap_local_min'] == 1 or df.loc[i-3, 'ema21_ma50_gap_local_min'] == 1 or df.loc[i-4, 'ema21_ma50_gap_local_min'] == 1 or df.loc[i-5, 'ema21_ma50_gap_local_min'] == 1 or df.loc[i-6, 'ema21_ma50_gap_local_min'] == 1:
#             df.loc[i, 'ma_gap_reverse_in_past_6days'] = 1
#  
#         df.loc[i, 'ma21_local_min_in_past_6days'] = 0
#         if df.loc[i-1, 'ema21_local_min'] == 1 or df.loc[i-2, 'ema21_local_min'] == 1 or df.loc[i-3, 'ema21_local_min'] == 1 or df.loc[i-4, 'ema21_local_min'] == 1 or df.loc[i-5, 'ema21_local_min'] == 1 or df.loc[i-6, 'ema21_local_min'] == 1:
#             df.loc[i, 'ma21_local_min_in_past_6days'] = 1


    #drop price bar without MA or incomplete price bar
    df.dropna(subset=['ema8'], inplace=True)
    df.dropna(subset=['open'], inplace=True)
    df.dropna(subset=['high'], inplace=True)
    df.dropna(subset=['close'], inplace=True)
    df.dropna(subset=['low'], inplace=True)
    
    ################################# add seperate feature indicator #############################
    get_velocity_one_bar_on_close(df)
    get_down_from_peak(df)
    # experiment indicator 20220227 - delete after run
    get_velocity_pct_on_metric(df=df, metric='ema21', bar_range=3, feature_col='v_ema21_3')
    
    
def datefilter(df,s,e):
    df = df.loc[(df['date']>=s) & (df['date']<=e)]
    df_filtered = df.copy()
    return df_filtered

def tsfilter(df,s,e):
    df2 = df.loc[(df['est_datetime']>=s) & (df['est_datetime']<=e)]
    df2.reset_index(drop=True, inplace=True)
    return df2

def unixtsfilter(df,s,e):
    s_ts = datetime.timestamp(datetime.strptime(s,"%Y-%m-%d %H:%M:%S")) 
    e_ts = datetime.timestamp(datetime.strptime(e,"%Y-%m-%d %H:%M:%S")) 
    df2 = df.loc[(df['time']>=s_ts) & (df['time']<=e_ts)]
    return df2
    
def cover(lower_bound, upper_bound, target):
    if lower_bound <= target and upper_bound >= target:
        return 1
    else:
        return 0

def sequence_8_21_50(ema8, ema21, ma50, ema8_delta, ema21_delta, ma50_delta, strict=False):
    if not strict:
        if ma50 > ema21 and ema21 > ema8:
            return 'short_sequence'
        if ma50 < ema21 and ema21 < ema8:
            return 'long_sequence'
        return 'na'
    else:
        if ma50 > ema21 and ema21 > ema8 and ema8_delta<=0 and ema21_delta<=0 and ma50_delta<=0:
            return 'short_sequence'
        if ma50 < ema21 and ema21 < ema8 and ema8_delta>=0 and ema21_delta>=0 and ma50_delta>=0:
            return 'long_sequence'
        return 'na'
    
def sequence_8_21(ema8, ema21, ema8_delta, ema21_delta, strict=False):
    if not strict:
        if  ema21 > ema8 and ema21_delta<=0:
            return 'short_sequence'
        if  ema21 < ema8 and ema21_delta>=0:
            return 'long_sequence'
        return 'na'
    else: # strict, all line must has same gradient direction
        if  ema21 > ema8 and ema21_delta<=0 and ema8_delta<=0:
            return 'short_sequence'
        if  ema21 < ema8 and ema21_delta>=0 and ema8_delta>=0:
            return 'long_sequence'
        return 'na'
    
def sequence_p_8_21(open, close, ema8, ema21, ma50):
    if  ema21 > ema8 and ema8 > max(open, close):
        return 'short_sequence'
    if  ema21 < ema8 and ema8 < min(open, close):
        return 'long_sequence'
    
def macd_status(macd, mark_position, status):
    if status == 'positive':
        if macd > 0:
            return mark_position
    elif status == 'negative':
        if macd < 0:
            return mark_position  

def mark_sequence_8_21_50_status(sequence_8_21_50, mark_position, status):
    if status == 'long':
        if sequence_8_21_50 == 'long_sequence':
            return mark_position
    elif status == 'short':
        if sequence_8_21_50 == 'short_sequence':
            return mark_position  
    elif status == 'na':
        if sequence_8_21_50 != 'short_sequence' and sequence_8_21_50 != 'long_sequence':
            return mark_position  
                
def mark_sequence_8_21_status(sequence_8_21, mark_position, status):
    if status == 'long':
        if sequence_8_21 == 'long_sequence':
            return mark_position
    elif status == 'short':
        if sequence_8_21 == 'short_sequence':
            return mark_position  
    elif status == 'na':
        if sequence_8_21 != 'short_sequence' and sequence_8_21 != 'long_sequence':
            return mark_position  

def mark_sequence_p_8_21_status(sequence_p_8_21, mark_position, status):
    if status == 'long':
        if sequence_p_8_21 == 'long_sequence':
            return mark_position
    elif status == 'short':
        if sequence_p_8_21 == 'short_sequence':
            return mark_position  

def mark_gap_ema_20_50_delta(delta, mark_position, up):
    if up:
        if delta >0:
            return mark_position
        
    else:
        if delta < 0:
            return mark_position
        
def mark_shrink_block(should_mark,price):
    if should_mark == 1:
        return price
   
def mark_ribbon_expand(num, seq, price):
    if num == seq:
        return price 
    

def threshold_display(target, low, up, ui):
    if target >=low and target <= up:
        return ui
    else: 
        return np.nan
    

def load_df_add_indicator(filepath, start_time, end_time):
    df = load_df_from_csv(filepath)
    add_indicator(df)
    df_range = datefilter(df, start_time, end_time)
    print('df loading, indicator done!')
    return df_range




############################################## test ###################################################
# path_test = """D:/f_data/BITSTAMP_BTCUSD, 60.csv"""
# df = load_df_from_csv(path_test)
# add_indicator(df)
# print(df)
############################################## test ###################################################

