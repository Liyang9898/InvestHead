'''
Created on Feb 13, 2021

@author: leon
'''
import os
import pandas as pd
from trading_floor.TradeInterface import Trade
from datetime import date, timedelta
import datetime
import random




def getAllEntryCSV(path):
    files = {}
    for file in os.listdir(path):
        if file.endswith("_all_entry.csv"):
            file_path = path + file 
            ticker = file.split('_')[0]
            files[ticker] = file_path
    
    return files


# this function merge all trades into one data structure
def mergeAllEntryTrade(files):
    """
    input: a list of files with entry
    output: dict<date, dict<ticker, Trade Object>>
    """
    all_entry_trades = {}
    total_trade_cnt = 0
    for ticker, file in files.items():
        # per ticker

        trades_df = None
        
        try:
            trades_df = pd.read_csv(file)
            ### Do Some Stuff
        except:
            continue
        
        
        total_trade_cnt = total_trade_cnt + len(trades_df)
        for i in range(0, len(trades_df)):
            # per trades
            trade = Trade(
                entry_price=trades_df.loc[i, 'entry_price'], 
                entry_ts=trades_df.loc[i, 'entry_ts'], 
                exit_price=trades_df.loc[i, 'exit_price'], 
                exit_ts=trades_df.loc[i, 'exit_ts'], 
                direction=trades_df.loc[i, 'direction'], 
                bar_duration=trades_df.loc[i, 'bar_duration'],
                best_potential_pnl_percent=trades_df.loc[i, 'best_potential_pnl_percent'],
                complete=trades_df.loc[i, 'complete']
            )
            # insert 
            entry_date = trades_df.loc[i, 'entry_ts'].split(' ')[0]
            
            # key exist
            if entry_date not in all_entry_trades.keys():
                all_entry_trades[entry_date] = {}
            all_entry_trades[entry_date][ticker] = trade
            
    cnt = 0
    for dt, val in all_entry_trades.items():
        cnt = cnt + len(val)
    assert cnt == total_trade_cnt
    print('merge from csv complete, number match:', cnt, total_trade_cnt)    
    return all_entry_trades


def filter_by_historical_best_ticker(all_entry_trades, yearly_ticker_pool):
    """
    for each date, we filter the ticker by the yearly_ticker_pool
    to get the best tickers for that time period
    yearly_ticker_pool has the best ticker for the past x years perf
    input: dict<date, dict<ticker, Trade Object>>
    output: dict<date, dict<ticker, Trade Object>>
    """
    all_entry_trades


def get_date_list(start_time, end_time):
    sdate = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    edate = datetime.datetime.strptime(end_time, '%Y-%m-%d')
    delta = edate - sdate       # as timedelta
    
    res = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        # remove weekend
        if day.weekday() >= 5: # 0-6
            continue # weekend
        
        day_str = day.strftime('%Y-%m-%d')
        res.append(day_str)
    
    return res


def draw_x_card_out_of_y(x, y):
#     print(x,y)
    res = []
    for i in range(0,min(x,y)):
        r = random.randint(1, y)
        while r in res:
            r = random.randint(1, y)
#             print(r)
        res.append(r)
    return res


def extract_track_time_seq(track):
    entry_ts_list = []
    for x in track:
        entry_ts = x['trade'].entry_ts
        if len(entry_ts_list) > 0:
            assert entry_ts_list[len(entry_ts_list)-1] <= entry_ts
        entry_ts_list.append(entry_ts)
    return entry_ts_list


# this function insert all trades into N track
def fill_position(all_entry_trades, start_date, end_date, capacity, print_log=False):
    room = {}
    track = {} # trade is room history, list of <ticker, trade>
    for idx in range(0, capacity):
        room[idx] = '-1'
        track[idx] = []
    
    historical_trades = []
    open_trades = {}
    daily_position_cnt = {}
    out_log = {}
    in_log = {}
    dates = get_date_list(start_date, end_date)
    for date in dates:
        # initial
        in_log[date] = []
        out_log[date] = []
        
        # step 1: close trade
        for ticker, cur_position in open_trades.items():
            exit_ts = cur_position.exit_ts
            exit_ts_date = exit_ts.split(' ')[0]
            if exit_ts_date == date: # exit
                out_log[date].append(ticker)
                
        for ticker in out_log[date]:
            del open_trades[ticker]
            
        # room scan, delete from room
        for idx, v in room.items():
            if v in out_log[date]:
                room[idx] = '-1'
                
        # step 2: add position
        if date not in all_entry_trades.keys(): # no opportunity today
            continue
        
        slot = capacity - len(open_trades)
        if slot == 0: # no remaining cash for new position today
            continue
        
        # start buying      
        all_entry_today = all_entry_trades[date] # all option
        
        # rule out existing position
        trade_opportunity_today = all_entry_today.copy()
        for _room_i, room_v in room.items():
            if room_v in trade_opportunity_today:
                # remove ticker in opportunity if it is already there
                del trade_opportunity_today[room_v]
        
        opportunity_cnt = len(trade_opportunity_today)
        drawed_id = draw_x_card_out_of_y(slot,opportunity_cnt)
        
        idx = 0
        room_idx = 0
        for ticker, trade in trade_opportunity_today.items():
            if idx not in drawed_id:
                idx = idx + 1
                continue
            open_trades[ticker]=trade
            historical_trades.append(trade)
            in_log[date].append(ticker)
            idx = idx + 1
            
            # find a room for ticker
            while room[room_idx] != '-1':
                room_idx = room_idx + 1
            room[room_idx] = ticker
            
            # track validation
            if len(track[room_idx]) > 0:
                last_trade_in_track = track[room_idx][len(track[room_idx])-1]
                last_trade_in_track_exit_price = last_trade_in_track['trade'].exit_ts
                new_enter_ts = trade.entry_ts
                assert last_trade_in_track_exit_price <= new_enter_ts
            
            # insert into 
            track_record = {
                "ticker": ticker,
                "trade": trade
            }
            track[room_idx].append(track_record)
            
            
        daily_position_cnt[date] = len(open_trades)   
        
        # validation on room logic
        x = 0
        
        for ticker in room.values():
            if ticker != '-1':
                x = x + 1

        assert x == len(open_trades)
        
        
        
        if print_log:
            print('date:', date, ' in:', in_log[date], ' out:', out_log[date] , ' position cnt:',len(open_trades)) 
    
    # print track information

    for idx in range(0,capacity):
        track_time_seq = extract_track_time_seq(track[idx])
        if print_log:
            print(track_time_seq)
            print('track id:', idx, ' ticker count:', len(track[idx]),' ',track[idx])
    print('fill in track complete, each track in time sequence valid')
    return track


