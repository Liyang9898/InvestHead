from api.api import api_download_ticker
from batch_20220310.batch_20220310_lib.constant import TICKERS_COLLECTION_OF_ALL_TIME, \
    TICKERS_PRICE_FOLDER_COLLECTION_OF_ALL_TIME, START_DATE, END_DATE
import pandas as pd


tickers_df = pd.read_csv(TICKERS_COLLECTION_OF_ALL_TIME)
tickers_all_time = tickers_df['ticker'].to_list()
print(len(tickers_all_time), 'tickers in russell 1000 all time')

start = START_DATE
end = END_DATE
interval = '1d'
cnt = 0

for ticker in tickers_all_time:
    print(f'{cnt} Downloading {ticker}')
    path = f'{TICKERS_PRICE_FOLDER_COLLECTION_OF_ALL_TIME}{ticker}.csv'
    api_download_ticker(ticker, start, end, path, interval, True)
    cnt += 1