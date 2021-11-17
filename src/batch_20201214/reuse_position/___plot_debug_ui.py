from batch_20201214.reuse_position.lib.fit_price_onto_position import fill_in_no_position_time
import pandas as pd
import plotly.express as px
from version_master.version import (
    t_20210420_ema21_ma50_gap_per_ticker,
    t_20210425_ema21_ma50_gap_per_ticker_4p_out
)


trade_path=t_20210420_ema21_ma50_gap_per_ticker
track_id=0


def plot_trades_position(trade_path, track_id, fix_or_roll):
    trades_in_track_path = trade_path + """merge/cash_history_reuse_trades_in_track.csv"""
    all_trade_df = pd.read_csv(trades_in_track_path)
    i_trade_df = all_trade_df[all_trade_df['track_id']==track_id]
    if fix_or_roll == 'roll':
        fig_roll = px.scatter(i_trade_df, x="exit_ts", y="roll_trade_end_pos", color="ticker",title='roll_trade_end_pos')
        fig_roll.show()
    if fix_or_roll == 'fix':
        fig_fix = px.scatter(i_trade_df, x="exit_ts", y="fix_trade_end_pos", color="ticker",title='fix_trade_end_pos')
        fig_fix.show()    


def plot_price(trade_path, track_id):
    price_in_track_path = trade_path + """merge/cash_history_reuse_price_in_track.csv"""
    df = pd.read_csv(price_in_track_path)
    i_trade_df = df[df['track_id']==track_id]
    fig = px.scatter(i_trade_df, x="date", y="price", color="ticker",title='price')
    fig.show() 
    

def plot_continues_position(trade_path, track_id, fix_or_roll):
    trades_in_track_path = trade_path + """merge/cash_history_reuse_positions_in_track.csv"""
    all_trade_df = pd.read_csv(trades_in_track_path)
    i_trade_df = all_trade_df[all_trade_df['track_id']==track_id]
    if fix_or_roll == 'roll':
        fig_roll = px.scatter(i_trade_df, x="date", y="roll_position", color="ticker",title='roll_trade_end_pos')
        fig_roll.show()
    if fix_or_roll == 'fix':
        fig_fix = px.scatter(i_trade_df, x="date", y="fix_position", color="ticker",title='fix_trade_end_pos')
        fig_fix.show()   



def aggregate_to_dic(df):
    df['fix'] = df['fix_position']
    df['roll'] = df['roll_position']
    gp = df.groupby('date').sum()
    df_gp = gp.reset_index()
    res = df_gp[['date','fix','roll']]
    fig = px.line(res, x="date", y="roll",title='all_track')
    fig.show()    
    
    gp2 = df.groupby('date')['roll'].size()
    df_gp2 = gp2.reset_index()
    print(df_gp2)
     
    fig2 = px.line(df_gp2, x="date", y='roll',title='all_track')
    fig2.show()

def plot_trades_position_all_track(trade_path, fix_or_roll):
    trades_in_track_path = trade_path + """merge/cash_history_reuse_trades_in_track.csv"""
    all_trade_df = pd.read_csv(trades_in_track_path)

    if fix_or_roll == 'roll':
        fig_roll = px.line(all_trade_df, x="exit_ts", y="roll_trade_end_pos", color="track_id",title='roll_trade_end_pos')
        fig_roll.show()
    if fix_or_roll == 'fix':
        fig_fix = px.line(all_trade_df, x="exit_ts", y="fix_trade_end_pos", color="track_id",title='fix_trade_end_pos')
        fig_fix.show()    
        
def impute_debug(trade_path, track_id):
    # this path gots to be not imputed
    trades_in_track_path = trade_path + """merge/cash_history_reuse_positions_in_track.csv"""
    
    all_trade_df = pd.read_csv(trades_in_track_path)
    i_trade_df = all_trade_df[all_trade_df['track_id']==track_id]

    fig_roll = px.scatter(i_trade_df, x="date", y="roll_position", color="ticker",title='position')
    fig_roll.show()

    position_history = fill_in_no_position_time(
        track_id=track_id, 
        start_date="2016-01-01",
        end_date="2020-12-31",
        df=i_trade_df
    )

    fig_roll = px.scatter(position_history, x="date", y="roll_position", color="ticker",title='imputed')
    fig_roll.show() 

# plot price
# plot_price(trade_path, track_id) # print price

# single track
# plot_trades_position(trade_path, track_id, 'fix')
# plot_continues_position(trade_path, track_id, 'fix')

#all track
# plot_trades_position_all_track(trade_path, 'roll')

trades_in_track_path = trade_path + """merge/cash_history_reuse_positions_in_track.csv"""
all_trade_df = pd.read_csv(trades_in_track_path)
aggregate_to_dic(all_trade_df)





    

