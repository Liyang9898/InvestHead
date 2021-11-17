'''
Created on Jun 4, 2020

@author: leon
'''
import plotly.graph_objects as go
from indicator_master.raw_stock_reader_lib import load_df_from_csv 
from indicator_master.indicator_compute_lib import add_indicator, datefilter

def plot_indicator(df_day, ma_indicator,ticker='default'):

    price_traces =go.Candlestick(
        x=df_day['est_datetime'],
        open=df_day['open'],
        high=df_day['high'],
        low=df_day['low'],
        close=df_day['close'],
    )
    
    price_high={
        "mode": "lines", 
        "name": "high", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['high'],
        "line_color":"royalblue",
        "line":{
            "width":1
        }
    }
        
    price_low={
        "mode": "lines", 
        "name": "low", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['low'],
        "line_color":"royalblue",
        "line":{
            "width":1
        }
    }
    
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

    trace_ema20={
        "mode": "lines", 
        "name": "ema20", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['ema20'],
        "line_color":"orange",
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
    
    
    trace_ema55={
        "mode": "lines", 
        "name": "ema55", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['ema55'],
        "line_color":"red",
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
    trace_na_8_21_50={
        "mode": "markers", 
        "name": "na", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_8_21_50_na'],
        "line_color":"blue",
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
    trace_na_8_21={
        "mode": "markers", 
        "name": "na", 
        "type": "scatter", 
        "x":df_day['est_datetime'],
        "y":df_day['sequence_8_21_na'],
        "line_color":"blue",
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
    
#     macd_positive={
#         "mode": "markers", 
#         "name": "macd_positive", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['macd_positive'],
#         "line_color":"red",
#         "line":{
#             "width":1
#         }
#     }
#     
#     macd_negative={
#         "mode": "markers", 
#         "name": "macd_negative", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['macd_negative'],
#         "line_color":"green",
#         "line":{
#             "width":1
#         }
#     }
    
#     enter_ui={
#         "mode": "markers", 
#         "name": "enter_ui", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['enter_ui'],
#         "line_color":"green",
#         "line":{
#             "width":1
#         }
#     }
     
    # ema 21 1 year
#     channel_100={
#         "mode": "markers", 
#         "name": "channel_100", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema21_percent_oneyear_channel_100'],
#         "line_color":"blue",
#         "marker_symbol":"x",
#         "line":{
#             "width":1
#         }
#     }
# 
#     channel_75={
#         "mode": "markers", 
#         "name": "channel_75", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema21_percent_oneyear_channel_75'],
#         "line_color":"blue",
#         "marker_symbol":"x",
#         "line":{
#             "width":1
#         }
#     }
# 
#     channel_50={
#         "mode": "markers", 
#         "name": "channel_50", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema21_percent_oneyear_channel_50'],
#         "line_color":"black",
#         "marker_symbol":"cross",
#         "line":{
#             "width":1
#         }
#     }
#     
#     channel_25={
#         "mode": "markers", 
#         "name": "channel_25", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema21_percent_oneyear_channel_25'],
#         "line_color":"blue",
#         "marker_symbol":"x",
#         "line":{
#             "width":1
#         }
#     }
#     
#     channel_0={
#         "mode": "markers", 
#         "name": "channel_0", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema21_percent_oneyear_channel_0'],
#         "line_color":"blue",
#         "marker_symbol":"x",
#         "line":{
#             "width":1
#         }
#     }
     

#     velocity={
#         "mode": "markers", 
#         "name": "velocity", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['velocity_ui'],
#         "line_color":"purple",
#         "marker_symbol":"x",
#         "line":{
#             "width":1
#         }
#     }
     

    
    
#     #channel low
#     barlow_2_ema8_channel_ceiling={
#         "mode": "markers", 
#         "name": "barlow_2_ema8_channel_ceiling", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema8_channel_ceiling'],
#         "line_color":"black",
#         "line":{
#             "width":1
#         }
#     }
#     
#     barlow_2_ema8_channel_floor={
#         "mode": "markers", 
#         "name": "barlow_2_ema8_channel_floor", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema8_channel_floor'],
#         "line_color":"black",
#         "line":{
#             "width":1
#         }
#     }
#     
#     barlow_2_ema8_channel_mp50_pos={
#         "mode": "markers", 
#         "name": "barlow_2_ema8_channel_mp50_pos", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema8_channel_mp50_pos'],
#         "marker_symbol":"cross",
#         "line_color":"black",
#         "line":{
#             "width":1
#         }
#     }
#     
#     barlow_2_ema8_channel_mp25_pos={
#         "mode": "markers", 
#         "name": "barlow_2_ema8_channel_mp25_pos", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema8_channel_mp25_pos'],
#         "marker_symbol":"cross",
#         "line_color":"blue",
#         "line":{
#             "width":1
#         }
#     }
#         
#     barlow_2_ema8_channel_mp75_pos={
#         "mode": "markers", 
#         "name": "barlow_2_ema8_channel_mp75_pos", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barlow_2_ema8_channel_mp75_pos'],
#         "marker_symbol":"cross",
#         "line_color":"blue",
#         "line":{
#             "width":1
#         }
#     }
#     
#     #channel high
#     barhigh_2_ema8_channel_ceiling={
#         "mode": "markers", 
#         "name": "barhigh_2_ema8_channel_ceiling", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barhigh_2_ema8_channel_ceiling'],
#         "line_color":"black",
#         "line":{
#             "width":1
#         }
#     }
#     
#     barhigh_2_ema8_channel_floor={
#         "mode": "markers", 
#         "name": "barhigh_2_ema8_channel_floor", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barhigh_2_ema8_channel_floor'],
#         "line_color":"black",
#         "line":{
#             "width":1
#         }
#     }
#     
#     barhigh_2_ema8_channel_mp50_pos={
#         "mode": "markers", 
#         "name": "barhigh_2_ema8_channel_mp50_pos", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barhigh_2_ema8_channel_mp50_pos'],
#         "marker_symbol":"cross",
#         "line_color":"black",
#         "line":{
#             "width":1
#         }
#     }
#     
#     barhigh_2_ema8_channel_mp25_pos={
#         "mode": "markers", 
#         "name": "barhigh_2_ema8_channel_mp25_pos", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barhigh_2_ema8_channel_mp25_pos'],
#         "marker_symbol":"cross",
#         "line_color":"blue",
#         "line":{
#             "width":1
#         }
#     }
#         
#     barhigh_2_ema8_channel_mp75_pos={
#         "mode": "markers", 
#         "name": "barhigh_2_ema8_channel_mp75_pos", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['barhigh_2_ema8_channel_mp75_pos'],
#         "marker_symbol":"cross",
#         "line_color":"blue",
#         "line":{
#             "width":1
#         }
#     }
    
#     ema55_20_gap_delta_up={
#         "mode": "markers", 
#         "name": "ema55_20_gap_delta_up", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ema55_20_gap_delta_up'],
#         "marker_symbol":"cross",
#         "line_color":"blue",
#         "line":{
#             "width":1
#         }
#     }
#     
#     ema55_20_gap_delta_down={
#         "mode": "markers", 
#         "name": "ema55_20_gap_delta_down", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ema55_20_gap_delta_down'],
#         "marker_symbol":"cross",
#         "line_color":"red",
#         "line":{
#             "width":1
#         }
#     }
#     
#     shrink_block_mark={
#         "mode": "markers", 
#         "name": "shrink_block_mark", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['shrink_block_mark'],
# #         "marker_symbol":"cross",
#         "line_color":"purple",
#         "line":{
#             "width":1
#         }
#     }
#     
#     ribbon_expand_seq_1st={
#         "mode": "markers", 
#         "name": "ribbon_expand_seq_1st", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ribbon_expand_seq_1st'],
#         "marker_symbol":"cross",
#         "line_color":"green",
#         "line":{
#             "width":1
#         }
#     }
#     ribbon_expand_seq_2st={
#         "mode": "markers", 
#         "name": "ribbon_expand_seq_2st", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ribbon_expand_seq_2st'],
#         "marker_symbol":"cross",
#         "line_color":"green",
#         "line":{
#             "width":1
#         }
#     }
#     ribbon_expand_seq_3st={
#         "mode": "markers", 
#         "name": "ribbon_expand_seq_3st", 
#         "type": "scatter", 
#         "x":df_day['est_datetime'],
#         "y":df_day['ribbon_expand_seq_3st'],
#         "marker_symbol":"cross",
#         "line_color":"green",
#         "line":{
#             "width":1
#         }
#     }
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
    
    # moving average trace
    trace = [
#         macd_positive,
#         macd_negative,
        price_traces, 
        trace_ema8, 
#         trace_ema20, 
        trace_ema21, 
#         trace_ema55,
        trace_ma50,
        
#         channel_0,
#         channel_25,
#         channel_50,
#         channel_75,
#         channel_100,
        
#         velocity
#         price_high,
#         price_low,

#         enter_ui,
#         up,
#         down,
#         channel_50
        
#         ema55_20_gap_delta_up,
#         ema55_20_gap_delta_down,
#         shrink_block_mark,
#         ribbon_expand_seq_1st,
#         ribbon_expand_seq_2st,
#         ribbon_expand_seq_3st,
        
#         barlow_2_ema8_channel_ceiling,
#         barlow_2_ema8_channel_floor,
#         barlow_2_ema8_channel_mp25_pos,
#         barlow_2_ema8_channel_mp50_pos,
#         barlow_2_ema8_channel_mp75_pos,
        
        
#         barhigh_2_ema8_channel_ceiling,
#         barhigh_2_ema8_channel_floor,
#         barhigh_2_ema8_channel_mp25_pos,
#         barhigh_2_ema8_channel_mp50_pos,
#         barhigh_2_ema8_channel_mp75_pos
    ]
    
    # long or short situation indicator
    if ma_indicator == 'sequence_8_21':
        trace.append(trace_short_8_21)
        trace.append(trace_long_8_21)
        trace.append(trace_na_8_21)
        
    elif ma_indicator == 'sequence_8_21_50':
        trace.append(trace_short_8_21_50)
        trace.append(trace_long_8_21_50)
        trace.append(trace_na_8_21_50)
        
    elif ma_indicator == 'sequence_p_8_21':
        trace.append(trace_short_p_8_21)
        trace.append(trace_long_p_8_21)
        
    fig = go.Figure(
        data=trace,
    )
    
    fig.update_layout(
        title=ticker
    )
    fig.show()



def plot_trades_entry(trades):
    return None

def plot_single_trade(trade):
    return None
############################################## test ###################################################
# path_test = """D:/f_data/BITSTAMP_BTCUSD, 60.csv"""
# df = load_df_from_csv(path_test)
# add_indicator(df)
# print(df['consecutive_sequence_8_21_cnt'])
# df_range = datefilter(df, '2019-10-01', '2019-10-15')
# plot_indicator(df_range, 'sequence_8_21')
############################################## test ###################################################