def build_price_history_collection(ticker_list, indicator_folder):
    price_book = {}
    for ticker in ticker_list:
        path = indicator_folder + ticker + '_downloaded_raw.csv'
        df = pd.read_csv(path)
        date_price_dic = {}
        
        for i in range(0, len(df)):
            est_time = df.loc[i, 'est_datetime']
            date = est_time.split(' ')[0]
            close_price = df.loc[i, 'close']
            date_price_dic[date] = close_price
        
        price_book[ticker] = date_price_dic
        assert len(date_price_dic) > 0
    return price_book
            

def gen_price_seq_one_track(track, price_history):
    date_position_dic = {}
    for x in track:
        ticker = x['ticker']
        s = x['trade'].entry_ts.split(' ')[0]
        e = x['trade'].exit_ts.split(' ')[0]
        date_list = get_date_list(s, e)

        for date in date_list:
            if date not in price_history[ticker].keys(): # not every day is a trading day
                continue
            close_price = price_history[ticker][date]
            date_position_dic[date] = {
                "ticker": ticker,
                "price": close_price
            }
    return date_position_dic
    


def get_ticker_list_from_track(tracks):
    tickers = []
    for idx, track in tracks.items():
        for x in track:
            ticker = x['ticker']
            if ticker not in tickers:
                tickers.append(ticker)
    return tickers


# track fill in price
def gen_price_seq(tracks, price_book, track_summary_path):
    """
    output: 
        price and ticker on each day for each track
        dict<track_id, dict<data, {ticker:?,price?}>>
    """
    price_in_tracks = {}
    rows = []
    for idx, track in tracks.items():
        
        price_in_track = gen_price_seq_one_track(track, price_book)
        position_open_days = len(price_in_track)
        
        # validation - ticker
        input_ticker = []
        ouput_ticker = []
        
        for x in track:
            t1 = x['ticker']
            if t1 not in input_ticker:
                input_ticker.append(t1)
        
        for date, x in price_in_track.items():
            t2 = x['ticker']
            if t2 not in ouput_ticker:
                ouput_ticker.append(t2)
        
        assert len(input_ticker) == len(ouput_ticker) 
    
        
        for t3 in input_ticker:
            if t3 in ouput_ticker:
                ouput_ticker.remove(t3)
        assert len(ouput_ticker) == 0
        
        # validation - days
        input_date = []
        output_date = []
        for x in track:
            t4 = x['ticker']
            s = x['trade'].entry_ts.split(' ')[0]
            e = x['trade'].exit_ts.split(' ')[0]
            date_list = get_date_list(s, e)
            for date in date_list:
                if date not in price_book[t4].keys():
                    continue
                if date not in input_date:
                    input_date.append(date)
        
        for date, _x in price_in_track.items():
            if date not in output_date:
                output_date.append(date)
        
        assert  len(output_date) == len(input_date) 
        

        # print track_summary
        track_summary = {
            'track_id': idx,
            'ticker_traded': len(input_ticker),
            'position_open_days': position_open_days,
            'ticker': ','.join(input_ticker)
        }
        rows.append(track_summary)

        price_in_tracks[idx] = price_in_track
        
    track_summary_df = pd.DataFrame(rows)
    track_summary_df.to_csv(track_summary_path, index=False)
    return price_in_tracks


def price_in_tracks_to_csv(price_in_tracks, path):
    rows = []
    for idx, track in price_in_tracks.items():
        for date, x in track.items():
            ticker = x['ticker']
            price = x['price']
            row = {
                'track_id': idx,
                'date': date,
                'ticker': ticker,
                'price': price
            }
            rows.append(row)
    df = pd.DataFrame(rows)

    df.to_csv(path, index=False)
    print('write to csv: ', path)
    
