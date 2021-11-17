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

df = df_date_filter(df, 'date', '2020-08-01', '2021-04-08')

labeling_adjust_signal_range(df, adjustments)
df2 = df[df[LABEL_ADJUST]==np.nan]
print(df2['date'])


    
# 



def foo(df, feature_col, label_col, threshold):
    t_p = df[(df[feature_col] >= threshold) & (df[label_col] == True)]
    f_p = df[(df[feature_col] >= threshold) & (df[label_col] == False)]
    t_n = df[(df[feature_col] < threshold) & (df[label_col] == False)]
    f_n = df[(df[feature_col] < threshold) & (df[label_col] == True)]
    
    # when above threshold, how many are real adjustment?
    total = len(t_p) + len(f_p)
    res = {
        'total': total,
        'adjust': len(t_p) / total,
        'not_adjust': len(f_p) / total
    }
    return res

x = foo(df, 'p_delta_1d_pct', LABEL_ADJUST, 0.02)
print(x)