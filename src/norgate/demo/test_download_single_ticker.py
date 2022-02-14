from norgate.ticker_price_downloader import pull_ticker_price_locally_norgate

path_out = 'D:/f_data/temp/norgate/test1.csv'
path_out2 = 'D:/f_data/temp/norgate/test2.csv'
df = pull_ticker_price_locally_norgate('FB', '2022-01-01', '2022-02-01', path_out)
df = pull_ticker_price_locally_norgate('V', '2022-01-01', '2022-02-01', path_out2)
# print(df.columns)
# print(df)