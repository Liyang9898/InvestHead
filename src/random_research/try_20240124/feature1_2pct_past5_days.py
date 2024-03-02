'''
Created on Mar 1, 2024

@author: spark
'''
import pandas as pd
import math

# get pct change on each bar,  from previous close to today's high low
def per_bar_change_max(df, threshold, x_bar):
    df['per_bar_change_max'] = 0
    df['per_bar_change_max_breach'] = 0
    df['breach_in_pst_x_bar'] = 0
    for i in range(len(df)):
        if i == 0:
            continue
        
        d = df.loc[i, "date"]
        h = df.loc[i, "high"]
        l = df.loc[i, "low"]
        c = df.loc[i-1, "close"]
        
        diff1 = abs(h-c)
        diff2 = abs(l-c)
        
        pct1 = diff1/c
        pct2 = diff2/c
        
        pact_max = max(pct1,pct2)
        df.loc[i, "per_bar_change_max"] = pact_max
        
        if (pact_max>threshold):
            df.loc[i, "per_bar_change_max_breach"] = 1
            
        # check past x bars    
        for j in range(1, x_bar+1):
            if i-j < 0:
                break
            breach_in_past = df.loc[i-j, "per_bar_change_max_breach"]
            if breach_in_past == 1:
                df.loc[i, "breach_in_pst_x_bar"] = 1
                break
    df = df.copy()  
    return df



'''
test
'''

# path_position_record='C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
# df=pd.read_csv(path_position_record)
# df = per_bar_change_max(df, 0.02, 5)
# df= df[df['breach_in_pst_x_bar']==1]
# print(df)