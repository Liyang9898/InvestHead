from api.api import api_gen_indicator
from batch_20211116.batch_20211116_lib.constant import TICKERS_PRICE_FOLDER_RUSSLL1000_OF_ALL_TIME, \
    INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME
from util.util_file import get_all_csv_file_in_folder
import os

raw_price_files = get_all_csv_file_in_folder(TICKERS_PRICE_FOLDER_RUSSLL1000_OF_ALL_TIME)
print(len(raw_price_files))


start_date = '2006-01-01'
end_date = '2022-01-01'
cnt = 0

for file_path in raw_price_files:
    tokens = file_path.split('/')
    file_name = tokens[len(tokens) - 1]
    ticker = file_name.split('.')[0]
    
    print(f'{cnt} Adding indicator {ticker}')
    output_path = f'{INDICATOR_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}.csv'
    
    if os.path.isfile(output_path):
        print('already done, skip')
    else:
        api_gen_indicator(file_path, output_path, start_date, end_date)

    cnt += 1