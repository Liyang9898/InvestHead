from util.util_file import get_all_csv_file_in_folder
import pandas as pd

# base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_no_take_profit/'
# 
# trade_folder = base_folder + 'step3_add_indicator/'
# indicator_folder = base_folder + 'step4_gen_trades/'
# trade_with_idc_folder = 'D:/f_data/analysis/20220116_ma_gap_influence/trade_with_idc/'
feature_label = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label/'
feature_label_merge = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label_merge.csv'


files = get_all_csv_file_in_folder(feature_label)


dfs = []
for file in files:
    print(file)
    df = pd.read_csv(file)
    dfs.append(df)
    
    
df_all = pd.concat(dfs)
df_all.to_csv(feature_label_merge, index=False)