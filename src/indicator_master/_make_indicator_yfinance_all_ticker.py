'''
Created on Jun 9, 2020

@author: leon
'''

from indicator_master.create_indicator_api_main import price_csv_append_indicator
from util import util
stock_ticker_folder="""D:/f_data/download_yfinance/"""


filepath_list=util.get_all_csv_file_path_from_folder(stock_ticker_folder)
print("found "+ str(len(filepath_list))+" ticker files")

input_file_path="D:/f_data/download_yfinance/"
output_file_path="D:/f_data/download_yfinance_with_indicator/"

cnt = 1
for file in filepath_list.keys():
    newfile = file[:-4] + '_with_indicator_20200609.csv'
    print(str(cnt) + " processing: "+file+" -> " + newfile)
    cnt = cnt + 1
    price_csv_append_indicator(
        input_file_path=input_file_path+file, 
        output_file_path=output_file_path+newfile, 
        start_time="1991-01-31 20:00:00", 
        end_time="2020-12-26 19:00:00",
        plot_chart=False
    )
    print(file + '  done')