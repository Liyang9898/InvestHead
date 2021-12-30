'''
Created on Feb 14, 2021

@author: leon
'''
from batch_20201214.reuse_position.cash_position_from_price_lib import (
    price_in_track_df_to_dic,
    roll_over_position_all_tracks
)
from batch_20201214.reuse_position.fill_price_in_track_lib import (
    getAllEntryCSV,
    mergeAllEntryTrade,
    fill_position,
    get_ticker_list_from_track,
    build_price_history_collection,
    gen_price_seq,
    price_in_tracks_to_csv
)
from batch_20201214.reuse_position.lib.fit_price_onto_position import gen_position_all_track, \
    aggregate_to_dic
from batch_20201214.reuse_position.lib.util import track_trades_to_df
from batch_20211116.batch_20211116_lib.stock_ranking_store import gen_stock_rank_artifact
import pandas as pd
import plotly.express as px
from plotting_lib.simple import moving_window, dip_measure, moving_window_batch


def get_daily_position_cnt(path_in, path_out):
    df = pd.read_csv(path_in)
    daily_position_cnt = df.groupby('date').size().to_frame(name = 'position_cnt').reset_index()
    daily_position_cnt.to_csv(path_out, index=False)
    

def reuse_position_cash_history(
    # input
    start_date,
    end_date,
    trade_folder,
    ticker_rank_folder,
    indicator_folder,
    #output
    output_folder,
    #
    capacity=50,
):
    """
    input: time range, trades file, indicator file
        indicator folder's file name must be upper case ticker name
    output: 
        per track DataFrame with trades
        per track DataFrame with ticker and price for each date
        per track positions
        sum positions
        
        position count
        performance
    """
#     print(start_date,end_date,trade_folder,indicator_folder)
    path_trades = trade_folder
    
    # report folder
    per_track_trades_path = f'{output_folder}intermediate_per_track_trades.csv'
    per_track_ticker_price_path = f'{output_folder}intermediate_per_track_ticker_price.csv'
    per_track_position_path = f'{output_folder}intermediate_per_track_position.csv'
    per_track_summary_path = f'{output_folder}intermediate_per_track_summary.csv'
    
    moving_window_path = f'{output_folder}intermediate_moving_window.csv'
    position_cnt_path = f'{output_folder}intermediate_position_cnt.csv'
    
    position_path = f'{output_folder}position.csv'
    performance_path = f'{output_folder}performance.csv'
    
    #################################################################################################
    # step 1: fill in trades
#     per_track_ticker_price_path = trade_folder + """merge/cash_history_reuse_price_in_track.csv"""
    
    # step 2: retrieve price in trade range
#     per_track_trades_path = trade_folder + """merge/cash_history_reuse_trades_in_track.csv"""
    
    # step 3: re-scale price to make them match trades
#     per_track_position_path = trade_folder + """merge/cash_history_reuse_positions_in_track.csv"""
    
    #################################################################################################
