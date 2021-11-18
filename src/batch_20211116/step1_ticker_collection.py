from batch_20211116.batch_20211116_lib.constant import TICKERS_RUSSLL1000_OF_ALL_TIME
import pandas as pd


path = 'D:/f_data/external_data_source/snapshot_version/russell1000_formatted_yearly.csv'
df = pd.read_csv(path)
ticker_col = df['ticker'].to_list()


tickers_of_all_time = []
for x in ticker_col:
    tokens = x.split('|')
    for t in tokens:
        if t not in tickers_of_all_time:
            tickers_of_all_time.append(t)
            
set_list = set(tickers_of_all_time)            
assert len(set_list) == len(tickers_of_all_time)

d = {'ticker': tickers_of_all_time}
df_ticker_of_all_time = pd.DataFrame(data=d)
print(df_ticker_of_all_time)
df_ticker_of_all_time.to_csv(TICKERS_RUSSLL1000_OF_ALL_TIME, index=False)