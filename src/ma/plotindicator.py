import plotly.graph_objects as go
from _overlapped import NULL
from plotly.subplots import make_subplots

def gen_trade_plot(trades):
    res = {}
    win = {}
    lose = {}
    early_exit = {}
    
    win_improved_enter = {}
    win_improved_exit = {}
    
    lose_improved_enter = {}
    lose_improved_exit = {}
    
    for trade in trades:
        res[trade['enter_ts']]=trade['enter_p']
        res[trade['exit_ts']]=trade['exit_p']
        if 'drop_exit_ts' in trade.keys():
            early_exit[trade['drop_exit_ts']]=trade['drop_exit_p']
        if trade['label']:
            if 'entry_ts_improved' in trade.keys():
                win_improved_enter[trade['entry_ts_improved']] = trade['entry_p_improved']
                win_improved_exit[trade['exit_ts_improved']] = trade['exit_p_improved']
        else:
#             lose[trade['exit_ts']]=trade['exit_p']
            if 'entry_ts_improved' in trade.keys():
                lose_improved_enter[trade['entry_ts_improved']] = trade['entry_p_improved']
                lose_improved_exit[trade['exit_ts_improved']] = trade['exit_p_improved']
    
        if trade['pnl'] > 0: 
            win[trade['exit_ts']]=trade['exit_p']
        else:
            lose[trade['exit_ts']]=trade['exit_p']        
    
    return {
        'trade':res,
        'win':win,
        'lose':lose,
#         'early_exit':early_exit
        'win_enter':win_improved_enter,
        'win_exit':win_improved_exit,
        'lose_enter':lose_improved_enter,
        'lose_exit':lose_improved_exit,
    }

def plot_symbol(df_day ,ma_indicator,trades=NULL):

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
    
    trace = [
        price_traces, 
        trace_ema8, 
        trace_ema21, 
        trace_ma50,
    ]
    
    
    if ma_indicator is 'sequence_8_21':
        trace.append(trace_short_8_21)
        trace.append(trace_long_8_21)
    elif ma_indicator is 'sequence_8_21_50':
        trace.append(trace_short_8_21_50)
        trace.append(trace_long_8_21_50)
    elif ma_indicator is 'sequence_p_8_21':
        trace.append(trace_short_p_8_21)
        trace.append(trace_long_p_8_21)
        
    if trades is not NULL:
        print('plot trade line')
        trade_plot = gen_trade_plot(trades)
#         trace_early_exit={
#             "mode": "markers", 
#             "name": "early_exit", 
#             "type": "scatter", 
#             "x":list(trade_plot['early_exit'].keys()),
#             "y":list(trade_plot['early_exit'].values()),
#             "line_color":"blue",
#             "line":{
#                 "width":1
#             },
#             "marker":{
#                 "symbol" : 3
#             },
#         }

        trace_trade={
            "mode": "lines+markers", 
            "name": "trades", 
            "type": "scatter", 
            "x":list(trade_plot['trade'].keys()),
            "y":list(trade_plot['trade'].values()),
            "line_color":"black",
            "line":{
                "width":1
            }
        }
        trace_trade_end_win={
            "mode": "markers", 
            "name": "trades", 
            "type": "scatter", 
            "x":list(trade_plot['win'].keys()),
            "y":list(trade_plot['win'].values()),
            "line_color":"green",
            "line":{
                "width":1
            }
        }
        trace_trade_end_lose={
            "mode": "markers", 
            "name": "trades", 
            "type": "scatter", 
            "x":list(trade_plot['lose'].keys()),
            "y":list(trade_plot['lose'].values()),
            "line_color":"red",
            "line":{
                "width":1
            },

        }
        
        trace_improved_win_enter={
            "mode": "markers", 
            "name": "win_enter", 
            "type": "scatter", 
            "x":list(trade_plot['win_enter'].keys()),
            "y":list(trade_plot['win_enter'].values()),
            "line_color":"blue",
            "line":{
                "width":1
            },
            "marker":{
                "symbol" : 3
            },
        }
        
        trace_improved_win_exit={
            "mode": "markers", 
            "name": "win_exit", 
            "type": "scatter", 
            "x":list(trade_plot['win_exit'].keys()),
            "y":list(trade_plot['win_exit'].values()),
            "line_color":"blue",
            "line":{
                "width":1
            },
            "marker":{
                "symbol" : 4
            },
        }
        
        trace_improved_lose_enter={
            "mode": "markers", 
            "name": "lose_enter", 
            "type": "scatter", 
            "x":list(trade_plot['lose_enter'].keys()),
            "y":list(trade_plot['lose_enter'].values()),
            "line_color":"red",
            "line":{
                "width":1
            },
            "marker":{
                "symbol" : 3
            },
        }
        
        trace_improved_lose_exit={
            "mode": "markers", 
            "name": "lose_exit", 
            "type": "scatter", 
            "x":list(trade_plot['lose_exit'].keys()),
            "y":list(trade_plot['lose_exit'].values()),
            "line_color":"red",
            "line":{
                "width":1
            },
            "marker":{
                "symbol" : 4
            },
        }
        
        trace.append(trace_trade)
        trace.append(trace_trade_end_win)
        trace.append(trace_trade_end_lose)
        
        trace.append(trace_improved_win_enter)
        trace.append(trace_improved_win_exit)
        trace.append(trace_improved_lose_enter)
        trace.append(trace_improved_lose_exit)
