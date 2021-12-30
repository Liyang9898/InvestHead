import pandas as pd

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

