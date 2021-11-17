'''
Created on Jun 16, 2020

@author: leon
'''
import pandas as pd
from indicator_master.constant import trade_summary_interface
def valid_strategy_param_exist(sweep_file_path, total_rate, lose_rate):
    path = sweep_file_path
    df = pd.read_csv(
        path,
        sep=',',
        header=0,
        names=trade_summary_interface,
    )
    for i in range(0, len(df)):
        pnl_p = df.loc[i, 'win_pnl_p'] - df.loc[i, 'lose_pnl_p']
        if df.loc[i, 'total_rate'] > total_rate and df.loc[i, 'lose_rate'] < lose_rate and pnl_p > 0:
            return True
    return False