'''
Created on Jul 13, 2020

@author: leon
'''
from global_constant.constant import folder_path_trade_ml_sample,trade_feature
import pandas as pd
from trading_floor.TradePlot import label_distribution_on_feature,distribution_on_feature


    
path='D:/f_data/trade_ml_sample/BTC_4H_fmt_ml_sample.csv'
df = pd.read_csv(
    path,
    sep=',',
    header=0,
    names=trade_feature
)
print(df)
label_distribution_on_feature(df, 'ema_8_v_yesterday')
label_distribution_on_feature(df, 'ema_21_v_yesterday')
label_distribution_on_feature(df, 'ema_8_21_gap_yesterday')
label_distribution_on_feature(df, 'ema_8_strict_sequence_yesterday')
label_distribution_on_feature(df, 'pnl_p_per_trade')
# label_distribution_on_feature(df, 'entry_time')
# distribution_on_feature(df, 'entry_time')
