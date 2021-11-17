
from version_master.version import (
    t_20210425_ema21_ma50_gap_per_ticker_4p_out,
    t_20210511_ema21_ma50_gap_per_ticker_3p_out,
    t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage
)
import pandas as pd
import numpy as np
import plotly.express as px

def eval_take_profit_at_p(threshold, trades_df):
    total = len(trades_df)
    win_cnt = 0
    total_pnl = 0
    for i in range(0, len(trades_df)):
        best_profit = trades_df.loc[i, 'best_potential_pnl_percent']
        pnl_percent = trades_df.loc[i, 'pnl_percent']
        pnl_percent_new = pnl_take_profit_p(threshold, best_profit, pnl_percent)
        total_pnl += pnl_percent_new
        if pnl_percent_new > 0:
            win_cnt += 1
        
    res = {
        'threshold': threshold,
        'total_opportunity': total,
        'win_rate': win_cnt * 1.0 / total,
        'total_pnl': total_pnl  
    }
    return res
    
def pnl_take_profit_p(threshold, best_profit, pnl_percent):
    if best_profit >= threshold:
        return threshold
    else:
        return pnl_percent
    
experiment = t_20210511_ema21_ma50_gap_per_ticker_no_profit_manage
path = f"{experiment}merge/all_trades_all_entry.csv"
print(path)
df = pd.read_csv(path)


def fit(df):

    ths = np.arange(0.01,2,0.01)
    rows = []
    for th in ths:
        th = round(th, 2)
        res = eval_take_profit_at_p(th, df)
        rows.append(res)
        print(res)
    df = pd.DataFrame(rows)
    df.to_csv('D:/f_data/leonyan518_4pexp1.csv')
    
# fit(df)

df = pd.read_csv('D:/f_data/leonyan518_4pexp1.csv')
print(df)
fig = px.line(df, x="threshold", y="win_rate", title='win_rate')
fig.show()
fig = px.line(df, x="threshold", y="total_pnl", title='total_pnl')
fig.show()