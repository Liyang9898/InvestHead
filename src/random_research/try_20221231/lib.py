'''
Created on Dec 31, 2022

@author: spark
'''
import pandas as pd

path = 'C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'
df = pd.read_csv(path)
df['pnl_1_year'] = ''

print(df.columns)

for i in range(0, len(df)):
    s = i
    e = i + 52
    if e > len(df) - 1:
        break
    dt = df.loc[s, 'date']
    p_s = df.loc[s, 'close']
    p_e = df.loc[e, 'close']
    pnl = p_e / p_s - 1
    df.loc[i, 'pnl_1_year'] = pnl
    print(dt, p_s, p_e, pnl)


print(df)

df.to_csv('C:/f_data/random/SPY_1W_1_year_return.csv',index=False)