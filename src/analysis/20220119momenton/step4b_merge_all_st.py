import pandas as pd
from util.util_file import get_all_csv_file_in_folder


# folder_in = 'D:/f_data/analysis/20220119_momenton/step3_filter_first_trade/'
folder_in = 'D:/f_data/analysis/20220119_momenton/step4_added_label/'
file_out = 'D:/f_data/analysis/20220119_momenton/merged_feature_label.csv'
files = get_all_csv_file_in_folder(folder_in)

    
cnt = 0
# print(len(files))
dfs = []
for file in files:
    file_name = file.split('/')[-1]
    ticker = file_name.split('.')[0]
    
    path_in = folder_in + ticker + '.csv'
    print(cnt, ticker)
#     path_out = f'{folder_out}/{ticker}.csv'
    df = pd.read_csv(path_in)
    df['ticker'] = ticker
    dfs.append(df)
#     df['label']=df.apply(lambda row : label(row['pnl_percent']), axis = 1)
    cnt += 1
    
df_merged = pd.concat(dfs)
df_merged.to_csv(file_out, index=False)
# print(df_merged)