'''
Created on Jan 13, 2023

@author: spark
'''

import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

'''
conclusion: 
in positive: 0>1>(2,3,4)
in negative:
1>4
3<4
0<4
'''

path = 'C:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
df = pd.read_csv(path)

df.sort_values(by='time', ascending=True, inplace=True)
df.reset_index(inplace=True, drop=True)
df['weekly_delta'] = 0
df['weekday'] = 0



for i in range(0, len(df)):
    if i + 4 < len(df):
        t = df.loc[i, 'time']
        s = df.loc[i, 'close']
        e = df.loc[i + 4, 'close']  
        r = e / s - 1  
        df.loc[i, 'weekly_delta'] = r
        
        dt = datetime.fromtimestamp(int(t))
        wd = dt.weekday()
        df.loc[i, 'weekday'] = wd
        
        
print(len(df))

fig = px.histogram(df, x="weekly_delta", color="weekday", barmode="overlay")
fig.show()


positive = df[df['weekly_delta']>0]
negative = df[df['weekly_delta']<0]

fig = px.histogram(negative, x="weekly_delta", color="weekday", barmode="overlay",cumulative=True,histnorm='percent')
fig.show()

# weekday0 = df[df['weekday']==0]
# weekday1 = df[df['weekday']==1]
# weekday2 = df[df['weekday']==2]
# weekday3 = df[df['weekday']==3]
# weekday4 = df[df['weekday']==4]
# print(len(weekday0))
# print(len(weekday1))
# print(len(weekday2))
# print(len(weekday3))
# print(len(weekday4))
#
# fig0 = px.histogram(weekday0, x="weekly_delta", title='weekday0',cumulative=False,histnorm='percent')
# fig0.show()
#
# fig1 = px.histogram(weekday1, x="weekly_delta", title='weekday1',cumulative=False,histnorm='percent')
# fig1.show()
#
# fig2 = px.histogram(weekday2, x="weekly_delta", title='weekday2',cumulative=False,histnorm='percent')
# fig2.show()
#
# fig3 = px.histogram(weekday3, x="weekly_delta", title='weekday3',cumulative=False,histnorm='percent')
# fig3.show()
#
# fig4 = px.histogram(weekday4, x="weekly_delta", title='weekday4',cumulative=False,histnorm='percent')
# fig4.show()
