'''
Created on Feb 21, 2021

@author: leon
'''
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


output_path1="D:/f_data/sweep_20201214/merge_detail/test_1_all_entry.csv"
output_path2="D:/f_data/sweep_20201214/merge_detail/test_1_consecutive.csv"

# df_all_entry = pd.read_csv(output_path1)
df_consecutive = pd.read_csv(output_path2)

fig2 = px.histogram(df_consecutive, x="pnl_percent", range_x=[-1, 1])
fig2.show()


pnl_positive = df_consecutive[df_consecutive['pnl_percent']>0]
pnl_negative = df_consecutive[df_consecutive['pnl_percent']<0]
pnl_negative['pnl_percent'] = pnl_negative['pnl_percent'] * -1

x0 = pnl_positive['pnl_percent'].to_list()
x1 = pnl_negative['pnl_percent'].to_list()
x2 = df_consecutive['best_potential_pnl_percent'].to_list()




# Add 1 to shift the mean of the Gaussian distribution


fig = go.Figure()
fig.add_trace(go.Histogram(x=x0,xbins=dict(start=-1,end=0.4)))
fig.add_trace(go.Histogram(x=x1,xbins=dict(start=-1,end=0.4)))
fig.add_trace(go.Histogram(x=x2,xbins=dict(start=-1,end=0.4)))

# Overlay both histograms
fig.update_layout(barmode='overlay')
# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
fig.show()