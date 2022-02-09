from indicator_master.feature_set.fs20220119 import feature_set_20220119
import pandas as pd
from util.util_file import get_all_csv_file_in_folder


base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_no_take_profit/'

sub_trades_path = 'D:/f_data/analysis/20220208_momenton/trades_split/'

idc_folder = base_folder + 'step3_add_indicator/'

files = get_all_csv_file_in_folder(sub_trades_path)

cnt = 0
print(len(files))
for file in files:
    file_name = file.split('/')[-1]
    ticker = file_name.split('.')[0]
    
    path_in = idc_folder + ticker + '.csv'
    print(cnt, path_in)
    path_out = f'D:/f_data/analysis/20220208_momenton/idc_with_feature/{ticker}.csv'
    df = pd.read_csv(path_in)
    feature_set_20220119(df)
    df.to_csv(path_out, index=False)
    cnt += 1
