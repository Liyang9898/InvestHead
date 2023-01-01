'''
Created on Jan 1, 2023

@author: spark
'''
import plotly.express as px
import pandas as pd

path = 'C:/f_data/random/SPY_1W_1_year_return.csv'
df = pd.read_csv(path)


fig = px.bar(df, x='date', y='pnl_1_year')
fig.show()


fig2 = px.line(df, x='date', y='close')
fig2.show()


path_long = 'C:/f_data/random/SPY_1W_1_year_return_long.csv'
path_short = 'C:/f_data/random/SPY_1W_1_year_return_short.csv'
df_long = pd.read_csv(path_long)
df_short = pd.read_csv(path_short)

fig3 = px.histogram(df_long, x="pnl_1_year", title='long',cumulative=True,histnorm='percent')
fig3.show()

fig4 = px.histogram(df_short, x="pnl_1_year", title='short',cumulative=True,histnorm='percent')
fig4.show()

fig6 = px.bar(df_short, x='date', y='pnl_1_year')
fig6.show()