from api.api import api_download_ticker
from batch_20220214.batch_20220214_lib.constant import TICKERS_SNP500_OF_ALL_TIME, \
    TICKERS_PRICE_FOLDER_SNP500_OF_ALL_TIME, START_DATE, END_DATE
import pandas as pd


tickers_russell1000_df = pd.read_csv(TICKERS_SNP500_OF_ALL_TIME)
tickers_russell1000_all_time = tickers_russell1000_df['ticker'].to_list()
print(len(tickers_russell1000_all_time), 'tickers in russell 1000 all time')

start = START_DATE
end = END_DATE
interval = '1d'
cnt = 0

for ticker in tickers_russell1000_all_time:
    print(f'{cnt} Downloading {ticker}')
    path = f'{TICKERS_PRICE_FOLDER_SNP500_OF_ALL_TIME}{ticker}.csv'
    api_download_ticker(ticker, start, end, path, interval, True)
    cnt += 1