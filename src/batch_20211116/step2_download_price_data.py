from api.api import api_download_ticker
from batch_20211116.batch_20211116_lib.constant import TICKERS_RUSSLL1000_OF_ALL_TIME, \
    TICKERS_PRICE_FOLDER_RUSSLL1000_OF_ALL_TIME
import pandas as pd


tickers_russell1000_df = pd.read_csv(TICKERS_RUSSLL1000_OF_ALL_TIME)
tickers_russell1000_all_time = tickers_russell1000_df['ticker'].to_list()
print(len(tickers_russell1000_all_time), 'tickers in russell 1000 all time')

start = '2006-01-01'
end = '2022-01-01'
interval = '1d'
cnt = 0

for ticker in tickers_russell1000_all_time:
    print(f'{cnt} Downloading {ticker}')
    path = f'{TICKERS_PRICE_FOLDER_RUSSLL1000_OF_ALL_TIME}{ticker}.csv'
    api_download_ticker(ticker, start, end, path, interval)
    cnt += 1