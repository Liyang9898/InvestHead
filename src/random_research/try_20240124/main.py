'''
Created on Jan 24, 2024

@author: spark
'''
import pandas as pd
from util.general_ui import plot_line_from_xy_list


path_position_record='C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df=pd.read_csv(path_position_record)

'''
small feature daily ema8>ema21
'''
df['feature'] = df['ema8'] - df['ema21']
'''
'''

df['label'] = 0
df['pct'] = 0

print(df[['feature','ema8','ema21']])

# compute over 2 days change
for i in range(len(df)-1):
    date = df.loc[i, "date"]
    s = df.loc[i, "open"]
    e = df.loc[i+1, "close"]
    change = e/s-1
    df.loc[i+1, "label"] = change


'''
apply feature, get rid of the days that you don't trade
'''
df = df[df['feature']>0].copy()
df_target = df.copy()

'''
'''

'''
print out trade record
'''
df_target.sort_values(by=['label'],inplace=True)
df_target.reset_index(drop=True,inplace=True)


'''
get percentage record
'''
total = len(df_target)

for i in range(len(df_target)):
    date = df_target.loc[i, "date"]
    label = df_target.loc[i, "label"]
    pct = i/total
    df_target.loc[i, "pct"] = 1 - pct
    print(i,date,label,pct)
    
df_final = df_target[['date','label','pct']].copy()
# pct mean the chance that the drop is smaller than 'label' as indicated
df_final.reset_index(inplace=True)

print(df_final)

'''
get percentage record only on certain mark up,
basically extract several row from the previous record
'''
pct_mark_up = [-0.02,-0.015,-0.01, 0]

offset = 0
l = []
for i in range(len(df_target)):
    date = df_target.loc[i, "date"]
    label = df_target.loc[i, "label"]
    pct = df_target.loc[i, "pct"]
    markup = pct_mark_up[offset]
    if i ==0:
        row = {'drop':label,'chance':pct}
        l.insert(0,row)
        print(row)
    if label>markup:
        row = {'drop':markup,'chance':pct}
        l.insert(0,row)
        print(row)
        offset=offset+1
        if offset >= len(pct_mark_up):
            break

df_pct_simple = pd.DataFrame(l)
print(df_pct_simple)
df_pct_simple.to_csv('C:/f_data/random/exp_202401_24.csv', index=False)