#     per_track_summary_path = trade_folder + """merge/cash_history_reuse_track_summary.csv"""
#     moving_window_res_path = trade_folder + """merge/cash_history_reuse_moving_window.csv"""
#     cash_line_path = trade_folder + """merge/cash_history_reuse_cash_history.csv"""
#     position_cnt_path = trade_folder + """merge/daily_position_cnt.csv"""
#     position_path = trade_folder + """merge/cash_line_reuse.csv"""
#     performance_path = trade_folder + """merge/moving_windows.csv"""
     
    ############################################trades get start###################################################
    # merge all trades into one data structure
    files = getAllEntryCSV(path_trades)
    all_entry_trades = mergeAllEntryTrade(files)
    print('Until here, all trade option get')
    """
    Until here, all trade option is retrieved at hand
    """
    
    # this function insert all trades into N track
    ticker_rank_artifact = gen_stock_rank_artifact(ticker_rank_folder)
    tracks = fill_position(all_entry_trades, start_date, end_date, capacity,ticker_rank_artifact)        
    # track to csv, each row is one trade
    tracks_df = track_trades_to_df(tracks)
    tracks_df.to_csv(per_track_trades_path, index = False)
    print('Until here, we got a CSV with all trades happened in all tracks')
    """
    Until here, we got a CSV with all trades happened in all tracks
        col: ticker, track_id, trade.to_dic
    """
    ############################################trades get end###################################################
     
    ############################################price get start##################################################  
    # get all ticker that has been traded
    tickers = get_ticker_list_from_track(tracks)
    print('total traded ticker:', len(tickers))
    
    # get all price
    price_book = build_price_history_collection(tickers, indicator_folder)
    assert len(tickers) == len(price_book)
    print('price book loaded, ticker count correct, price in ticker correct, total traded ticker:', len(tickers))
    
    # track fill in price - return value has all price and ticker on all timestamp in all tracks
    price_in_tracks = gen_price_seq(tracks, price_book, per_track_summary_path)
    """
    Until here, we got a data structure of price and ticker on each day for each track
        dict<track_id, dict<data, {ticker:?,price?}>>
    """
    
    # write to csv
    price_in_tracks_to_csv(price_in_tracks, per_track_ticker_price_path)
    print('Until here, we got a csv of price and ticker on each day for each track')
    """
    Until here, we got a csv of price and ticker on each day for each track
        date, track_id, ticker, price
    """
    get_daily_position_cnt(per_track_ticker_price_path, position_cnt_path)
    """
    Until here, we got a csv of daily stock count
        date, total number of stock
    """
     
    df = pd.read_csv(per_track_ticker_price_path)
    price_in_tracks = price_in_track_df_to_dic(df) # dict<track_id, dict<data, {ticker:?,price?}>>
     
    # print validation
    print('get total track:', len(price_in_tracks))
    ############################################price get end#################################################### 
    
    ############################################position get start###############################################
    all_position_df=gen_position_all_track(
        start_date,
        end_date,
        per_track_ticker_price_path, 
        per_track_trades_path, 
        track_count=50
    )    
    all_position_df.to_csv(per_track_position_path, index=False)
    ############################################position get end#################################################
    print('until here we get a csv of positions in all tracks')
    """
    until here we get a csv of positions in all tracks
        col: track_id, date, ticker(include cash), ticker price, fix position, roll position
    """
    all_position_df = pd.read_csv(per_track_position_path)
    cash_fix_roll_df = aggregate_to_dic(all_position_df)
    cash_fix_roll_df.to_csv(position_path, index=False) 
    """
    until here we get a csv of positions sum up all tracks
        col: date, fix position, roll position
    """     
    # plot 
#     fig = px.line(cash_fix_roll_df, x="date", y="roll", title='roll')
#     fig.show()
     
#     fig2 = px.line(cash_fix_roll_df, x="date", y="fix", title='fix')
#     fig2.show()
     
    fix_dict = dict(zip(cash_fix_roll_df.date, cash_fix_roll_df.fix))
#     print(fix_dict)
      
    roll_dict = dict(zip(cash_fix_roll_df.date, cash_fix_roll_df.roll))
    
#     fix_dict = roll_dict
#     print(roll_dict)
#      
    mw_list = moving_window_batch(
        dic=fix_dict, 
        window_option=[260,120,60,20,10,5,2], 
        csv_path=moving_window_path
    )

#     res_12 = moving_window(fix_dict, window=260)
#     res_6 = moving_window(fix_dict, window=120)
#     res_3 = moving_window(fix_dict, window=60)
#     res_1 = moving_window(fix_dict, window=20)
    
    res_12 = mw_list[260]
    res_6 =  mw_list[120]
    res_3 =  mw_list[60]
    res_1 =  mw_list[20]
    
    dip_info = dip_measure(fix_dict)
      
#     print(res_1, '1 month')
#     print(res_3, '3 month')
#     print(res_6, '6 month')
#     print(res_12, '12 month ')
    res = {
        'alt_up_rate_1_m': res_1['positive_rate'],
        'alt_up_rate_3_m': res_3['positive_rate'],
        'alt_up_rate_6_m': res_6['positive_rate'],
        'alt_up_rate_12_m': res_12['positive_rate'],
        
        'alt_window_pnl_p_1_m': res_1['window_pnl_p_avg'],
        'alt_window_pnl_p_3_m': res_3['window_pnl_p_avg'],
        'alt_window_pnl_p_6_m': res_6['window_pnl_p_avg'],
        'alt_window_pnl_p_12_m': res_12['window_pnl_p_avg'],
        
        'max_dip_time':dip_info['max_dip_time'],
        'max_dip':dip_info['max_dip'],
        'max_dip_exit_ts':dip_info['max_dip_exit_ts'],
        'max_dip_bottom_ts':dip_info['max_dip_bottom_ts']
    }

    
    moving_window_df = pd.DataFrame([res])
    moving_window_df.to_csv(performance_path,index=False)
    """
    until here: we get the performance stat of the Portfolio overtime
    """
#     print(res)
    
#     moving_window_res_path = trade_folder + """merge/cash_history_reuse_moving_window.csv"""
#     cash_line_path = trade_folder + """merge/cash_history_reuse_cash_history.csv"""