
import pandas as pd
from util.general_ui import plot_candle_stick
from util.util import df_date_filter


st_path = 'D:/f_data/price_with_indicator/SPY_1D_fmt_idc.csv'
start_date = '2018-08-01'
end_date = '2022-04-08'

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
df = df_date_filter(df, 'date', start_date, end_date)


df_selected = df[df['p_delta_1d_pct'] < -0.02]
date_list = df_selected['date'].to_list()

plot_candle_stick(
    df=df,
    date_marker=date_list
)