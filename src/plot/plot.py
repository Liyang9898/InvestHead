import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from plotly.subplots import make_subplots


def gendatetime(date_str, time_str):
    s=date_str+' '+time_str
    p='%d/%m/%Y  %H:%M:%S'
    return datetime.strptime(s, p)
    
def plot_day_chart_multi(df_day, ds, trades):
    df_day = df_day.loc[df_day['date'] == ds]
    if len(trades) == 0:
        return
    price_traces =go.Candlestick(
        x=df_day['est_time'],
        open=df_day['open'],
        high=df_day['high'],
        low=df_day['low'],
        close=df_day['close'],
        name=ds,
    )
    trades_element = trade2plotelement_single(trades[ds])
    dat = []
    for token in trades_element:
        dat.append(token["enter"])
        dat.append(token["exit"])
    
    lines = []
    for token in trades_element:
        lines.append(token["enter_ts"])
        lines.append(token["exit_ts"])
        lines.append(token["enter_p"])
        lines.append(token["exit_p"])
    
    
    dat.insert(0,price_traces)        
    fig = go.Figure(
        data=dat,
    )


    fig.update_layout(xaxis_rangeslider_visible=False)  
    
#     if len(trades) is 0:
#         return
    fisrt_trade = list(trades.values())[0]

    fisrt_enter_p = fisrt_trade['entry_p']
    enter_p_p3=dict(
        y0=fisrt_enter_p+3, 
        y1=fisrt_enter_p+3, 
        x0=0, x1=1, xref='paper', yref='y',line=dict(color="LightSeaGreen",dash="dot"),
        line_width=1
    )
    enter_p_p2=dict(
        y0=fisrt_enter_p+2, 
        y1=fisrt_enter_p+2, 
        x0=0, x1=1, xref='paper', yref='y',line=dict(color="LightSeaGreen",dash="dot"),
        line_width=1
    )
    enter_p_m3=dict(
        y0=fisrt_enter_p-3, 
        y1=fisrt_enter_p-3, 
        x0=0, x1=1, xref='paper', yref='y',line=dict(color="LightSeaGreen",dash="dot"),
        line_width=1
    )
    enter_p_m2=dict(
        y0=fisrt_enter_p-2, 
        y1=fisrt_enter_p-2, 
        x0=0, x1=1, xref='paper', yref='y',line=dict(color="LightSeaGreen",dash="dot"),
        line_width=1
    )




    win_str = 'win'
    color_str = 'green'
    if fisrt_trade['pnl'] == 0:
        win_str = 'neutual'
        color_str = 'yellow'
    elif fisrt_trade['pnl'] < 0:
        win_str = 'lose'
        color_str = 'red'
    long_str = 'short'
    if fisrt_trade['is_long']:
        long_str = 'long'
    title = ds + ' ' + win_str + '   Direction:['+long_str+'] PNL = ' + str(fisrt_trade['pnl'])
    fig.update_layout(
        height=400, 
        width=1200,
        title = ds,
        shapes=[
            # these are +/- 2 3 indicator
#             enter_p_p2,enter_p_p3,enter_p_m2,enter_p_m3
        ] + lines,
        annotations=[
            dict(x='0', y=0, xref='paper', yref='paper',
            showarrow=False, 
            xanchor='left', 
            text=title,font=dict(color=color_str))
        ]
    )
    fig.show()
    
def trade2plotelement(trades):
    res = []
    print('trade count:',len(trades))
    for ds,trade in trades.items():
        
        print(trade)
        enter={
            "mode": "markers", 
            "name": "one_side", 
            "type": "scatter", 
            "x":[trade['entry_ts']],
            "y":[trade['entry_p']],
            "line_color":"green",
            "line":{
                "width":8
            }
        }
        exit={
            "mode": "markers", 
            "name": "one_side", 
            "type": "scatter", 
            "x":[trade['exit_ts']],
            "y":[trade['exit_p']],
            "line_color":"purple",
            "line":{
                "width":8
            }
        }
        enter_ts=dict(
            x0=trade['entry_ts'], 
            x1=trade['entry_ts'], 
            y0=0, y1=1, xref='x', yref='paper',
            line_width=1
        )
        exit_ts=dict(
            x0=trade['exit_ts'], 
            x1=trade['exit_ts'], 
            y0=0, y1=1, xref='x', yref='paper',
            line_width=1
        )
        enter_p=dict(
            y0=trade['entry_p'], 
            y1=trade['entry_p'], 
            x0=0, x1=1, xref='paper', yref='y',
            line_width=1
        )
        exit_p=dict(
            y0=trade['exit_p'], 
            y1=trade['exit_p'], 
            x0=0, x1=1, xref='paper', yref='y',
            line_width=1
        )
        trade_element = {
            "enter":enter,
            "exit":exit,
            "enter_ts":enter_ts,
            "exit_ts":exit_ts,
            "enter_p":enter_p,
            "exit_p":exit_p
        }
        res.append(trade_element)
    return res


    
def trade2plotelement_single(trade):
    res = []

    enter={
        "mode": "markers", 
        "name": "one_side", 
        "type": "scatter", 
        "x":[trade['entry_ts']],
        "y":[trade['entry_p']],
        "line_color":"green",
        "line":{
            "width":8
        }
    }
    exit={
        "mode": "markers", 
        "name": "one_side", 
        "type": "scatter", 
        "x":[trade['exit_ts']],
        "y":[trade['exit_p']],
        "line_color":"purple",
        "line":{
            "width":8
        }
    }
    enter_ts=dict(
        x0=trade['entry_ts'], 
        x1=trade['entry_ts'], 
        y0=0, y1=1, xref='x', yref='paper',
        line_width=1
    )
    exit_ts=dict(
        x0=trade['exit_ts'], 
        x1=trade['exit_ts'], 
        y0=0, y1=1, xref='x', yref='paper',
        line_width=1
    )
    enter_p=dict(
        y0=trade['entry_p'], 
        y1=trade['entry_p'], 
        x0=0, x1=1, xref='paper', yref='y',
        line_width=1
    )
    exit_p=dict(
        y0=trade['exit_p'], 
        y1=trade['exit_p'], 
        x0=0, x1=1, xref='paper', yref='y',
        line_width=1
    )
    trade_element = {
        "enter":enter,
        "exit":exit,
        "enter_ts":enter_ts,
        "exit_ts":exit_ts,
        "enter_p":enter_p,
        "exit_p":exit_p
    }
    res.append(trade_element)
    return res