from util.util_file import get_all_csv_file_in_folder
import pandas as pd


folder_in = 'D:/f_data/analysis/20220119_momenton/step2_join_trades/'
folder_out = 'D:/f_data/analysis/20220119_momenton/step3b_filter_idc_without_trade/'
files = get_all_csv_file_in_folder(folder_in)

cnt = 0
print(len(files))
for file in files:
    file_name = file.split('/')[-1]
    ticker = file_name.split('.')[0]
#     print(file_name)
    
    path_in = folder_in + ticker + '.csv'
    print(cnt, path_in)
    path_out = f'{folder_out}/{ticker}.csv'
    df = pd.read_csv(path_in)
    df2 = df[df['entry_date'].notnull()]
    print(len(df), len(df2))
    df2.to_csv(path_out, index=False)
    cnt += 1
