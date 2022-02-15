from batch_20220207.batch_20220207_lib.constant import IDC_TRADE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    BASE_PATH
import pandas as pd
from util.util_file import get_all_csv_file_in_folder


def label_on_pnl(pnl_percent):
    if pnl_percent > 0:
        return True
    else:
        return False

# add label, extract col
raw_price_files = get_all_csv_file_in_folder(IDC_TRADE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME)

dfs = []
for file in raw_price_files:

    df = pd.read_csv(file)
    print(file, len(df))
#     print(df)
    df['label']=df.apply(lambda row : label_on_pnl(row['pnl_percent']), axis = 1)
    df = df[['v_ema21_3','label']].copy()
#     print(df)
    dfs.append(df)

df_all = pd.concat(dfs)
path_all = BASE_PATH + 'all_idc_trade.csv'
df_all.to_csv(path_all, index=False)