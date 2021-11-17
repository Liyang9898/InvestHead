from datetime import datetime
import pandas as pd


def load_df(filepath):
    path = filepath
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=['time', 'open','high','low','close','ma200','ma50','ema21','ema8']
    )
    return df

def add_indicator(df):
    df['est_datetime']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d %H:%M:%S'), axis = 1)
    df['date']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%Y-%m-%d'), axis = 1)
    df['est_time']=df.apply(lambda row : datetime.fromtimestamp(int(row['time'])).strftime('%H:%M:%S'), axis = 1)
    # return 'long short_sequence' or 'short_sequence'
    df['sequence_8_21_50']=df.apply(lambda row : sequence_8_21_50(row['ema8'],row['ema21'],row['ma50']), axis = 1)
    # return 'long short_sequence' or 'short_sequence'
    df['sequence_8_21']=df.apply(lambda row : sequence_8_21(row['ema8'],row['ema21'],row['ma50']), axis = 1)
    # return 'long short_sequence' or 'short_sequence', p is price
    df['sequence_p_8_21']=df.apply(lambda row : sequence_p_8_21(row['open'],row['close'],row['ema8'],row['ema21'],row['ma50']), axis = 1)
    
    # UI marker
    # 8_21_50
    df['sequence_8_21_50_short']=df.apply(lambda row : mark_sequence_8_21_50_status(row['sequence_8_21_50'], row['high'], 'short'), axis = 1)
    df['sequence_8_21_50_long']=df.apply(lambda row : mark_sequence_8_21_50_status(row['sequence_8_21_50'], row['high'], 'long'), axis = 1)
    
    # 8_21
    df['sequence_8_21_short']=df.apply(lambda row : mark_sequence_8_21_status(row['sequence_8_21'], row['high'], 'short'), axis = 1)
    df['sequence_8_21_long']=df.apply(lambda row : mark_sequence_8_21_status(row['sequence_8_21'], row['high'], 'long'), axis = 1)
    
    # p_8_21
    df['sequence_p_8_21_short']=df.apply(lambda row : mark_sequence_p_8_21_status(row['sequence_p_8_21'], row['high'], 'short'), axis = 1)
    df['sequence_p_8_21_long']=df.apply(lambda row : mark_sequence_p_8_21_status(row['sequence_p_8_21'], row['high'], 'long'), axis = 1)
    
    # % difference between price bar middle and ema8
    df['ema8_p_distance %'] = ((df['low']+df['high']) / 2 - df['ema8']) / df['ema8']
    df['ema8_v'] = abs((df['ema8'] - df['ema8'].shift(5)) / df['ema8'])
    
    #drop price bar without MA or incomplete price bar
    df.dropna(subset=['ema8'], inplace=True)
    df.dropna(subset=['open'], inplace=True)
    df.dropna(subset=['high'], inplace=True)
    df.dropna(subset=['close'], inplace=True)
    df.dropna(subset=['low'], inplace=True)
    
    
def datefilter(df,s,e):
    df2 = df.loc[(df['date']>=s) & (df['date']<=e)]
    return df2
    
def sequence_8_21_50(ema8, ema21, ma50):
    if ma50 > ema21 and ema21 > ema8:
        return 'short_sequence'
    if ma50 < ema21 and ema21 < ema8:
        return 'long_sequence'
    
def sequence_8_21(ema8, ema21, ma50):
    if  ema21 > ema8:
        return 'short_sequence'
    if  ema21 < ema8:
        return 'long_sequence'
    
def sequence_p_8_21(open, close, ema8, ema21, ma50):
    if  ema21 > ema8 and ema8 > max(open, close):
        return 'short_sequence'
    if  ema21 < ema8 and ema8 < min(open, close):
        return 'long_sequence'
    
def mark_sequence_8_21_50_status(sequence_8_21_50, mark_position, status):
    if status is 'long':
        if sequence_8_21_50 is 'long_sequence':
            return mark_position
    elif status is 'short':
        if sequence_8_21_50 is 'short_sequence':
            return mark_position  
        
def mark_sequence_8_21_status(sequence_8_21, mark_position, status):
    if status is 'long':
        if sequence_8_21 is 'long_sequence':
            return mark_position
    elif status is 'short':
        if sequence_8_21 is 'short_sequence':
            return mark_position  

def mark_sequence_p_8_21_status(sequence_p_8_21, mark_position, status):
    if status is 'long':
        if sequence_p_8_21 is 'long_sequence':
            return mark_position
    elif status is 'short':
        if sequence_p_8_21 is 'short_sequence':
            return mark_position  


def load_df_add_indicator(filepath, start_time, end_time):
    df = load_df(filepath)
    add_indicator(df)
    df_range = datefilter(df, start_time, end_time)
    print('df loading, indicator done!')
    return df_range

# test
path_test = """D:/f_data/BITSTAMP_BTCUSD, 60.csv"""
df = load_df(path_test)
add_indicator(df)
print(df)

