import pandas as pd
import plotly.graph_objects as go

from batch_20201214.util_for_batch.batch_util import get_all_files_general
from version_master.version import (
    trade_swing_2150in_2150out_20210313_iwf_50up
)
trade_path = trade_swing_2150in_2150out_20210313_iwf_50up

x = get_all_files_general(trade_path + 'section/')
print(x)

hist = {}   
res = []
for k,v in x.items():
    df = pd.read_csv(trade_path + 'section/'+v)
    l = df['pnl_percent'].to_list()
    hist[v] = l
    p=df.loc[df['pnl_percent'] > 0]
    n=df.loc[df['pnl_percent'] < 0]
    pnl = df['pnl_percent'].mean()
    win_pnl = p['pnl_percent'].mean()
    lose_pnl = n['pnl_percent'].mean()
    
    win_rate = 0
    if len(p) + len(n)>0:
        win_rate = len(p) / len(df)

    print(v, len(df), len(p), len(n), pnl,win_pnl,lose_pnl,'win_rate:', win_rate)
    dic = {
        'section': v,
        'total_trade':len(df),
        'win_trade':len(p),
        'lose_trade':len(n),
        'total_pnl':pnl,
        'win_pnl':win_pnl,
        'lose_pnl':lose_pnl,
        'win_rate':win_rate
    }
    res.append(dic)

res_df = pd.DataFrame(res)
res_df.to_csv(trade_path + 'merge/section_conclusion.csv')

fig = go.Figure()

xbins=dict(start=-1.0,end=1.0,size=0.1)


fig.add_trace(go.Histogram(x=hist['channel_enter_sec_-1.csv'],xbins=xbins,name='-1',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_0.csv'],xbins=xbins,name='0',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_25.csv'],xbins=xbins,name='25',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_50.csv'],xbins=xbins,name='50',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_75.csv'],xbins=xbins,name='75',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_100.csv'],xbins=xbins,name='120',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_150.csv'],xbins=xbins,name='120',histnorm='probability'))
fig.add_trace(go.Histogram(x=hist['channel_enter_sec_200.csv'],xbins=xbins,name='120',histnorm='probability'))

# Overlay both histograms
fig.update_layout(barmode='overlay')
fig.update_traces(opacity=0.75)
fig.show()