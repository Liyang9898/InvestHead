'''
Created on Jan 14, 2020

@author: leon
'''
import plotly.graph_objects as go

def single_heat_map(df, opentop,stop_gain_list,stop_loss_list, rank_col,title):
    df.sort_values(by='avg_monthly_gain', ascending=False)
    df = df[df['opentop']==opentop]
    z = []
    
    for y in stop_gain_list: #y
        z_row = []
        for x in stop_loss_list: #x
            current_row = df[(df['stop_gain']==y) & (df['stop_loss']==x)]
            heat=list(current_row[rank_col].to_list())
            for h in heat:
                z_row.append(h)
        z.append(z_row)
    
    
    fig = go.Figure(data=go.Heatmap(
                       z= z,
                       x=stop_gain_list,
                       y=stop_gain_list,
                    ))
    fig.update_layout(title=title,xaxis={"title": "stop_loss"},yaxis={"title": "stop_gain"})
    fig.show()
    
    
    
    #     df_head_values = [
#         'opentop',
#         'stop_loss', 
#         'stop_gain',
#         'avg_monthly_gain',
#         'win_rate',
#         'win_rate_exclude_neutral',
#         'pnl_ma_20_positive_rate',
#         'rate_ma_20_positive_rate',
#         'pnl_ma_20_avg',
#         'rate_ma_20_avg',
#     
#     ]
#     
#     df_values=[
#         df.opentop, 
#         df.stop_loss, 
#         df.stop_gain,
#         df.avg_monthly_gain,
#         df.win_rate,
#         df.win_rate_exclude_neutral,
#         df.pnl_ma_20_positive_rate,
#         df.rate_ma_20_positive_rate,
#         df.pnl_ma_20_avg,
#         df.rate_ma_20_avg,
#     ]