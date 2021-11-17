from datetime import datetime
from unittest.mock import inplace

from batch_20201214.analysis.extract_summary import fix
import pandas as pd
import plotly.express as px
from util.util import get_all_weekdays  
from version_master.version import (
#     trade_swing_2150in_2150out_20210302_iwf_channel,
    trade_swing_2150in_2150out_20210227_iwf,
#     trade_swing_2150in_2150out_20210302_iwf_trend_start,
    trade_swing_2150in_2150out_20210310_iwf_channel_in,
    trade_swing_2150in_2150out_20210310_iwf_channel_out,
    trade_swing_2150in_2150out_20210310_iwf_channel_inout,
    trade_swing_2150in_2150out_20210313_iwf_50up,
    trade_swing_2150in_2150out_20210313_iwf,
    
    t_20210314_iwf_ma50up_channel_out,
    t_20210314_iwf_ma50up_channel_inout,
    
    t_20210321_myswing_20210321,
    t_20210321_myswing,
    t_20210404_myswing_4percent_out,
    t_20210404_myswing,
    t_20210418_myswing,
    t_20210420_ema21_ma50_gap_per_ticker,
    t_20210425_ema21_ma50_gap_per_ticker_4p_out
)


# from util.util import get_all_weekdays
# 
# # 
# trade_path=t_20210425_ema21_ma50_gap_per_ticker_4p_out
# track_id = 1
# price_in_track_path = trade_path + """merge/cash_history_reuse_price_in_track.csv"""
# price_df = pd.read_csv(price_in_track_path)
# print(price_df)
# price_df = price_df[price_df['track_id']==track_id]
# price_df = price_df.sort_values(by=['date']).reset_index(drop = True)
# price_df.to_csv('D:/f_data/temp/c1.csv')
# print(price_df)
# 
# trades_in_track_path = trade_path + """merge/cash_history_reuse_trades_in_track.csv"""
# trades_df = pd.read_csv(trades_in_track_path)
# print(trades_df)
# trades_df = trades_df[trades_df['track_id']==track_id]
# 
# trades_df = trades_df.sort_values(by=['entry_ts']).reset_index(drop = True)
# trades_df.to_csv('D:/f_data/temp/c2.csv')
# print(trades_df)
def trade_key(ticker, entry_date):
    # both input are string, data in format 2020-01-01
    return ticker+'|'+entry_date


def get_boundary_split_price_history_by_ticker(price_df):
    # this function split price_df into different chunks
    # each consecutive chunk has the same ticker

    ranges = []
    pre_ticker = 'nothing'
    start = -1

    for i in range(0, len(price_df)): 
        ticker = price_df.loc[i, 'ticker']
        if ticker != pre_ticker:
            warp_previous_up = {'start':start, 'end':i-1}
            if start >=0:
                ranges.append(warp_previous_up)
            start = i
        pre_ticker = ticker
    warp_previous_up = {'start':start, 'end':len(price_df)-1}
    ranges.append(warp_previous_up)
    return ranges
    

def get_dfs_split_price_history_by_ticker(price_df, ranges):

    total_len = 0
    dfs = {}
    for boundary in ranges:
        
        # generate sub df of price
        s = boundary['start']
        e = boundary['end'] + 1
        ids = list(range(s, e))

        sub_df = price_df.iloc[ids, :]
        sub_df = sub_df.reset_index(drop = True)

        # generate meta data for the sub df
        sub_df_len = len(sub_df)
        unique_ticker = sub_df.ticker.unique()
        assert len(unique_ticker) == 1
        sub_ticker = unique_ticker[0]
        sub_start_date = sub_df.loc[0, 'date']
        sub_end_date = sub_df.loc[len(sub_df)-1, 'date']

        total_len += sub_df_len
        
        # store sub df
        key = trade_key(sub_ticker, sub_start_date)
        sub_bundle = {
            'ticker': sub_ticker,
            'start': sub_start_date,
            'end': sub_end_date,
            'df': sub_df
        }
        dfs[key] = sub_bundle
    assert total_len == len(price_df)
    return dfs


