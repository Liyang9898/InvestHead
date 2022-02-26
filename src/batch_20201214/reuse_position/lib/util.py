import pandas as pd
from trading_floor.TradeInterface import Trade


def get_cash_line(df):
    df_sorted = df.sort_values(by=['entry_ts']).reset_index(drop=True)
    roll_trade_end_pos = 1
    fix_trade_end_pos = 1
    df_sorted['roll_trade_end_pos']=1
    df_sorted['fix_trade_end_pos']=1
    
    df_sorted['roll_trade_start_pos']=1
    df_sorted['fix_trade_start_pos']=1
    
    for i in range(0,len(df_sorted)):
        factor = 1+df_sorted.loc[i,'pnl_percent']
        df_sorted.loc[i,'roll_trade_start_pos'] = roll_trade_end_pos
        df_sorted.loc[i,'fix_trade_start_pos'] = fix_trade_end_pos        
        roll_trade_end_pos *= factor
        fix_trade_end_pos += df_sorted.loc[i,'pnl_percent']
        df_sorted.loc[i,'roll_trade_end_pos'] = roll_trade_end_pos
        df_sorted.loc[i,'fix_trade_end_pos'] = fix_trade_end_pos
    return df_sorted


def df_to_track_trades(df):
    """
    input: df with trades column an track id
    output: map<track_id, list<map< >>>   
    map = {
        "ticker": ticker,
        "trade": trade ->Trade class in TradeInterface.py
    }
    """
    tracks = {}
    for i in range(0, len(df)):
        track_id = int(df.loc[i, 'track_id'])
        ticker = df.loc[i, 'ticker']
        complete = False
        if df.loc[i, 'entry_price'] == 'TRUE':
            complete = True
        trade = Trade(
            entry_price = df.loc[i, 'entry_price'], 
            entry_ts = df.loc[i, 'entry_ts'], 
            exit_price = df.loc[i, 'exit_price'], 
            exit_ts = df.loc[i, 'exit_ts'], 
            direction = df.loc[i, 'direction'], 
            bar_duration = df.loc[i, 'bar_duration'],
            best_potential_pnl_percent = df.loc[i, 'best_potential_pnl_percent'],
            complete=complete
        )
        if track_id not in tracks:
            tracks[track_id] = []
        tup = {
            "ticker": ticker,
            "trade": trade
        }
        tracks[track_id].append(tup)
    
    for x,y in tracks.items():
        print(x, len(y))
        
    return tracks


def track_trades_to_df(track, capacity):
    # convert to df
    rows = []
    for track_id, trades in track.items():
        for trade in trades:
            ticker = trade['ticker']
            trade_detail = trade['trade']
            trade_dic = trade_detail.trade2dic()
            trade_dic['ticker'] = ticker
            trade_dic['track_id'] = track_id
            rows.append(trade_dic)
    all_trade_df = pd.DataFrame(rows)
    
    # get position
    cash_dfs= {}
    for i in range(0,capacity):
        cash_df_i = all_trade_df[all_trade_df['track_id']==i]
        cash_df_i_pos = get_cash_line(cash_df_i)
        cash_dfs[i] = cash_df_i_pos
    all_trade_df_with_pos = pd.concat(list(cash_dfs.values()))    
        
    return all_trade_df_with_pos

