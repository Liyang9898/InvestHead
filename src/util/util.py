'''
Created on Jun 9, 2020

@author: leon
'''
from datetime import timedelta, datetime
import os
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import random
import json

PX_PERCENT_HIST = 'percent'


def get_all_csv_file_path_from_folder(stock_ticker_with_indicator_folder):
    filepath_list={}
    for file in os.listdir(stock_ticker_with_indicator_folder):
        if file.endswith(".csv"):
            file_path=stock_ticker_with_indicator_folder+file
            filepath_list[file]=file_path
    return filepath_list

def extract_symbol_name(file_name):
    substring = '_'
    idx = file_name.find(substring)
    return file_name[:idx]

def load_df_from_csv(filepath,cols):
    path = filepath
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=cols
    )
    return df

def encode_dict(d):
    s = ""
    for k,v in d.items():
        s = s + str(k)+":"+str(v)+","
    return s

def decode_dict(s):
    tokens = s.split(",")
    d = {}
    for pair in tokens:
        if pair == "":
            continue
        kv = pair.split(":")
        d[kv[0]]=kv[1]
    return d

def get_volume_map():
    path_out = """D:/f_data/volume_all_ticker.csv"""
    mmap = {}
    df = pd.read_csv(
        path_out,
        sep=',',
        header=0,
        names=['ticker','vol']
    )
    for i in range(0, len(df)):
        mmap[df.loc[i, 'ticker']]= df.loc[i, 'vol'] 

    return mmap


def get_ticker_larger_than_vol(vol_threshold, vol_map):
    l = []
    for k, v in vol_map.items():
        if v > vol_threshold:
            l.append(k)
    return l


def printTradesSummary(
    win_rate,
    lose_rate,
    neutral_rate,
    total_trades,
    bar_count,
    win,
    win_pnl,
    win_pnl_p,
    lose,
    lose_pnl,
    lose_pnl_p,
    neutral,
    roll_over_pnl_p,
    total_pnl,
    win_average_pnl,
    lose_average_pnl,
    win_lose_pnl_ratio,
    strategy_params  # this is a dict [string, num]
):
    win_lose_rate_diff = win_rate-lose_rate
    pnl_diff=win_pnl_p+lose_pnl_p
    roll_over_pnl_p_delta = roll_over_pnl_p-1
    trade_summary_str="""
    win trades:{win}({win_rate}), lose trades:{lose}({lose_rate}), 
    --------------------------------------------------------------------------
    win avg size:({win_average_pnl}), lose avg size:({lose_average_pnl}), 
    --------------------------------------------------------------------------
    win_lose_pnl_ratio:({win_lose_pnl_ratio}), 
    --------------------------------------------------------------------------
    neutral trades:{neutral}({neutral_rate}), win-lose: {win_lose_rate_diff}
    --------------------------------------------------------------------------
    win_pnl:{win_pnl_p}, lose_pnl:{lose_pnl_p}, total_pnl:{pnl_diff}, snowball_pnl:{roll_over_pnl_p_delta}
    --------------------------------------------------------------------------
    win_points:{win_pnl},lose_points: {lose_pnl},all_points_mades: {total_pnl}
    --------------------------------------------------------------------------
    total trades:{total},bar_count: {bar_count}
    --------------------------------------------------------------------------
    strategy_params:{strategy_params}
    """.format(
        win_lose_rate_diff="{:.2%}".format(win_lose_rate_diff),
        win_rate="{:.2%}".format(win_rate),
        lose_rate="{:.2%}".format(lose_rate),
        neutral_rate="{:.2%}".format(neutral_rate),
        total=total_trades,
        bar_count=bar_count,
        win=win,
        win_pnl=int(win_pnl),
        win_pnl_p="{:.2%}".format(win_pnl_p),
        lose=lose,
        lose_pnl=int(lose_pnl),
        lose_pnl_p="{:.2%}".format(lose_pnl_p),
        pnl_diff="{:.2%}".format(pnl_diff),
        neutral=neutral,
        roll_over_pnl_p_delta="{:.2%}".format(roll_over_pnl_p_delta),
        total_pnl=int(total_pnl),
        win_average_pnl="{:.2%}".format(win_average_pnl),
        lose_average_pnl="{:.2%}".format(lose_average_pnl),
        win_lose_pnl_ratio = round(win_lose_pnl_ratio, 2),
        strategy_params=encode_dict(strategy_params)
    )
    return trade_summary_str

