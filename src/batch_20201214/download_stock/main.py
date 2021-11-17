'''
Created on Mar 9, 2021

@author: leon
'''
import pandas as pd
from batch_20201214.download_stock.download_stock_lib import  download_format_2csv
from indicator_master.create_indicator_api_main import price_csv_append_indicator
def pickcolumn(file, path_out, input_column):
    df = pd.read_csv(
        file,
        sep=',',
        header=0,
        names=input_column
    )
    df.to_csv(
        path_out,
    )
    
ticker = 'spy'
start_time = '2021-02-01'
end_time = '2021-03-11'
path_out = 'D:/f_data/a.csv'
path_out2 = 'D:/f_data/a2.csv'
path_out3 = 'D:/f_data/a3.csv'


download_format_2csv(ticker, start_time, end_time, path_out)
input_column=['time', 'open','high','low','close','ma200','ma50','ema21','ema8']
pickcolumn(path_out, path_out2, input_column)



price_csv_append_indicator(
    input_file_path=path_out2, 
    output_file_path=path_out3,
    start_time="1991-01-31 20:00:00", 
    end_time="2021-03-11 19:00:00",
    plot_chart=True
)