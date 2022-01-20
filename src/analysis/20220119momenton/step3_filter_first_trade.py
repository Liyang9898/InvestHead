import pandas as pd
from util.util_file import get_all_csv_file_in_folder


def get_first_trade_date_20220120(df):
    trade_selected = False
    selected_trades = []
    
    for i in range(0, len(df)):
        ema21 = df.loc[i, 'ema21']
        ma50 = df.loc[i, 'ma50']
        if ema21 > ma50:
            # should select trades
            if not trade_selected:
                # if this is a trade capture, 
                if df.loc[i, 'complete'] == True:

                    selected_trades.append(df.loc[i, 'date'])
                    trade_selected = True
        else:
            trade_selected = False
         
    return selected_trades


def get_first_trade_df_20220120(df, first_trade):
    df = df[df['date'].isin(first_trade)]
    df = df.copy()
    return df


def get_first_trade_csv(path_in, path_out):
    df = pd.read_csv(path_in)
    first_trade = get_first_trade_date_20220120(df)
    first_trade_df = get_first_trade_df_20220120(df, first_trade)
    print(len(first_trade_df))
    first_trade_df.to_csv(path_out)


folder_in = 'D:/f_data/analysis/20220119_momenton/step2_join_trades/'
folder_out = 'D:/f_data/analysis/20220119_momenton/step3_filter_first_trade/'
files = get_all_csv_file_in_folder(folder_in)

cnt = 0
print(len(files))
for file in files:
    file_name = file.split('/')[-1]
    ticker = file_name.split('.')[0]
    
    path_in = folder_in + ticker + '.csv'
    print(cnt, path_in)
    path_out = f'{folder_out}/{ticker}.csv'
    df = pd.read_csv(path_in)
    get_first_trade_csv(path_in, path_out)
    cnt += 1
