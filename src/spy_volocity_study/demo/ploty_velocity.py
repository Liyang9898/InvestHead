import pandas as pd
import numpy as np
import plotly.graph_objects as go
from spy_volocity_study.lib.constant import adjustments, S, S2, E, LABEL_ADJUST
from spy_volocity_study.lib.labeling import labeling_adjust_signal_range
from spy_volocity_study.lib.ploty import ploty_velocity_adjust_ui
from util.util import get_all_weekdays, df_date_filter


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

df = df_date_filter(df, 'date', '2019-08-01', '2022-04-08')

ploty_velocity_adjust_ui(df, col_names, adjustments)