def print_trade(
    pnl,
    pnl_percent,
    direction,
    bar_duration,
    entry_price,
    entry_ts,
    exit_price,
    exit_ts,
    best_potential_pnl_percent
):
    result = "Win" 
    if pnl < 0:
        result = "Lose"
    elif pnl == 0:
        result = "Neutral"
        
    direction_str = "Long" if direction == 1 else "Short"
    trade_str="{result}, {direction_str}, {pnl_percent}({pnl}), {duration} bars,     in:{entry_price} ({entry_ts})   out:{exit_price} ({exit_ts})  best pnl%:{best_pnl_p}".format(
        result=result,
        direction_str=direction_str,
        pnl_percent="{:.2%}".format(pnl_percent),
        pnl=str(round(pnl, 2)),
        duration=bar_duration,
        entry_price=str(round(entry_price, 2)),
        entry_ts=entry_ts,
        exit_price=str(round(exit_price, 2)),
        exit_ts=exit_ts,
        best_pnl_p="{:.2%}".format(best_potential_pnl_percent),
    )
    return trade_str

def bracket_value_in_dict(d):
    for k,v in d.items():
        d[k]=[v]
        
def fist_value_in_dict(d):
    for k,v in d.items():
        d[k]=v[0]
        
           
def plus_day(date_str, days):
    date_1 = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    end_date = date_1 + datetime.timedelta(days)
    end_date_str = end_date.strftime("%Y-%m-%d")
    return end_date_str

def make_date_chain(start,end,gap):
    res = []
    cur_str = start
    while(cur_str<=end):
        res.append(cur_str)
        date_1 = datetime.datetime.strptime(cur_str, "%Y-%m-%d")
        end_date = date_1 + datetime.timedelta(gap)
        end_date_str = end_date.strftime("%Y-%m-%d")
        cur_str=end_date_str
    return res
        
def plot_time_series(df, col):
    fig = px.scatter(df, x="ts", y=col).update_traces(mode="lines+markers")
    fig.show()
    
def percent_str(n):
    return "{:.2%}".format(n)


def get_all_weekdays(s, e):
    sdate = datetime.strptime(s, '%Y-%m-%d').date()
    edate = datetime.strptime(e, '%Y-%m-%d').date()

    delta = edate - sdate       # as timedelta
    res = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        if day.weekday()>=5:
            continue
        res.append(str(day))

    return res


def get_certain_weekdays(
    s, 
    e, 
    weekday_id  # Monday = 0 Sunday = 6
):
    sdate = datetime.strptime(s, '%Y-%m-%d').date()
    edate = datetime.strptime(e, '%Y-%m-%d').date()

    delta = edate - sdate       # as timedelta
    res = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        if day.weekday()!=weekday_id:
            continue
        res.append(str(day))

    return res


def holding_days(s,e):    
    return day_gap(s,e)


def day_gap(s,e):
    sdate = datetime.strptime(s.split(' ')[0], '%Y-%m-%d').date()
    edate = datetime.strptime(e.split(' ')[0], '%Y-%m-%d').date()

    delta = edate - sdate      
    return int(delta.days)


def float_to_percent_str(x):
    return "{p}%".format(p=round(x*100.0,2))


def sort_dic_by_val(dic, descending=False):
    if len(dic)==0:
        return dic
    
    # sort
    sort_dic = sorted(dic.items(), key=lambda x: x[1], reverse=descending)
    res = {}
    for x in sort_dic:
        k=x[0]
        v=x[1]
        res[k]=v

    # validation
    assert len(dic) == len(res)
    pre_v = list(res.values())[0]
    for k,v in res.items():
        if not descending:
            assert v >= pre_v
        else:
            assert v <= pre_v
        pre_v=v
    return res


