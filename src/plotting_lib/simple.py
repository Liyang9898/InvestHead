'''
Created on Dec 23, 2020

@author: leon
'''
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
# from batch_20201214.analysis.compare_with_without_channel_enter import res



def moving_window_batch(dic, window_option, csv_path):
    res = {}
    
    for window in window_option:
        res_w = moving_window(dic, window)
        res[window] = res_w
        
    df = pd.DataFrame(list(res.values()))
    df.to_csv(csv_path, index=False)
    return res

def moving_window(dic, window):
    diff_sum = 0
    cnt = 0
    positive = 0
    pnl_list = []
    l = [] # value sorted by time
    for key in sorted(dic.keys()):
        l.append(dic[key])
    # loop
    left = 0
    right = len(l) - window
    window_lefts = list(range(right+1))

    for window_left in window_lefts:
        # between window_left and window_left + window-1
        # get diff, get positive
        a = l[window_left]
        b = l[window_left + window-1]
        diff = b *1.0 / a - 1
        pnl_list.append(diff)
        diff_sum = diff_sum + diff
        if b>a:
            positive = positive + 1
        cnt = cnt + 1
    positive_rate = positive*1.0/cnt
    window_pnl_p_avg = diff_sum / cnt
    

    pnl_lost_str = ','.join(str(x) for x in pnl_list)
    return {
        "window":window,
        "positive_rate":positive_rate,
        "window_pnl_p_avg":window_pnl_p_avg,
        "pnl_list":pnl_lost_str
    }
    
def dip_measure(dic):
    l = [] # value sorted by time
    for key in sorted(dic.keys()):
        l.append(key)
    top = 1
    max_time_between_top = 0
    time_between_top=0
    max_dip = 0
    max_gap_exit_date = ''
    max_dip_bottom_ts = ''
    for t in l:
        p = dic[t]
        if p < top:
            
            time_between_top=time_between_top+1
            gap = top - p
            gap_p = gap * 1.0 / top
            if gap_p > max_dip:
                max_dip = gap_p
                max_dip_bottom_ts = t
        else:
            top = p
            if time_between_top > max_time_between_top:
                max_time_between_top = time_between_top
                max_gap_exit_date = t
            time_between_top=0    
    return {
        'max_dip_time':max_time_between_top,
        'max_dip':max_dip,
        'max_dip_exit_ts':max_gap_exit_date,
        'max_dip_bottom_ts':max_dip_bottom_ts
    }
    
# def plotTimeSerisDic(dic):
#     data = {'ts': list(dic.keys()), 'val': list(dic.values())}
#     df=pd.DataFrame.from_dict(data)
#     fig = px.line(df, x='ts', y="val")
#     fig.show()



# Create random data with numpy
def plotTimeSerisDic(dic):

    fig = go.Figure()

#         print(dic)
#     fig.add_trace(go.Scatter(x=list(dic.keys()), y=list(dic.values()),
#                         mode='lines',
#                         name='lines'))
#     fig.add_trace(go.Scatter(x=random_x, y=random_y1,
#                         mode='lines+markers',
#                         name='lines+markers'))
    fig.add_trace(go.Scatter(x=list(dic.keys()), y=list(dic.values()),
                        mode='markers', name='markers'))
    
    fig.show()
    
def plotTimeSerisDic3(dic1,dic2,dic3,ticker='default'):

    fig = go.Figure()


    fig.add_trace(go.Scatter(x=list(dic1.keys()), y=list(dic1.values()),
                        mode='markers', name='price'))
    fig.add_trace(go.Scatter(x=list(dic2.keys()), y=list(dic2.values()),
                        mode='markers', name='fix'))
    fig.add_trace(go.Scatter(x=list(dic3.keys()), y=list(dic3.values()),
                        mode='markers', name='rollover'))
    fig.update_layout(
        title=ticker
    )

    fig.show()
    