#         trace.append(trace_early_exit)
    
    fig = go.Figure(
        data=trace,
    )
    fig.show()
    print('plot indicator, done!')
    
def plotpie(data,title):  

    data_sorted = {}
    for i in sorted (data) : 

        data_sorted[i] = data[i]
    values = list(data_sorted.values())

    
    fig = go.Figure(data=[go.Pie(labels=list(data_sorted.keys()), values=values,sort=False)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    fig.update_layout(title_text=title)
    fig.show()



# 
# def plot_minor_symbol(df_day ,ma_indicator,trades=NULL):
# 
#     price_traces =go.Candlestick(
#         x=df_day['est_datetime'],
#         open=df_day['open'],
#         high=df_day['high'],
#         low=df_day['low'],
#         close=df_day['close'],
#     )
#     trace_ema8={
#         "mode": "lines", 
#         "name": "ema8", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ema8'],
#         "line_color":"royalblue",
#         "line":{
#             "width":1
#         }
#     }
#     
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
#     
#     
#     trace_ema21={
#         "mode": "lines", 
#         "name": "ema21", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ema21'],
#         "line_color":"orange",
#         "line":{
#             "width":1
#         }
#     }
#     trace_ma50={
#         "mode": "lines", 
#         "name": "ma50", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ma50'],
#         "line_color":"red",
#         "line":{
#             "width":1
#         }
#     }
#     
#     # long short trace
#     trace_short_8_21_50={
#         "mode": "markers", 
#         "name": "short", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['sequence_8_21_50_short'],
#         "line_color":"purple",
#         "line":{
#             "width":1
#         }
#     }
#     trace_long_8_21_50={
#         "mode": "markers", 
#         "name": "long", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['sequence_8_21_50_long'],
#         "line_color":"orange",
#         "line":{
#             "width":1
#         }
#     }
#     
#     trace_short_8_21={
#         "mode": "markers", 
#         "name": "short", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['sequence_8_21_short'],
#         "line_color":"purple",
#         "line":{
#             "width":1
#         }
#     }
#     trace_long_8_21={
#         "mode": "markers", 
#         "name": "long", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['sequence_8_21_long'],
#         "line_color":"orange",
#         "line":{
#             "width":1
#         }
#     }
#     
#     trace = [
# #         price_traces, 
#         trace_ema8, 
#         trace_ema21, 
#         trace_ma50,
#     ]
#     
# #     
# #     if ma_indicator is 'sequence_8_21':
# #         trace.append(trace_short_8_21)
# #         trace.append(trace_long_8_21)
# #     elif ma_indicator is 'sequence_8_21_50':
# #         trace.append(trace_short_8_21_50)
# #         trace.append(trace_long_8_21_50)
#         
#     if trades is not NULL:
#         print('plot trade line')
#         trade_plot = gen_trade_plot(trades)
#         trace_trade={
#             "mode": "lines+markers", 
#             "name": "trades", 
#             "type": "scatter", 
#             "x":list(trade_plot['trade'].keys()),
#             "y":list(trade_plot['trade'].values()),
#             "line_color":"black",
#             "line":{
#                 "width":1
#             }
#         }
#         trace_trade_end_win={
#             "mode": "markers", 
#             "name": "trades", 
#             "type": "scatter", 
#             "x":list(trade_plot['win'].keys()),
#             "y":list(trade_plot['win'].values()),
#             "line_color":"green",
#             "line":{
#                 "width":1
#             }
#         }
#         trace_trade_end_lose={
#             "mode": "markers", 
#             "name": "trades", 
#             "type": "scatter", 
#             "x":list(trade_plot['lose'].keys()),
#             "y":list(trade_plot['lose'].values()),
#             "line_color":"red",
#             "line":{
#                 "width":1
#             },
# #             "marker":{
# #                 "symbol" : 3
# #             },
#         }
#         trace.append(trace_trade)
#         trace.append(trace_trade_end_win)
#         trace.append(trace_trade_end_lose)
#     
# #     fig = go.Figure(
# #         data=trace,
# #     )
#      
#     fig = make_subplots(rows=2, cols=1)
#     fig.add_trace(
#         trace_ema8_diff,
#         row=2, 
#         col=1
#     )
#     for t in trace:
#         fig.add_trace(
#             t,
#             row=1, 
#             col=1
#         )
# #     
#     fig.show()
#     print('plot indicator, done!')