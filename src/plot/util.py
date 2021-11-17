import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from plotly.graph_objs import layout
from collections import OrderedDict
import plotly.express as px



def histogram(points):
    fig = go.Figure(go.Histogram(x=points))
    fig.show()


def pnltimeseries(trades):

    res = {}
    for ds, trade in trades.items():
        pnl = trade['pnl']
        res[ds] = pnl
    return res


def pnlma(pnldic,ma_len):
    res_ma = {}
    rate_res = {}
    for end in range(ma_len-1,len(pnldic)-1):
        total_pnl = 0
        ma = 0
        p = 0
        n = 0
        for x in list(pnldic.values())[end - ma_len + 1:end+1]:
            total_pnl = total_pnl + x
            if x > 0:
                p = p +1 
            if x < 0:
                n=n + 1
        ma = total_pnl/ float(ma_len) /2 * 1000 * 20
        if float(p+n) == 0:
            rate = 0
        else:
            rate = float(p) / float(p+n)
        res_ma[list(pnldic.keys())[end]] = ma
        rate_res[list(pnldic.keys())[end]] = rate
    res = {
        'ma':res_ma,
        'rate':rate_res
    }
    return res

def pnltotaltimeseries(trades):
    total_pnl = 0
    res = {}
    
    # no commision
    for ds, trade in trades.items():
        pnl = trade['pnl']
        total_pnl = total_pnl + pnl
        res[ds] = total_pnl
    return res
    
#     # commision
#     for ds, trade in trades.items():
#         pnl = trade['pnl']
#         if pnl == 1:
#             pnl = (50.0-4.2)/50.0
#         total_pnl = total_pnl + pnl
#         res[ds] = total_pnl
#     return res


def pnldistribution(trades):
    total_pnl = 0
    res = {}
    for ds, trade in trades.items():
        pnl_decimal = trade['pnl']
        
        pnl = float(int(pnl_decimal * 2)) / 2
        
        if pnl in res:
            res[pnl] = res[pnl] + 1
        else:
            res[pnl] = 1
    b = OrderedDict(sorted(res.items()))
    return dict(b)
#     return res

def pnldistributionagg(trades):
    total_pnl = 0
    res = {}
    for ds, trade in trades.items():
        pnl_decimal = trade['pnl']
        
        pnl = float(int(pnl_decimal * 2)) / 2
        
        if pnl in res:
            res[pnl] = res[pnl] + 1
        else:
            res[pnl] = 1
    for k,v in res.items():
        res[k] = v * k
    b = OrderedDict(sorted(res.items()))
    return dict(b)




def plottimeseries(data, title):
    res_str = title
    for x in list(data.values()):
        if x > 0:
            res_str = res_str + '+'
        elif x < 0:
            res_str = res_str + 'X'
        else:
            res_str = res_str + '0'
    
    fig = go.Figure(data=go.Scatter(mode='lines+markers',x=list(data.keys()), y=list(data.values())))
    fig.update_layout(title=res_str)
    fig.show()
    
def plottimeseriesmultiline(datas, title):

    res_str = title
    lines = []
    for k,data in datas.items():
        if len (list(data.values())) is 0:
            continue
        avg = sum(list(data.values())) / len (list(data.values()))
        line = go.Scatter(name=k+' ma='+str(avg),mode='lines+markers',x=list(data.keys()), y=list(data.values()))
        lines.append(line)
    fig = go.Figure(data=lines)
    fig.update_layout(title=res_str)
    fig.show()
    
def plotcategory(data):
    
    fig = go.Figure([go.Bar(x=list(data.keys()), y=list(data.values()))])
    
    fig.show()
    
    
    
    
def plotpie(data,title):  
#     labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    values = list(data.values())
    values= [abs(v) for v in values] 
    
    fig = go.Figure(data=[go.Pie(labels=list(data.keys()), values=values,sort=False)])
    fig.update_traces(textposition='inside', textinfo='percent+label')
#     fig.update_layout(legend=data)
    fig.update_layout(title_text=title)
    fig.show()
    
    

def win_rate_ma_multi_trade_a_day(trades, ma_len):
    rate_res = {}
    dss = list(trades.keys())
    res_list = []
    for ds in dss:
        win=0
        lose=0
        neutral = 0
        
        for ts in trades[ds].keys():
            if trades[ds][ts]['pnl'] > 0:
                win = win + 1
            elif trades[ds][ts]['pnl'] < 0:
                lose = lose + 1
            else:
                neutral = neutral + 1
        res = {
            'win':win,
            'lose':lose,
            'neutral':neutral
        }
        res_list.append(res)
        
        print(ds + '_' + str(res))    
            
    for end in range(ma_len-1,len(res_list)-1):
        ma = 0
        p = 0
        n = 0
        for x in res_list[end - ma_len + 1:end+1]:
            p = p + x['win']
            n = n + x['lose']
        
        if float(p + n) > 0:
            ma = float(p) / float(p + n)
      
        rate_res[dss[end - ma_len + 1]] = ma

    return rate_res

# '''
# Created on Jan 12, 2020
# 
# @author: leon
# '''
# from plot.util import pnltimeseries, plottimeseries,pnltotaltimeseries,pnldistribution,plotcategory,pnldistributionagg,plotpie,pnlma,plottimeseriesmultiline
# 
# def compute_stat(trades):
#     pnldic = pnltimeseries(trades)
#     pnlaggdic = pnltotaltimeseries(trades)
#     pnlma_20 = pnlma(pnldic,20)
#     pnlma_10 = pnlma(pnldic,10)
#     pnlma_5 = pnlma(pnldic,5)
#     plottimeseries(pnldic,'daily pnl')
#     plottimeseries(pnlaggdic,'pnl agg')
#     # plottimeseries(pnlma_20,'ma20 pnl')
#     # plottimeseries(pnlma_10,'ma10 pnl')
#     # plottimeseries(pnlma_5,'ma5 pnl')
#     plottimeseriesmultiline({'ma20':pnlma_20['ma'],'ma10':pnlma_10['ma'],'ma5':pnlma_5['ma']},'ma pnl')
#     plottimeseriesmultiline({'rate20':pnlma_20['rate'],'rate10':pnlma_10['rate'],'rate5':pnlma_5['rate']},'ma pnl')
#     dis = pnldistribution(trades)
#     disagg = pnldistributionagg(trades)
#     # plotcategory(dis)
#     # plotcategory(disagg)
#     plotpie(dis, 'change')
#     plotpie(disagg, 'amount of money')