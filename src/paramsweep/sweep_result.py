
# from numpy.random.entropy import np
import numpy as np
import pandas as pd
from paramsweep.ui import single_heat_map
from paramsweep.util import gen_date_rage_list


# from paramsweep.param_sweep import stop_gain_list, stop_loss_list, ds_range_list
path_out_1 = """D:/f_data/param_sweep_1m.csv"""
path_out_2 = """D:/f_data/param_sweep_5m.csv"""
path_out_3 = """D:/f_data/param_sweep_5m_2008_2020.csv"""
def load_df():
    path = path_out_3
    df = pd.read_csv(
        path,
        sep=',',
        header=1,
        names=[
            'start_time',
            'end_time',
            'opentop',
            'stop_loss', 
            'stop_gain',
            'avg_monthly_gain',
            'win_rate',
            'win_rate_exclude_neutral',
            'days',
            'win',
            'lose', 
            'neutual',
            'pnl',
            'daily_balance_10_contract',
            'pnl_ma_20_avg',
            'rate_ma_20_avg',
            'pnl_ma_20_positive_rate',
            'rate_ma_20_positive_rate'
        ]
    )
    return df
   
df = load_df()
print('load sweep result')
print(df)
 
rank_cols = [
    'avg_monthly_gain',
    'win_rate_exclude_neutral',
    'pnl_ma_20_positive_rate',
    'rate_ma_20_positive_rate'
]
 
 
# threshold = 0.25
stop_gain_list = np.arange(1,5,0.5)
stop_loss_list = np.arange(1,5,0.5)
ds_range_list = gen_date_rage_list('2008-01-01','2020-01-01', 90)
 
 
stop_gain_list = stop_gain_list
stop_loss_list = stop_loss_list
opentop=True
ds_range_list = ds_range_list
rank_col=1
rank_col='avg_monthly_gain'
for ds in ds_range_list:
    start = ds['s']
    title = rank_col + '   from: '+ds['s'] + ' to: '+ds['e']
    df_sub = df[(df['start_time'] == start) & (df['opentop'] == opentop)]
    single_heat_map(df_sub, opentop,stop_gain_list,stop_loss_list, rank_col,title)
 
