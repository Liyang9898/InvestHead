import pandas as pd

def get_trade_perf_from_trades_csv(trades_csv, output_perf_csv):
    df = pd.read_csv(trades_csv)
    df_complete = df[df['complete']==True]
    df_win = df_complete[df_complete['pnl_percent'] > 0]
    df_lose = df_complete[df_complete['pnl_percent'] < 0]
    
    total_trade = len(df_complete)
    win_cnt = len(df_win)
    lose_cnt = len(df_lose)
    
    win_pnl_avg = df_win['pnl_percent'].mean()
    lose_pnl_avg = df_lose['pnl_percent'].mean()
    win_rate = win_cnt / total_trade
    lose_rate = lose_cnt / total_trade
    
    win_lose_pnl_ratio = (win_rate * win_pnl_avg) / (lose_rate * lose_pnl_avg) * -1
    
    stat = {
        'ticker': 'portfolio',
        'win_rate':round(win_rate,4),
        'lose_rate':round(lose_rate,4),
        'win_pnl_avg':round(win_pnl_avg,4),
        'lose_pnl_avg':round(lose_pnl_avg,4),
        'win_lose_pnl_ratio':round(win_lose_pnl_ratio,4),
        'total_trades':round(total_trade,4),
    }
    df_stat = pd.DataFrame([stat])
    df_stat.to_csv(output_perf_csv, index=False)

    

trades_csv = 'D:/f_data/batch_20211116/step8_portfolio_time_series/intermediate_per_track_trades.csv'
output_perf_csv = 'D:/f_data/temp/ab/trade_perf.csv'
get_trade_perf_from_trades_csv(trades_csv, output_perf_csv)
