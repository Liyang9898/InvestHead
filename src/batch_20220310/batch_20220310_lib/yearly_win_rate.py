import pandas as pd
from util.general_ui import plot_bars_from_xy_list


path = 'D:/f_data/batch_20220214/step8_portfolio_time_series/intermediate_per_track_trades.csv'


df = pd.read_csv(path)
win = {}
lose = {}
win_rate = {}
all_year = []
for i in range(0, len(df)):
    pnl_percent = df.loc[i, 'pnl_percent']
    entry_ts = df.loc[i, 'entry_ts']
    year = int(str(entry_ts)[0:4])
    all_year.append(year)
    if year not in win:
        win[year] = 0
        
    if year not in lose:
        lose[year] = 0
        
    if pnl_percent > 0:
        win[year] += 1 
    else:
        lose[year] += 1 
        
for year in all_year:
    win_rate[year] = win[year] / (win[year] + lose[year])

x_list = list(win_rate.keys())
y_list = list(win_rate.values())
plot_bars_from_xy_list(x_list, y_list, title='default', path=None)
# print(win_rate)