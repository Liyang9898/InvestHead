
import os

from api.api import api_gen_trades
from batch_20220310.batch_20220310_lib.constant import RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME, \
    INDICATOR_FOLDER_COLLECTION_OF_ALL_TIME, START_DATE, END_DATE
import pandas as pd
from strategy_lib.stratage_param import strat_param_swing_2150in_2150out_ma_gap_no_take_profit
from util.util_file import get_all_csv_file_in_folder


raw_price_files = get_all_csv_file_in_folder(INDICATOR_FOLDER_COLLECTION_OF_ALL_TIME)
print(len(raw_price_files))


start_date = START_DATE
end_date = END_DATE
cnt = 0

for file_path in raw_price_files:
    tokens = file_path.split('/')
    file_name = tokens[len(tokens) - 1]
    ticker = file_name.split('.')[0]
    
    print(f'{cnt} Generating trades {ticker}')
    output_path_all_entry = f'{RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME}{ticker}_all_entry.csv'
    output_path_consecutive = f'{RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME}{ticker}_consecutive.csv'
    
    
    
    if os.path.isfile(output_path_all_entry) and os.path.isfile(output_path_consecutive):
        try:
            pd.read_csv(output_path_all_entry)
            print('already done, skip')
        except:
            print('pandas can not be opened')
    else:
        api_gen_trades(
            ticker=file_name,
            start_date=start_date, 
            end_date=end_date, 
            strategy=strat_param_swing_2150in_2150out_ma_gap_no_take_profit,
            indicator_file_path=file_path, 
            trade_result_all_entry_path=output_path_all_entry, 
            trade_result_consecutive_entry_path=output_path_consecutive, 
        )

    cnt += 1













