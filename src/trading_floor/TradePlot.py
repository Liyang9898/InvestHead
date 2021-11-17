'''
Created on Jun 7, 2020

@author: leon
'''

from indicator_master.indicator_compute_lib import add_indicator, datefilter
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from util.util import plot_hist_from_df_col


def plot_trades(
    df_day, 
    ma_indicator, 
    trade_bundle,
    entry_only=False,
    ticker='default'
):
    trade_bundle.genAllPlotDataMap()
    
    price_traces =go.Candlestick(
        x=df_day['est_datetime'],
        open=df_day['open'],
        high=df_day['high'],
        low=df_day['low'],
        close=df_day['close'],
    )
    trace_ema8={
        "mode": "lines", 
        "name": "ema8", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['ema8'],
        "line_color":"royalblue",
        "line":{
            "width":1
        }
    }
    
#     trace_ema8_diff={
#         "mode": "lines", 
#         "name": "ema8_diff", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ema8_diff'],
#         "line_color":"royalblue",
#         "line":{
#             "width":1
#         }
#     }
    trace_ema8_predict={
        "mode": "lines", 
        "name": "ema8_predict", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['ema8_1day_projectile'],
        "line_color":"black",
        "line":{
            "width":1
        }
    }
    
    trace_ema21={
        "mode": "lines", 
        "name": "ema21", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['ema21'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    trace_ma50={
        "mode": "lines", 
        "name": "ma50", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['ma50'],
        "line_color":"red",
        "line":{
            "width":1
        }
    }
    
    # long short trace
    trace_short_8_21_50={
        "mode": "markers", 
        "name": "short", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_8_21_50_short'],
        "line_color":"purple",
        "line":{
            "width":1
        }
    }
    trace_long_8_21_50={
        "mode": "markers", 
        "name": "long", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_8_21_50_long'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    
    trace_short_8_21={
        "mode": "markers", 
        "name": "short", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_8_21_short'],
        "line_color":"purple",
        "line":{
            "width":1
        }
    }
    trace_long_8_21={
        "mode": "markers", 
        "name": "long", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_8_21_long'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    
    trace_short_p_8_21={
        "mode": "markers", 
        "name": "short", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_p_8_21_short'],
        "line_color":"purple",
        "line":{
            "width":1
        }
    }
    trace_long_p_8_21={
        "mode": "markers", 
        "name": "long", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_p_8_21_long'],
        "line_color":"orange",
        "line":{
            "width":1
        }
    }
    
#   debug only: plot first x  bar in continues long or short
#     consecutive_sequence_8_21_cnt={
#         "mode": "markers", 
#         "name": "consecutive_sequence_8_21_cnt", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['consecutive_sequence_8_21_cnt_plot'],
#         "line_color":"blue",
#         "line":{
#             "width":4
#         }
#     }
    
    win_entry={
        "mode": "markers", 
        "name": "win_entry", 
        "type": "scatter", 
        "x":list(trade_bundle.win_entry_plots.keys()),
        "y":list(trade_bundle.win_entry_plots.values()),
        "line_color":"blue",
        "line":{
            "width":1
        }
    }
    
    win_exit={
        "mode": "markers", 
        "name": "win_exit", 
        "type": "scatter", 
        "x":list(trade_bundle.win_exit_plots.keys()),
        "y":list(trade_bundle.win_exit_plots.values()),
        "line_color":"blue",
        "line":{
            "width":1
        },
        "marker":{
            "symbol" : 4
        },
    }
    
    lose_entry={
        "mode": "markers", 
        "name": "lose_entry", 
        "type": "scatter", 
        "x":list(trade_bundle.lose_entry_plots.keys()),
        "y":list(trade_bundle.lose_entry_plots.values()),
        "line_color":"orange",
        "line":{
            "width":1
        },
    }
    
    lose_exit={
        "mode": "markers", 
        "name": "lose_exit", 
        "type": "scatter", 
        "x":list(trade_bundle.lose_exit_plots.keys()),
        "y":list(trade_bundle.lose_exit_plots.values()),
        "line_color":"orange",
        "line":{
            "width":1
        },
        "marker":{
            "symbol" : 4
        },
    }
    
    neutral_entry={
        "mode": "markers", 
        "name": "neutral_entry", 
        "type": "scatter", 
        "x":list(trade_bundle.neutral_entry_plots.keys()),
        "y":list(trade_bundle.neutral_entry_plots.values()),
        "line_color":"black",
        "line":{
            "width":1
        },
    }
    
    neutral_exit={
        "mode": "markers", 
        "name": "neutral_exit", 
        "type": "scatter", 
        "x":list(trade_bundle.neutral_exit_plots.keys()),
        "y":list(trade_bundle.neutral_exit_plots.values()),
        "line_color":"black",
        "line":{
            "width":1
        },
        "marker":{
            "symbol" : 4
        },
    }
    
    trace = [
        price_traces, 
        # moving average trace
        trace_ema8, 
        trace_ema8_predict,
        trace_ema21, 
        trace_ma50,
        # trades plot
        win_entry,
        lose_entry,
        neutral_entry,
    ]
    
    if entry_only is False:
        trace.append(win_exit)
        trace.append(lose_exit)
        trace.append(neutral_exit)
     

    # long or short situation indicator
    if ma_indicator == 'sequence_8_21':
        trace.append(trace_short_8_21)
        trace.append(trace_long_8_21)
    elif ma_indicator == 'sequence_8_21_50':
        trace.append(trace_short_8_21_50)
        trace.append(trace_long_8_21_50)
    elif ma_indicator == 'sequence_p_8_21':
        trace.append(trace_short_p_8_21)
        trace.append(trace_long_p_8_21)
        
        
    fig = go.Figure(
        data=trace,
#         title = ticker
    )
    
    fig.update_layout(
        title=ticker
    )
    fig.show()
    
    
def label_distribution_on_feature(
    df,
    feature
):    
    fig = px.histogram(df, x=feature, color="label")

    fig.update_layout(
        barmode="overlay",
        bargap=0.1
    )
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    fig.show()
    

def distribution_on_feature(
    df,
    feature
):    
    fig = px.histogram(df, x=feature)

    fig.update_layout(
        barmode="overlay",
        bargap=0.1
    )
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.75)
    fig.show()

    
    
    
    
#     x0 = np.random.randn(500)
#     # Add 1 to shift the mean of the Gaussian distribution
#     x1 = np.random.randn(500) + 1
#     
#     fig = go.Figure()
#     fig.add_trace(go.Histogram(x=x0))
#     fig.add_trace(go.Histogram(x=x1))
#     
#     # Overlay both histograms
#     fig.update_layout(barmode='overlay')
#     # Reduce opacity to see both histograms
#     fig.update_traces(opacity=0.75)
#     fig.show()


def plot_win_lose_trade_size(df):
    df_win = df[df['pnl_percent']>0]
    df_lose = df[df['pnl_percent']<0]
    plot_hist_from_df_col(df=df_win, col='pnl_percent', bin_size=0.01, title='win')
    plot_hist_from_df_col(df=df_lose, col='pnl_percent', bin_size=0.01, title='lose')