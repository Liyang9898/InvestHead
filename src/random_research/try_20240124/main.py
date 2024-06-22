'''
Created on Jan 24, 2024

@author: spark
'''
import pandas as pd
from random_research.try_20240124.feature1_2pct_past5_days import per_bar_change_max
from random_research.try_20240124.feature2_weekly_up import weekly_up
from util.general_ui import plot_line_from_xy_list, plot_candle_stick


path_position_record='C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df=pd.read_csv(path_position_record)
df_daily = df.copy()

path_position_record_w='C:/f_data/price_with_indicator/SPY_1W_fmt_idc.csv'
df_w=pd.read_csv(path_position_record_w)


'''

'''
df['feature'] = df['ema8'] - df['ema21']
'''
'''

df['label'] = 0
df['pct'] = 0

# print(df[['feature','ema8','ema21']])

# compute over 2 days change
for i in range(len(df)-1):
    date = df.loc[i, "date"]
    s = df.loc[i, "open"]
    e = df.loc[i+1, "close"]
    change = e/s-1
    df.loc[i+1, "label"] = change


'''
feature compute region start
'''
#small feature daily ema8>ema21
df['feature'] = df['ema8'] - df['ema21']
# apply daily past 5 trading days max change < 0.02
df = per_bar_change_max(df, 0.02, 10, 'breach_2_pst_10_bar')  
df = per_bar_change_max(df, 0.025, 15, 'breach_25_pst_15_bar')  
df = per_bar_change_max(df, 0.03, 15, 'breach_3_pst_15_bar')   
# apply this weeks weekly ema21>ma50
df = weekly_up(df, df_w)
'''
feature compute region end
'''



'''
apply feature start, get rid of the days that you don't trade
'''
# apply daily past 5 trading days max change < 0.02
df= df[df['breach_2_pst_10_bar']==0].copy()
# df= df[df['breach_25_pst_15_bar']==0].copy()
# df= df[df['breach_3_pst_15_bar']==0].copy()

# apply daily ema8>ena21
df = df[df['feature']>0].copy()

# apply this weeks weekly ema21>ma50
df= df[df['weekly_tradable']==1].copy()

'''
apply feature end, get rid of the days that you don't trade
'''

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
    
df_final = df_target[['date','label','pct']].copy()
# pct mean the chance that the drop is smaller than 'label' as indicated
df_final.reset_index(inplace=True)
df_final.to_csv('C:/f_data/random/exp_202401_24.csv', index=False)

print('trade count', len(df_final))

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
    if label>markup:
        row = {'drop':markup,'chance':pct}
        l.insert(0,row)
        offset=offset+1
        if offset >= len(pct_mark_up):
            break

df_pct_simple = pd.DataFrame(l)
print(df_pct_simple)
df_pct_simple.to_csv('C:/f_data/random/exp_202401_24_pct.csv', index=False)

'''
draw tradeble days
'''
# trade_days = list(df['date'].to_list())
# print(trade_days)
plot_candle_stick(df, date_marker=[], date_marker2=[], ticker='spy')
plot_candle_stick(df_daily, date_marker=[], date_marker2=[], ticker='spy')

df_lose = df_final[df_final['label']<-0.02].copy()
lose_date = list(df_lose['date'].to_list())
plot_candle_stick(df, date_marker=lose_date, date_marker2=[], ticker='spy')
# print(df_lose)