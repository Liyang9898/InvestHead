from util.util_file import get_all_csv_file_in_folder
import pandas as pd

base_folder = 'D:/f_data/batch_20211116_strat_param_swing_2150in_2150out_ma_gap_4p_profit/'

trade_folder = base_folder + 'step3_add_indicator/'
indicator_folder = base_folder + 'step4_gen_trades/'
trade_with_idc_folder = 'D:/f_data/analysis/20220116_ma_gap_influence/trade_with_idc/'
feature_label = 'D:/f_data/analysis/20220116_ma_gap_influence/feature_label/'


def label(pnl_percent):
    if pnl_percent > 0:
        return True
    else:
        return False


def feature_ma21_50_pct_gap_4p(ma21_50_pct_gap):
    if ma21_50_pct_gap > 0.04:
        return 1
    else:
        return -1


files = get_all_csv_file_in_folder(trade_with_idc_folder)
feature_list = ['ma21_50_pct_gap', 'ma21_50_pct_gap_4p', 'label']


for file in files:
    file_name = file.split('/')[-1]
    print(file_name)
    df = pd.read_csv(file)
    df['ma21_50_pct_gap'] = df['ema21'] / df['ma50'] - 1
    df['label']=df.apply(lambda row : label(row['pnl_percent']), axis = 1)
    df['ma21_50_pct_gap_4p']=df.apply(lambda row : feature_ma21_50_pct_gap_4p(row['ma21_50_pct_gap']), axis = 1)
    df = df[feature_list]
    df.to_csv(feature_label+file_name, index=False)

