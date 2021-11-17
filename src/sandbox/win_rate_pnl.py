import numpy as np
import pandas as pd
from datetime import datetime

win_rate = 0.8
win_pnl=0.04

lose_pnl = win_rate/(1-win_rate) *win_pnl

print(lose_pnl)


win_pnl = 1
lose_pnl = 0.5
win_rate = 0.55

gain = win_rate*win_pnl-(1-win_rate)*lose_pnl
print('total gain:', gain)


print('annual:',gain*12)
#32%, 80%

def days_gap_date_str(date_str_s, date_str_e):
#     print(date_str_s, date_str_e)
    dt_s = datetime.strptime(date_str_s, '%m/%d/%Y')
    dt_e = datetime.strptime(date_str_e, '%m/%d/%Y')
    gap = dt_e - dt_s
    return gap.days 

x = days_gap_date_str('9/2/2021','10/6/2021')
print(x)
path = 'D:/f_data/operation/closed.csv'
df = pd.read_csv(path)

df_close = df[['enter_price', 'exit_price']].copy()
df_close.dropna(inplace=True)
df_close['pnl'] = (df_close['exit_price'] - df_close['enter_price'])/df_close['enter_price']
df_win = df_close[df_close['pnl']>0]
df_lose = df_close[df_close['pnl']<=0]

avg_win = df_win['pnl'].mean()
avg_lose = df_lose['pnl'].mean()

print('win:',avg_win,' lose:',avg_lose)
win_rate = len(df_win)/len(df_close)
print('winrate:', win_rate)

avg_gain = win_rate * avg_win + (1-win_rate) * avg_lose
print(avg_gain)

df=df[['date','close date']].copy()
df.dropna(inplace=True)
df['gap']=df.apply(lambda row : days_gap_date_str(row['date'],row['close date']), axis = 1)



avg = df['gap'].mean()

print(avg)

