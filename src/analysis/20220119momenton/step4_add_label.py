import pandas as pd
from util.util_file import get_all_csv_file_in_folder


folder_in = 'D:/f_data/analysis/20220119_momenton/step3b_filter_idc_without_trade/'
folder_out = 'D:/f_data/analysis/20220119_momenton/step4_added_label/'
files = get_all_csv_file_in_folder(folder_in)


def label(pnl_percent):
    if pnl_percent > 0:
        return True
    else:
        return False
    

cnt = 0
# print(len(files))
for file in files:
    file_name = file.split('/')[-1]
    ticker = file_name.split('.')[0]
    
    path_in = folder_in + ticker + '.csv'
    print(cnt, ticker)
    path_out = f'{folder_out}/{ticker}.csv'
    df = pd.read_csv(path_in)
    df['label']=df.apply(lambda row : label(row['pnl_percent']), axis = 1)
    df.to_csv(path_out, index=False)

    cnt += 1