def sort_dic_by_key(dic, descending=False):
    keys = list(dic.keys())
    keys.sort(reverse=descending)
    res = {}
    for k in keys:
        res[k] = dic[k]
    return res


def print_dict(d):
    for k, v in d.items():
        print(k, v)
        
        
def plotly_color():
    return px.colors.qualitative.Plotly
    

def print_sep_line(info):
    width = 142
    info_width = len(info) + 2
    len_side = (width - info_width) / 2
    start_on_side = "*" * int(len_side)
    print(f"{start_on_side} {info} {start_on_side}")
    
    
def df_date_filter(df, date_col, s, e):
    # date format: yyyy-mm-dd
    df = df[(df[date_col] >= s) & (df[date_col] <= e)]
    return df


def df_date_index_mapping(df):
    res = {}
    for idx in range(0, len(df)):
        date = df.loc[idx, 'date']
        if date in res:
            raise Exception('Duplicate date in stock rows')
        res[date] = idx
    return res


def percentile_from_list(input,descending=False):
    # default is ascending order
    l=input.copy()
    l.sort(reverse=descending)
    total = len(l)-1
    res = {}
    for i in range(0, 110, 10):
        idx = int(i * 1.0 / 100 * total)
        res[i] = l[idx]
    return res


def delta_df(df, col):
    col_d = f"{col}_delta"
    df[col_d] = np.nan
    for i in range(1, len(df)):
        df.loc[i, col_d] = (df.loc[i, col] - df.loc[i - 1, col]) / df.loc[i - 1, col]
        

def df_2col_to_dic(df, key, val):
    res = {}
    for i in range(0, len(df)):
        date=df.loc[i, key]
        p=df.loc[i, val]
        res[date]=p
    return res


def plot_hist_from_df_col(df, col, bin_size, title):
    x = df[col].to_list()
    xbins=dict(size=bin_size)
    fig = go.Figure(data=[go.Histogram(x=x, xbins=xbins, histnorm='percent')])
    fig.update_layout(title_text=title)
    fig.show()
    
    
def plot_line_chart_from_df_col(df, x_col, y_cols, title='please enter title'):
    fig = go.Figure()
    for y_col in y_cols:
        trace = go.Scatter(
            x=df[x_col], 
            y=df[y_col],
            mode='markers', #lines+markers, markers, lines
            name='y_col'
        )
        fig.add_trace(trace)
        
    fig.update_layout(title=title, xaxis_title=x_col)    
    fig.show()


def interval_boundary(interval):
    if interval is np.nan:
        return np.nan
    else:
        s = str(interval)
        s = s[1:-1]
        tokens = s.split(',')
        return [float(tokens[0]), float(tokens[1])]
    
    
def get_bucket_mid(min, max, x, bin_size):
    if np.isnan(x):
        return x
    absolute = x-min

    chunk_cnt = int(absolute/bin_size)
    low = chunk_cnt * bin_size
    high = chunk_cnt * bin_size + bin_size
    mid = chunk_cnt * bin_size + bin_size * 0.5
    return mid


def extract_sub_df_single_st_based_on_period(df, date_col, position_col, period):
    df=df.copy()
    df.sort_values(by=['date'], inplace=True)
    if period == 'year':
        df_r = df[df['year_start'] == True].copy()
    elif period == 'month':
        df_r = df[df['month_start'] == True].copy()
    elif period == 'week':
        df_r = df[df['week_start'] == True].copy()
    

    df_r.rename(columns={position_col: 'position'}, inplace=True)
    
    df_r.reset_index(inplace=True, drop=True) 
    df_r = df_r[[date_col, 'position']]
    df_r = df_r.copy()
    return df_r


def gen_random_str():
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
    r_str = str(int(random.random()*10000))
    return f'{now_str}_{r_str}'
    

# def create_perf_compare_folder():
#     # root, price, position, result, picture
#     
#     root = 'D:/f_data/perf_compare/'
#     return 


def str_to_txt(content, path):    
    text_file = open(path, "w")
     
    #write string to file
    text_file.write(content)
     
    #close file
    text_file.close()