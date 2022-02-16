import os

from api.api import api_gen_indicator
from batch_20220214.batch_20220214_lib.constant import TICKERS_PRICE_FOLDER_SNP500_OF_ALL_TIME, indicator_path, START_DATE, END_DATE
from util.util_file import get_all_csv_file_in_folder


raw_price_files = get_all_csv_file_in_folder(TICKERS_PRICE_FOLDER_SNP500_OF_ALL_TIME)
print(len(raw_price_files))


start_date = START_DATE
end_date = END_DATE
cnt = 0

for file_path in raw_price_files:
    tokens = file_path.split('/')
    file_name = tokens[len(tokens) - 1]
    ticker = file_name.split('.')[0]
    
    print(f'{cnt} Adding indicator {ticker}')
    output_path = indicator_path(ticker)
    
    if os.path.isfile(output_path):
        print('already done, skip')
    else:
        api_gen_indicator(file_path, output_path, start_date, end_date)

    cnt += 1