'''
Created on Jun 4, 2020

@author: leon
'''
from datetime import datetime
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
from cmath import nan

# This library add indicator to each bar, input df should has the following interface: see global_constant file

def add_indicator(df):
    # meta info
    df['est_datetime']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d %H:%M:%S'), axis = 1)
    df['date']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d'), axis = 1)
    df['est_time']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%H:%M:%S'), axis = 1)
    
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

#     temporary disabled: bar count on continues trend
#     for i in range(1, len(df)):
#         if df.loc[i, 'sequence_8_21'] is not nan and df.loc[i-1, 'sequence_8_21'] == df.loc[i, 'sequence_8_21']:
#             x = df.loc[i-1, 'consecutive_sequence_8_21_cnt'] + 1
#             df.loc[i, 'consecutive_sequence_8_21_cnt'] = x
#            # debug only, plot for first x continues bar in one direction
#             if x<=2:
#                 df.loc[i, 'consecutive_sequence_8_21_cnt_plot'] = df.loc[i, 'high']
        


    #drop price bar without MA or incomplete price bar
    df.dropna(subset=['ema8'], inplace=True)
    df.dropna(subset=['open'], inplace=True)
    df.dropna(subset=['high'], inplace=True)
    df.dropna(subset=['close'], inplace=True)
    df.dropna(subset=['low'], inplace=True)
    
def datefilter(df,s,e):
    df2 = df.loc[(df['date']>=s) & (df['date']<=e)]
    return df2

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
    if status is 'positive':
        if macd > 0:
            return mark_position
    elif status is 'negative':
        if macd < 0:
            return mark_position  

def mark_sequence_8_21_50_status(sequence_8_21_50, mark_position, status):
    if status is 'long':
        if sequence_8_21_50 is 'long_sequence':
            return mark_position
    elif status is 'short':
        if sequence_8_21_50 is 'short_sequence':
            return mark_position  
    elif status is 'na':
        if sequence_8_21_50 is not 'short_sequence' and sequence_8_21_50 is not 'long_sequence':
            return mark_position  
                
def mark_sequence_8_21_status(sequence_8_21, mark_position, status):
    if status is 'long':
        if sequence_8_21 is 'long_sequence':
            return mark_position
    elif status is 'short':
        if sequence_8_21 is 'short_sequence':
            return mark_position  
    elif status is 'na':
        if sequence_8_21 is not 'short_sequence' and sequence_8_21 is not 'long_sequence':
            return mark_position  

def mark_sequence_p_8_21_status(sequence_p_8_21, mark_position, status):
    if status is 'long':
        if sequence_p_8_21 is 'long_sequence':
            return mark_position
    elif status is 'short':
        if sequence_p_8_21 is 'short_sequence':
            return mark_position  


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

