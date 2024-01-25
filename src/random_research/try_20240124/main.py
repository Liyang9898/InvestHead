'''
Created on Jan 24, 2024

@author: spark
'''
import pandas as pd
from util.general_ui import plot_line_from_xy_list


path_position_record='C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df=pd.read_csv(path_position_record)
df['feature'] = df['ema8'] - df['ema21']
df['label'] = 0
df['pct'] = 0

print(df[['feature','ema8','ema21']])

for i in range(len(df)-1):
    date = df.loc[i, "date"]
    s = df.loc[i, "open"]
    e = df.loc[i+1, "close"]
    change = e/s-1
    df.loc[i+1, "label"] = change


# df_target = df[df['feature']>0].copy()
df_target = df.copy()
df_target.sort_values(by=['label'],inplace=True)
df_target.reset_index(drop=True,inplace=True)


total = len(df_target)

for i in range(len(df_target)):
    date = df_target.loc[i, "date"]
    label = df_target.loc[i, "label"]
    pct = i/total
    df_target.loc[i, "pct"] = pct
    print(i,date,label,pct)
    
df_final = df_target[['date','label','pct']].copy()
df_final.reset_index(inplace=True)
df_final.to_csv('C:/f_data/random/exp_202401_24.csv', index=False)
print(df_final)