
from batch_20220207.batch_20220207_lib.constant import RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    FEATURE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME, gen_time_window, \
    WINDOW_SIZE, START_YEAR, END_YEAR, \
    IDC_TRADE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME
from batch_20220207.batch_20220207_lib.util_feature_threshold import merge_idc_trade_add_label, \
    compute_v_threshold_on_idc_trade_merged_data
import pandas as pd
from util.util_file import get_all_csv_file_in_folder


raw_price_files = get_all_csv_file_in_folder(INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME)
print(len(raw_price_files))

# trade
# RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME

#idc
# INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME
    

l = []
start_date = '2006-01-01'
end_date = '2022-01-01'
cnt = 0

for file_path in raw_price_files:
    tokens = file_path.split('/')
    file_name = tokens[len(tokens) - 1]
    ticker = file_name.split('.')[0]
    
    print(f'{cnt} Generating trades {ticker}')
    output_path_all_entry = f'{RAWS_TRADES_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}_all_entry.csv'

    # merge trade and indicator, add labeling
    df_idc = pd.read_csv(file_path)
    df_trade = pd.read_csv(output_path_all_entry)
    if len(df_idc) == 0 or len(df_trade) == 0:
        cnt += 1
        continue
    df_merge = merge_idc_trade_add_label(df_idc, df_trade)
    path_threshold = IDC_TRADE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME + ticker + '.csv'
    df_merge.to_csv(path_threshold, index=False)
    
    windows = gen_time_window(window_size=WINDOW_SIZE, start_year=START_YEAR, end_year=END_YEAR) 
    
    d = []
    for window in windows:
        s = window['start']
        e = window['end']
        

        df_merge_sub = df_merge.loc[(df_merge['entry_date'] >= s) & (df_merge['entry_date'] <= e)]
        df_merge_sub = df_merge_sub.copy()
        
        # compute threshold
        threshold = compute_v_threshold_on_idc_trade_merged_data(df_merge_sub, ticker)
        if threshold is None:
            continue
        threshold['start_date'] = s
        threshold['end_date'] = e
        d.append(threshold)
        
    df_threshold = pd.DataFrame(d)
    path_threshold = FEATURE_THRESHOLD_FOLDER_RUSSLL1000_OF_ALL_TIME + ticker + '.csv'
    df_threshold.to_csv(path_threshold, index=False)
    
    
#     if cnt > 7:
#         break
    cnt += 1



    