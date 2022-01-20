

from indicator_master.feature_set.fs20220119 import feature_set_20220119
import pandas as pd


path='D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/step3_add_indicator/ACA.csv'
path_out='D:/f_data/temp/ACA_test.csv'

df = pd.read_csv(path)
feature_set_20220119(df)
df.to_csv(path_out, index=False)