'''
Created on Feb 21, 2021

@author: leon
'''
import pandas as pd
import plotly.graph_objects as go

path = "D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv"

df = pd.read_csv(path)

x0=df['v_p_3d'].to_list()
x1=df['v_p_1w'].to_list()
x2=df['v_p_2w'].to_list()

fig = go.Figure()
fig.add_trace(go.Histogram(x=x0,xbins=dict(size=0.005)))
fig.add_trace(go.Histogram(x=x1,xbins=dict(size=0.005)))
fig.add_trace(go.Histogram(x=x2,xbins=dict(size=0.005)))

# Overlay both histograms
fig.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
fig.show()

def get_p_x(l,x):
    l.sort()
    idx = int((x * 1.0 / 100) * len(l))

    return l[idx]

df_positive_v_p_3d = df[df['v_p_3d']>0]['v_p_3d'].to_list()
res = get_p_x(df_positive_v_p_3d, 90)
print(res)