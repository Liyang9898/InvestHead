from datetime import datetime, timedelta
import pandas as pd
import math

def point_five_percent_bucket(x):

    if math.isnan(x):
        return x
    return int(x * 200)/200


def gen_label(pnl_percent):
    label = 1 if pnl_percent>0 else -1
    return label


def gen_win(pnl_percent):
    label = 1 if pnl_percent>0 else 0
    return label


def holding_days(start, end):
    start = start.split(' ')[0]
    end = end.split(' ')[0]
    s_dt = datetime.strptime(start, '%Y-%m-%d')
    e_dt = datetime.strptime(end, '%Y-%m-%d')
    cnt = 0
    while e_dt > s_dt:
        # if e_dt is weekend, add count
        if e_dt.weekday() < 5: 
            cnt = cnt + 1
        # move to previous day
        e_dt = e_dt - timedelta(days=1)

    return cnt 
        
        
def gen_feature_on_trade_entry(df):
    df['label'] = df.apply(lambda row : gen_label(row['pnl_percent']), axis = 1) 
    df['win'] = df.apply(lambda row : gen_win(row['pnl_percent']), axis = 1)  
    df['entry_price_ma50_gap'] = df['entry_price'] / df['ma50'] - 1
    df['entry_price_ma50_gap_percent_bucket'] = round(df['entry_price_ma50_gap'], 2)
    df['ema21_price_channel_bucket'] = round(df['barlow_2_ema21_percent_oneyear_channel_percentile'], 2)
    df['hold_days'] = df.apply(lambda row : holding_days(row['entry_ts'], row['exit_ts']), axis = 1) 
    df['gap_ema21_ma50'] = df['ema21'] / df['ma50'] - 1
    df['gap_ema21_ma50_half_percent_bucket'] = df.apply(lambda row : point_five_percent_bucket(row['gap_ema21_ma50']), axis = 1) 
    return df


def gen_feature_on_entire_trade_batch(ticker, trades_with_entry_day_feature, df_indicator):
    df_trades = trades_with_entry_day_feature

    # generate feature for every trade
    df_trades['ma50_negative_cnt'] = 0
    df_trades['total_21_50_gap_shrink'] = 0
    df_trades['longest_21_50_gap_shrink'] = 0
    df_trades['exitable_after_ma50_negative'] = 0
    for i in range(0, len(df_trades)):
        df_trade = df_trades.iloc[[i]]
        feature_one_trade = gen_feature_on_entire_trade_single_trade(ticker, df_trade, df_indicator)
        assert feature_one_trade['total_21_50_gap_shrink']>=feature_one_trade['longest_21_50_gap_shrink']
        df_trades.loc[i,'ma50_negative_cnt'] = feature_one_trade['ma50_negative_cnt']
        df_trades.loc[i,'total_21_50_gap_shrink'] = feature_one_trade['total_21_50_gap_shrink']
        df_trades.loc[i,'longest_21_50_gap_shrink'] = feature_one_trade['longest_21_50_gap_shrink']
        df_trades.loc[i,'exitable_after_ma50_negative'] = feature_one_trade['exitable_after_ma50_negative']
        df_trades.loc[i,'total_21_50_gap_shrink_percent'] = feature_one_trade['total_21_50_gap_shrink_percent']
        df_trades.loc[i,'chance_neutralout_after_70p_shrink'] = feature_one_trade['chance_neutralout_after_70p_shrink']
        
    return df_trades

def gen_feature_on_entire_trade_single_trade(ticker, df_trade, df_indicator):
    trade = df_trade.iloc[0]
    s = trade['entry_ts'].split(' ')[0]
    e = trade['exit_ts'].split(' ')[0]

    df_indicator_filtered = df_indicator.loc[(df_indicator['date'] >= s) & (df_indicator['date'] <= e)]
    df_indicator_filtered.reset_index(drop=True,inplace=True)
    
    gap_21_50_pre = 0
    ma50_pre = 0
    gap_21_50_delta =0
    ma50_delta = 0

    ma50_negative_cnt = 0
    total_21_50_gap_shrink = 0
    longest_21_50_gap_shrink = 0
    cur_21_50_gap_shrink = 0
    
    # try to exit on enter price after ma50 become negative
    exitable_after_ma50_negative = 0 # until now no need to exit on enter
    holding_days = len(df_indicator_filtered) - 1
    
    exitable_after_70p_shrink = -1
    seeking70p_shrink_neutral_exit = False
    
    
    for i in range(0, len(df_indicator_filtered)):
        today_idc = df_indicator_filtered.iloc[i]
        
        # prepare data               
        ma50 = today_idc['ma50']
        ema21 = today_idc['ema21']
        gap_21_50 = ema21 - ma50

        # compute delta
        if i > 0:
            gap_21_50_delta = gap_21_50 - gap_21_50_pre
            ma50_delta = ma50 - ma50_pre
            
            # generate feature
            if ma50_delta < 0:
                ma50_negative_cnt = ma50_negative_cnt + 1
            if gap_21_50_delta <= 0: # gap shrinking
                total_21_50_gap_shrink = total_21_50_gap_shrink + 1
                cur_21_50_gap_shrink = cur_21_50_gap_shrink + 1
            else: # gap expanding
                if longest_21_50_gap_shrink < cur_21_50_gap_shrink:
                    longest_21_50_gap_shrink = cur_21_50_gap_shrink
                cur_21_50_gap_shrink = 0
            
            # you need start to think about exit at enter price
            if exitable_after_ma50_negative == 0 and ma50_negative_cnt > 0: 
                exitable_after_ma50_negative = -1
            
            # try to find neutral exit price
            if exitable_after_ma50_negative == -1:
                low = today_idc['low']
                high = today_idc['high']
                if trade['entry_price'] >= low and trade['entry_price'] <= high:
                    exitable_after_ma50_negative = 1
        
            # check percent shrink
            if not seeking70p_shrink_neutral_exit:
                percent_shrink = total_21_50_gap_shrink / i
                if percent_shrink >= 0.7:
                    seeking70p_shrink_neutral_exit = True
                    exitable_after_70p_shrink = 0
        
            if seeking70p_shrink_neutral_exit:
                if today_idc['high'] > trade['entry_price']:
                    exitable_after_70p_shrink = 1
                    
        # set previous
        gap_21_50_pre = gap_21_50
        ma50_pre = ma50
        
    total_21_50_gap_shrink_percent = total_21_50_gap_shrink * 1.0 / holding_days
    total_21_50_gap_shrink_percent = round(total_21_50_gap_shrink_percent, 2)
    return {
        'ma50_negative_cnt':ma50_negative_cnt,
        'total_21_50_gap_shrink':total_21_50_gap_shrink,
        'longest_21_50_gap_shrink':longest_21_50_gap_shrink,
        # if ma50 always positive, that require price during the holding should always > price 50 days ago
        'exitable_after_ma50_negative':exitable_after_ma50_negative,
        'holding_days': holding_days,
        'total_21_50_gap_shrink_percent': total_21_50_gap_shrink_percent,
        'chance_neutralout_after_70p_shrink': exitable_after_70p_shrink
    }