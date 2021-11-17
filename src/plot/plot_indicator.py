import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from plotly.subplots import make_subplots


def gendatetime(date_str, time_str):
    s=date_str+' '+time_str
    p='%d/%m/%Y  %H:%M:%S'
    return datetime.strptime(s, p)

def bbpabs(up, low, base,bbp):
#     if bbp > 0:
        return (up - low) * bbp + low
#     elif bbp < 0:
#         return (up - low) * bbp + low
#     else:
#         return base

def normalize_ma_in_bb(up, low, ma):
    return (ma - low) / (up - low)

def validpoint(ma8, ma21, ma17, bb):
    if (ma8 < ma21 and ma17 < bb):
        return -1
    elif (ma8 > ma21 and ma17 > bb):
        return 1
    else:
        return 0
    
def validlongplot(valid, close):
    if valid > 0:
        return close
        
def validshortplot(valid, close):
    if valid < 0:
        return close

    
def plot_chart_indi(df_day, ds):
    price_traces =go.Candlestick(
        x=df_day['est_time'],
        open=df_day['open'],
        high=df_day['high'],
        low=df_day['low'],
        close=df_day['close'],
        name=ds,
    )
    ma8 =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['ma8'],
        mode='lines',
        name='ma8'
    )
    ma17 =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['ma17'],
        mode='lines',
        name='ma17'
    )
    
    ma21 =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['ma21'],
        mode='lines',
        name='ma21'
    )
    
    valid_long =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['validlongplot'],
        mode='markers',
        name='valid_long'
    )
    
    valid_short =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['validshortplot'],
        mode='markers',
        name='valid_short'
    )
        
    fig = go.Figure(
        data=[price_traces,ma8,ma21,ma17,valid_long,valid_short],
    )
    fig.update_layout(
        title=ds,
        height=800, 
        width=1200,
        shapes=[],
    )
    fig.show()
    
    
def plot_ma_bb(df_day, ds):
    ma17_nor =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['ma17_nor'],
        mode='lines',
        name='ma17'
    )
    
    bb =go.Scatter(
        x=df_day['est_time'], 
        y=df_day['bb'],
        mode='lines',
        name='bbp'
    )
    fig = go.Figure(
        data=[bb,ma17_nor],
    )
    fig.update_layout(
        title=ds,
        height=800, 
        width=1200,
        shapes=[],
    )
    fig.show()