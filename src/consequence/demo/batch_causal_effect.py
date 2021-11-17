from consequence.causal.causal_velocity import gen_event_p_delta_1d_pct_drop
from consequence.effect.effect_lower_than_close import min_price_future
from consequence.lib.ce_velocity_to_lower_than_signal_bar_close import velocity_to_lower_than_signal_bar_close
import pandas as pd
import plotly.express as px
from util.util import df_date_filter, df_date_index_mapping, PX_PERCENT_HIST
import numpy as np
import plotly.graph_objects as go

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
df = df_date_filter(df, 'date', '2018-05-16', '2022-05-16')
df.reset_index(inplace=True, drop=True)
date_idx_map = df_date_index_mapping(df)


signal = 'p_delta_1d_pct'
# threshold = -0.02
thres_list = np.arange(-0.02, 0.002, 0.001)
observe_range = 10

dfs = {}
for threshold in thres_list:
    effect_df = velocity_to_lower_than_signal_bar_close(df, date_idx_map, signal, threshold, observe_range)
    dfs[threshold] = effect_df
    
df = pd.concat(list(dfs.values()))

x_0p = dfs[-0.0009999999999999835]['val'].to_list()
x_0_3p = dfs[-0.0029999999999999853]['val'].to_list()
x_1p = dfs[-0.009999999999999992]['val'].to_list()
x_1_5p = dfs[-0.014999999999999996]['val'].to_list()
x_2p = dfs[-0.02]['val'].to_list()


fig = go.Figure()
fig.add_trace(go.Histogram(x=x_0p,name='0p',cumulative_enabled=True,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
# fig.add_trace(go.Histogram(x=x_0_3p,name='0_3p',cumulative_enabled=True,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
# fig.add_trace(go.Histogram(x=x_1p,name='1p',cumulative_enabled=True,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
# fig.add_trace(go.Histogram(x=x_1_5p,name='1_5p',cumulative_enabled=True,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
fig.add_trace(go.Histogram(x=x_2p,name='2p',cumulative_enabled=True,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
fig.show()

# fig = go.Figure()
# fig.add_trace(go.Histogram(x=x_1p,name='1p',cumulative_enabled=False,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
# fig.add_trace(go.Histogram(x=x_1_5p,name='1_5p',cumulative_enabled=False,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
# fig.add_trace(go.Histogram(x=x_2p,name='2p',cumulative_enabled=False,xbins=dict(size=0.001),histnorm=PX_PERCENT_HIST))
# fig.show()