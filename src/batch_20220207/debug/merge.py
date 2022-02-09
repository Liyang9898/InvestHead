from batch_20220207.batch_20220207_lib.constant import FEATURE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME
import pandas as pd
from util.util_file import get_all_csv_file_in_folder


raw_price_files = get_all_csv_file_in_folder(FEATURE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME)


def label_on_pnl(pnl_percent):
    if pnl_percent > 0:
        return True
    else:
        return False

dfs = []
for file in raw_price_files:
    df = pd.read_csv(file)
    dfs.append(df)
    
df_all = pd.concat(dfs)
df_all['l'] = df_all['50'] - df_all['90']
df_all['label']=df_all.apply(lambda row : label_on_pnl(row['l']), axis = 1)

gp = df_all.groupby('label').size()
print(gp)