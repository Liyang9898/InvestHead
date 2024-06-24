'''
Created on Jun 22, 2024

@author: spark
'''

import pandas as pd
import plotly.graph_objects as go
    
    
path_trade_pnl = 'C:/f_data/trades_csv/SPY_1W_fmt_trades_all_entry_2.csv'
# path_trade_pnl = 'C:/f_data/trades_csv/SPY_1W_fmt_trades_all_consecutive_2.csv'

df = pd.read_csv(path_trade_pnl)

print(df.columns)


# Index(['entry_price', 'entry_ts', 'exit_price', 'exit_ts', 'direction',
#        'bar_duration', 'pnl', 'pnl_percent', 'best_potential_pnl_percent',
#        'complete'],
#       dtype='object')
fig = go.Figure()
fig.add_trace(go.Histogram(x=df['pnl_percent'],name='pnl',nbinsx=100,histnorm='percent'))
fig.show()

    # title = f'Feature distribution: {feature}'
    # fig.update_layout(
    #     barmode='overlay',
    #     title=title,
    #     xaxis_title_text='Feature value', # x axis label
    #     yaxis_title_text='Distribution', # y axis label
    # )
    #
    # fig.update_traces(opacity=0.75)
    # if img_path=='':
    #     fig.show()
    # else:
    #     fig.write_image(img_path)