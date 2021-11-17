from indicator_master.create_indicator_api_main import price_csv_append_indicator
from util.util_file import get_all_csv_file_in_folder
from version_master.version import (
    indicator_asset_path_base
)
from datetime import date
import os
import shutil


def batch_gen_indicator(price_file_path, indicator_version, start_time, end_time):
    folder_path = indicator_asset_path_base + indicator_version + '/'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path) 
    
    price_files = get_all_csv_file_in_folder(price_file_path)
    cnt = 1
    
    for price_file in price_files:
        tokens = price_file.split('/')
        filename = tokens[len(tokens)-1]
        ticker = filename.split('_')[0]
        output= folder_path + ticker + '.csv'
        print(cnt, " processing indicator:",ticker)
        price_csv_append_indicator(
            input_file_path=price_file, 
            output_file_path=output,
            start_time=start_time, 
            end_time=end_time,
            plot_chart=False
        )
        cnt = cnt + 1
