'''
Created on Jun 4, 2020

@author: leon
'''
import plotly.graph_objects as go
from plotly.io import write_image
from version_master.version import imagine_folder


def plot_candle_stick_generic(
    df, 
    traces_map_external = {}, 
    trace_map_df ={},
    traces_style_map = {}, 
    image_path=None,
    title = 'default' # chart title
):
    '''
    2023-03-01
    
    This function plot candle stick, you can add extra trace externally or from df. You can also apply style
    traces_map_external = {}, # dict<name, dict<x,y>>
    trace_map_df ={}, # dict<df_col_name, x_name>
    traces_style_map = {}, # dict<name, dict<style_filed, style>> 
    
    # plotly reference:https://plotly.com/python/marker-style/, mode = markerrs/lines
    '''
    price_traces =go.Candlestick(
        x=df['est_datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
    )
    traces_map = {'ticket': price_traces}
    
    # add external trace
    for trace_name, trace in traces_map_external.items():
        x_list = list(trace.keys())
        y_list = list(trace.values())
        trace={
            "mode": "lines", 
            "name": trace_name, 
            "type": "scatter", 
            "x":x_list,
            "y":y_list,
            # "line_color":"purple",
            "line":{
                "width":1
            }
        }
        traces_map[trace_name]=trace
    
    # add df trace
    for y_col, x_col in trace_map_df.items():
        trace_from_df={
            "mode": "lines", 
            "name": y_col, 
            "type": "scatter", 
            "x":df[x_col],
            "y":df[y_col],
            "line_color":"royalblue",
            "line":{
                "width":1
            }
        }
        traces_map[y_col]=trace_from_df
        
    # apply all styles
    for trace_name, style in traces_style_map.items():
        for style_field, style_val in style.items():
            traces_map[trace_name][style_field] = style_val
    
    
    fig = go.Figure(data=list(traces_map.values()))
    fig.update_layout(title=title)
    fig.show()
    
    # save image if necessary
    if image_path != None:
        fig.write_html(image_path)
        
        
def plot_candle_stick(df, date_marker=[], date_marker2=[], ticker='default', path=None):
    price_traces =go.Candlestick(
        x=df['est_datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
    )
    
    trace_ema8={
        "mode": "lines", 
        "name": "ema8", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ema8'],
        "line_color":"royalblue",
        "line":{
            "width":1
        }
    }
    
    trace_ema21={
        "mode": "lines", 
        "name": "ema21", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ema21'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    
    trace_ma50={
        "mode": "lines", 
        "name": "ma50", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ma50'],
        "line_color":"red",
        "line":{
            "width":1
        }
    }

    # moving average trace
    trace = [
        price_traces, 
        trace_ema8, 
        trace_ema21, 
        trace_ma50
    ]

    fig = go.Figure(data=trace)
    for date in date_marker:
        fig.add_vline(x=date, line_width=1, line_dash="dash", line_color="blue")
        
    for date in date_marker2:
        fig.add_vline(x=date, line_width=1, line_dash="dash", line_color="red")
    
    fig.update_layout(title=ticker)
    

    

    if path is not None:
        fig.write_image(path)
    else:
        fig.show()

def plot_trades_simple_base(
    df, 
    enters={}, 
    exits={}, 
    ticker='default', 
    is_image=False, 
    image_folder=None,
    ma_only=False
):
    enter_x = []
    enter_y = []
    for x,y in enters.items():
        enter_x.append(x)
        enter_y.append(y)
    
    exit_x = []
    exit_y = []
    for x,y in exits.items():
        exit_x.append(x)
        exit_y.append(y)
        
    price_traces =go.Candlestick(
        x=df['est_datetime'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
    )
    
    trace_ema8={
        "mode": "lines", 
        "name": "ema8", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ema8'],
        "line_color":"royalblue",
        "line":{
            "width":1
        }
    }
    
    trace_ema21={
        "mode": "lines", 
        "name": "ema21", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ema21'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    
    trace_ma50={
        "mode": "lines", 
        "name": "ma50", 
        "type": "scatter", 
        "x":df['est_datetime'],
        "y":df['ma50'],
        "line_color":"red",
        "line":{
            "width":1
        }
    }
    
    trace_enter={
        "mode": "markers", 
        "name": "enter", 
        "type": "scatter", 
        "x":list(enter_x),
        "y":list(enter_y),
        "line_color":"purple",
        "line":{
            "width":1
        }
    }
    
    trace_exit={
        "mode": "markers", 
        "name": "exit", 
        "type": "scatter", 
        "x":list(exit_x),
        "y":list(exit_y),
        "line_color":"orange",
        "line":{
            "width":1
        }
    }


    # moving average trace
    trace = [
        trace_ema8, 
        trace_ema21, 
        trace_ma50,
        trace_enter,
        trace_exit
    ]
    
    if not ma_only:
        trace.append(price_traces)

    fig = go.Figure(data=trace)

    fig.update_layout(title=ticker)
    
    if not is_image:
        fig.show()
    else:
        img_path = imagine_folder + image_folder + '/' + ticker + '.png'
        fig.write_image(img_path)
        print('write to:' + img_path)


def plot_trades_simple(df, enters={}, exits={}, ticker='default', is_image=False, image_folder=None):
    plot_trades_simple_base(df, enters=enters, exits=exits, ticker=ticker, is_image=is_image, image_folder=image_folder)


def plot_trades_ma_only(df, enters={}, exits={}, ticker='default', is_image=False, image_folder=None):
    plot_trades_simple_base(df, enters=enters, exits=exits, ticker=ticker, is_image=is_image, image_folder=image_folder, ma_only=True)
    
    
def plot_line_from_xy_list(x_list, y_list, title='default'):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x_list, 
            y=y_list,
            mode='lines',
            name='lines'
        )
    )
    fig.update_layout(title=title)
    fig.show()
    

def plot_lines_from_xy_list(x_list, y_list_map, title='default', path=None):
    fig = go.Figure()
    for k, y_list in y_list_map.items():
        fig.add_trace(
            go.Scatter(
                x=x_list, 
                y=y_list,
                mode='lines',
                name=k
            )
        )
    fig.update_layout(title=title)
    
    if path is not None:
        fig.write_image(path)
    else:
        fig.show()
        

def plot_bars_from_xy_list(x_list, y_list, title='default', path=None):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=x_list, 
            y=y_list,
        )
    )
    fig.update_layout(title=title)

    if path is not None:
        # fig.write_image(path)
        fig.write_html(path)
    else:
        fig.show()
        
        
def plot_points_from_xy_list(x_list, y_list_map, title='default', path=None, mode='markers'):
    fig = go.Figure()
    for k, y_list in y_list_map.items():
        fig.add_trace(
            go.Scatter(
                x=x_list, 
                y=y_list,
                mode=mode,#??
                name=k
            )
        )
    fig.update_layout(title=title)
    
    if path is not None:
        # fig.write_image(path)
        fig.write_html(path)
    else:
        fig.show()
        
        
def plot_bar_set_from_xy_list(x_list, y_list_map, title='default', path=None):
    fig = go.Figure()
    for k, y_list in y_list_map.items():
        fig.add_trace(
            go.Bar(
                x=x_list, 
                y=y_list,
                name=k
            )
        )
        
    fig.update_layout(title=title)
    
    if path is not None:
        fig.write_html(path)
        # fig.write_image(path)
    else:
        fig.show()