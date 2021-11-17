'''
Created on Mar 14, 2021

@author: leon
'''
import pandas as pd
import os
from version_master.version import (
    trade_swing_2150in_2150out_20210313_iwf_50up
)


def channel_sec(x, c0,c25,c50,c75,c100):
    if x > c100:
        if c100 > c0:
            over = (x-c0) / (c100-c0)
            if over > 2:
                return 200
            elif over > 1.5:
                return 150
            elif over > 1:
                return 100
        else:
            return 100
    elif x > c75:
        return 75
    elif x > c50:
        return 50
    elif x > c25:
        return 25
    elif x > c0:
        return 0    
    else:
        return -1

trade_path = trade_swing_2150in_2150out_20210313_iwf_50up
path = trade_path + 'merge/feature.csv'
df = pd.read_csv(path)
df['channel_enter_sec']=df.apply(
    lambda row : channel_sec(
        row['open'],
        row["barlow_2_ema8_channel_floor"],
        row["barlow_2_ema8_channel_ceiling"],
        row["barlow_2_ema8_channel_mp25_pos"],
        row["barlow_2_ema8_channel_mp50_pos"],
        row["barlow_2_ema8_channel_mp75_pos"]
    ), 
    axis = 1
)

# print(df['channel_enter_sec'])

section_path = trade_path + 'section/'
os.mkdir(section_path) 
k = 'channel_enter_sec'
vs = [-1,0,25,50,75,100,150,200]

dfs = {}
for v in vs:
    print(v)
    dfs[v]=df.loc[df[k] == v]
    dfs[v].to_csv(section_path + str(k) + '_'+ str(v) + '.csv')