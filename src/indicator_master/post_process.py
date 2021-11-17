'''
Created on Feb 22, 2021

@author: leon
'''
import pandas as pd

# cause: velocity 3d, 5d, 10d
# effect: price movement 3d, 5d, 10d
def velocity_price_causal_matrix(df):
    for i in range(0, len(df)):
        v_p_3d = df.loc[i, 'v_p_3d']
        v_p_1w = df.loc[i, 'v_p_1w']
        v_p_2w = df.loc[i, 'v_p_2w']
        delta_p_3d = df.loc[i, 'delta_p_3d']
        delta_p_1w = df.loc[i, 'delta_p_1w']
        delta_p_2w = df.loc[i, 'delta_p_2w']
        
        
#         print(v_3d)
        
path = "D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv"

df=pd.read_csv(path)
velocity_price_causal_matrix(df)