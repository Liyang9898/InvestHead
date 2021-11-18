from batch_20201214.download_stock.api.api import api_download_ticker


ticker = 'FB'
start = '2020-01-01'
end = '2021-01-01'
path_out='D:/f_data/temp/bbbb.csv'
interval='1d'
api_download_ticker(ticker, start, end, path_out, interval)