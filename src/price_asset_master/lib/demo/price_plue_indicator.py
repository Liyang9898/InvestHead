from batch_20201214.download_stock.download_stock_lib import download_stock
import pandas as pd
from price_asset_master.lib.refresh_price_asset_add_indicator import refresh_price_asset_add_indicator
from util.util_finance_chart import plot_candle_stick_with_trace


time_window=365*5
ticker_list = ['spy', 'iwf', 'xlk', 'xlf', 'fb', 'amzn', 'goog']

op_path_base = 'D:/f_data/operation_test/'
interval = '1d'
# interval = '1wk'

path_base = refresh_price_asset_add_indicator(time_window, ticker_list, op_path_base, interval)
print(path_base)
path='D:/f_data/operation_spy/2021-10-10/indicator/spy_downloaded_raw.csv'
df = pd.read_csv(path)


plot_candle_stick_with_trace(
    df, 
    traces={}
)