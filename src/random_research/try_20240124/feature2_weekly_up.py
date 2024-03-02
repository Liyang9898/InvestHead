'''
Created on Mar 2, 2024

@author: spark
'''
from util.util_time import date_add_days


def weekly_up(df_d, df_w):
    
    
    df_w['feature'] = df_w['ema8'] - df_w['ema21']
    df_w = df_w[df_w['feature']>0].copy()
    dates_w_tradable = list(df_w['date'].to_list())
    df_d['weekly_tradable'] = 0
    
    df_d.reset_index(drop=True, inplace=True)
    for i in range(len(df_d)):
        if i == 0:
            continue
        
        d = df_d.loc[i, "date"]
        for j in range(0,7):
            delta_days = -1*j
            d2 = date_add_days(d, delta_days)
            if d2 in dates_w_tradable:
                df_d.loc[i, "weekly_tradable"] = 1
                break

    df = df_d.copy()
    return df    
        
        # h = df_d.loc[i, "high"]
        # l = df_d.loc[i, "low"]
        # c = df_d.loc[i-1, "close"]
    
    
    # print(dates)