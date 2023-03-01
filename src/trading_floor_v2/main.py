'''
Created on Mar 1, 2023

@author: spark
'''
import pandas as pd
import plotly.graph_objects as go
from trading_floor_v2.trading_infra_lib import run_trading_strategy
from util.general_ui import plot_candle_stick_generic
from util.util_pandas import df_to_dict


path_test = "C:/f_data/sector/indicator_day/XLF_1D_fmt_idc.csv"
df = pd.read_csv(path_test)

df_action = run_trading_strategy(df)
# df_action = pd.DataFrame(action_list)
print(df_action)


enter_df = df_action[df_action['action'] == 'enter']
exit_df = df_action[df_action['action'] == 'exit']


enter_dict = df_to_dict(enter_df, 'ts', 'price')
exit_dict = df_to_dict(exit_df, 'ts', 'price')

traces_map_external = {
    'enter': enter_dict,
    'exit': exit_dict
}

trace_map_df = {
    'ema21':'est_datetime',
    'ma50':'est_datetime'
}

traces_style_map = {
    'enter': {'mode':'markers', 'line_color':'purple','type':'scatter', 'marker_symbol': 'x'},
    'exit': {'mode':'markers', 'line_color':'yellow','type':'scatter'},
    'ema21': {'mode':'lines', 'line_color':'orange','type':'scatter'},
    'ma50': {'mode':'lines', 'line_color':'blue','type':'scatter'}
}





image_path = "C:/f_data/sector/debug2/img.html"
plot_candle_stick_generic(df)    
plot_candle_stick_generic(df, traces_map_external, trace_map_df, traces_style_map)