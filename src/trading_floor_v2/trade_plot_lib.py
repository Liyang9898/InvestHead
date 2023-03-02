'''
Created on Mar 1, 2023

@author: spark
'''
from util.general_ui import plot_candle_stick_generic
from util.util_pandas import df_to_dict


def plot_trades(df_ticker, df_trades, img_path=None):
    enter_dict = df_to_dict(df_trades, 'ts_enter', 'price_enter')
    exit_dict = df_to_dict(df_trades, 'ts_exit', 'price_exit')
    
    traces_map_external = {
        'enter': enter_dict,
        'exit': exit_dict
    }
    
    trace_map_df = {
        'ema21':'est_datetime',
        'ma50':'est_datetime'
    }
    
    traces_style_map = {
        'enter': {'mode':'markers', 'line_color':'purple','type':'scatter'},
        'exit': {'mode':'markers', 'line_color':'yellow','type':'scatter', 'marker_symbol': 'x'},
        'ema21': {'mode':'lines', 'line_color':'orange','type':'scatter'},
        'ma50': {'mode':'lines', 'line_color':'blue','type':'scatter'}
    }
         
         

    # traces = {}
    # for i in range(0, len(df_trades)):
    #     t1 = df_trades.loc[i, 'ts_enter']
    #     t2 = df_trades.loc[i, 'ts_exit']
    #     p1 = df_trades.loc[i, 'price_enter']
    #     p2 = df_trades.loc[i, 'price_exit']
    #     trace = {t1:p1, t2:p2}
    #     traces[t1] = trace
    # traces_map_external = traces 
    
         
    plot_candle_stick_generic(
        df=df_ticker, 
        traces_map_external=traces_map_external, 
        trace_map_df=trace_map_df,
        traces_style_map=traces_style_map, 
        image_path=img_path,
        title = 'Trades'
    )
    


    
    