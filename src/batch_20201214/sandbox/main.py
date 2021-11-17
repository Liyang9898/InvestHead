'''
Created on Feb 21, 2021

@author: leon
'''
from version_master.version import (
    russell1000, 
    iwf, 
    exp_r1000,
    exp_iwf,
    exp_exclude_iwf,
    indicator_20210209
)
import pandas as pd
import os

def get_ticker_from_folder(folder):
    res = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            ticker = file.split('_')[0]
            res.append(ticker)
    return res

existing_indicator = get_ticker_from_folder(indicator_20210209)
print(len(existing_indicator))

df_r = pd.read_csv(russell1000)
list_r = df_r['ticker'].to_list()

df_iwf = pd.read_csv(iwf)
list_iwf = df_iwf['ticker'].to_list()

print(len(list_r))
print(len(list_iwf))

list_r_exist = []
for t in list_r:
    if t in existing_indicator:
        list_r_exist.append(t)



list_iwf_exist = []
for t in list_iwf:
    if t in list_r_exist:
        list_iwf_exist.append(t)

list_exclude_iwf_exist = []
for t in list_r_exist:
    if t not in list_iwf_exist:
        list_exclude_iwf_exist.append(t)        
    
print('existing r',len(list_r_exist))        
print('existing iwf',len(list_iwf_exist))
print('existing exclude iwf',len(list_exclude_iwf_exist))


all_df = pd.DataFrame(list_r_exist,columns=['ticker'])
iwf_df = pd.DataFrame(list_iwf_exist,columns=['ticker'])
counter_df = pd.DataFrame(list_exclude_iwf_exist,columns=['ticker'])


all_df.to_csv(exp_r1000,index=False)
iwf_df.to_csv(exp_iwf,index=False)
counter_df.to_csv(exp_exclude_iwf,index=False)