from consequence.causal.causal_velocity import gen_event_p_delta_1d_pct_drop
from consequence.effect.effect_lower_than_close import min_price_future
from consequence.lib.ce_velocity_to_lower_than_signal_bar_close import velocity_to_lower_than_signal_bar_close
import pandas as pd
import plotly.express as px
from util.general_ui import plot_candle_stick
from util.util import df_date_filter, df_date_index_mapping, PX_PERCENT_HIST


st_path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
col_names = [
    'p_delta_oc_pct',
    'p_delta_1d_pct',
    'p_delta_2d_pct',
    'p_delta_3d_pct',
    'p_delta_5d_pct',
    'p_delta_10d_pct',
    'p_delta_20d_pct',  
]


df = pd.read_csv(st_path)
df = df_date_filter(df, 'date', '2016-05-16', '2021-05-16')
df.reset_index(inplace=True, drop=True)

signal = 'p_delta_1d_pct'
threshold_causal = -0.017 # down of the signal
threshold_effect = -0.005 # down of the effect

observe_range = 20 # number of days to cover in observing what will happen
date_idx_map = df_date_index_mapping(df)

df_th = velocity_to_lower_than_signal_bar_close(df, date_idx_map, signal, threshold_causal, observe_range, False)
print(df_th)

within_1p = df_th[df_th['val'] >= threshold_effect]
within_1p_dates = within_1p['event_date'].to_list()

beyond_1p = df_th[df_th['val'] < threshold_effect]
beyond_1p_dates = beyond_1p['event_date'].to_list()

above = len(within_1p)
below = len(beyond_1p)
total = above + below
print(total, below/total)
 
# plot_candle_stick(
#     df=df,
#     date_marker=within_1p_dates,
# )
# 
# plot_candle_stick(
#     df=df,
#     date_marker=beyond_1p_dates
# )