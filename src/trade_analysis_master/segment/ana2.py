import pandas as pd
from version_master.version import trade_swing_2150in_2150out_20210313_iwf

df = pd.read_csv(trade_swing_2150in_2150out_20210313_iwf + 'merge/feature.csv')
print(df['df_channel_width_percent'])


import plotly.express as px
df = px.data.tips()
fig = px.histogram(df, x="total_bill")
fig.show()