def rescale_price_using_trade_position(trades_df, price_df_chunks):
    scaled_dfs = []
    for i in range(0, len(trades_df)): 
        # extract trade meta
        ticker = trades_df.loc[i, 'ticker']
        roll_trade_start_pos = trades_df.loc[i, 'roll_trade_start_pos']
        fix_trade_start_pos = trades_df.loc[i, 'fix_trade_start_pos']
        entry_ts = trades_df.loc[i, 'entry_ts']
        exit_ts = trades_df.loc[i, 'exit_ts']
        
        # get price chunk
        key = trade_key(ticker, entry_ts.split(' ')[0])
        if key not in price_df_chunks.keys():
            continue
        price_chunk = price_df_chunks[key]['df']
        
        # scale
        price_1st = price_chunk.loc[0, 'price']
        factor_roll = roll_trade_start_pos / price_1st
        factor_fix = fix_trade_start_pos / price_1st
        
        price_chunk['roll_position'] = price_chunk['price'] * factor_roll
        price_chunk['fix_position'] = price_chunk['price'] * factor_fix
        scaled_dfs.append(price_chunk)
    return scaled_dfs
        

def fill_in_no_position_time(track_id, start_date, end_date, df):
    ALL_CASH_TICKER = 'all_cash'
    # impute days without position
    date_with_position = list(df['date'].to_list())
    
    all_dates = get_all_weekdays(start_date, end_date)
    rows = []
    for date in all_dates:
        if date in date_with_position:
            continue
        # create a new row
        # track_id    date    ticker    price    roll_position    fix_position
        row = {
            'track_id':track_id,
            'date': date,
            'ticker': ALL_CASH_TICKER,
            'price': 0,
            'roll_position' : -1,
            'fix_position' : -1,
        }
        rows.append(row)

    assert len(rows) + len(date_with_position) == len(all_dates)
    
    df_all_cash = pd.DataFrame(rows)    

    df_imputed = pd.concat([df_all_cash, df])
        
    df_sorted = df_imputed.sort_values(by=['date']).reset_index(drop = True)
    pre_fix = 1
    pre_roll = 1
    for i in range(0, len(df_sorted)): 
        ticker = df_sorted.loc[i, 'ticker']
        # fill in position gap
        if ticker == ALL_CASH_TICKER:
            df_sorted.loc[i, 'roll_position'] = pre_roll
            df_sorted.loc[i, 'fix_position'] = pre_fix
        else:
            pre_roll = df_sorted.loc[i, 'roll_position']
            pre_fix = df_sorted.loc[i, 'fix_position']     
    return df_sorted 

        
def gen_single_track_position_history(track_id, start_date, end_date, price_df, trades_df):

    boundaries = get_boundary_split_price_history_by_ticker(price_df)
    price_dfs = get_dfs_split_price_history_by_ticker(price_df, boundaries)
    scaled_dfs = rescale_price_using_trade_position(trades_df, price_dfs)
    position_history_with_hole = pd.concat(scaled_dfs)
    position_history = fill_in_no_position_time(track_id, start_date, end_date, position_history_with_hole)
    return position_history


def aggregate_to_dic(df):
    df['fix'] = df['fix_position']
    df['roll'] = df['roll_position']
    # todo
    gp = df.groupby('date')['roll','fix'].mean()
    df = gp.reset_index()
    return df


def gen_position_all_track(
    start_date,
    end_date,
    price_in_track_path, 
    trades_in_track_path, 
    track_count
):
    position_dfs = []
    
    # read csv of all tracks
    price_df = pd.read_csv(price_in_track_path)
    trades_df = pd.read_csv(trades_in_track_path)

    for track_id in range(0, track_count):
        # prepare df for single track
        print('get position from trades and price:',track_id)
        price_df_i = price_df[price_df['track_id']==track_id]
        price_df_i = price_df_i.sort_values(by=['date']).reset_index(drop = True)

        trades_df_i = trades_df[trades_df['track_id']==track_id]
        trades_df_i = trades_df_i.sort_values(by=['entry_ts']).reset_index(drop = True)
        
        print(len(price_df_i),len(price_df),len(trades_df_i),len(trades_df))
        
        single_track_position_df = gen_single_track_position_history(
            track_id,
            start_date,
            end_date,
            price_df_i, 
            trades_df_i
        )
        position_dfs.append(single_track_position_df)
    
    all_position_df = pd.concat(position_dfs)
    return all_position_df
