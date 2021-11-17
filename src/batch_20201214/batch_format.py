'''
Created on Dec 14, 2020

@author: leon
'''


from batch_20201214.format_lib.lib import batch_format
folder_path_raw_downloaded = "D:/f_data/sweep_20201214/raw_stock_download_20210106/"
folder_path_raw_price_formated = "D:/f_data/sweep_20201214/format_stock_20210106/"


batch_format(folder_path_raw_downloaded, folder_path_raw_price_formated)