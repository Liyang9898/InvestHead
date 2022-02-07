import pandas as pd
from util.util_file import get_all_csv_file_in_folder


# folder_in = 'D:/f_data/analysis/20220119_momenton/step3_filter_first_trade/'
folder_in = 'D:/f_data/analysis/20220119_momenton/step4_added_label/'
file_out = 'D:/f_data/analysis/20220119_momenton/merged_feature_label.csv'
files = get_all_csv_file_in_folder(folder_in)


feature_list = [
    'ema21_increase_rate_5bar', # helpful, distinction not large
    'ema21_increase_rate_10bar',  # helpful, distinction not large
    'ma50_increase_rate_5bar', # no correlation at all
    'ma50_increase_rate_10bar',
    'ma50_increase_rate_90bar', # the higher the more likely to lose # need to see some example, more reverse?
    
    'ema21_peak_over_x_days_40', # obviously useful
    'ma50_peak_over_x_days_40', # no correlation at all
    
    'v_ema21_2', # obviously useful
    'v_ema21_3', # obviously useful
]

col_list = feature_list + ['label']
    
    
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
    df = df[col_list].copy()
    dfs.append(df)
#     df['label']=df.apply(lambda row : label(row['pnl_percent']), axis = 1)
    cnt += 1
    
df_merged = pd.concat(dfs)
df_merged.to_csv(file_out, index=False)
# print(df_merged)