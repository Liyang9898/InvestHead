from price_asset_master.lib.api.api import api_download_ticker


ticker = 'fb'
start = '2020-01-01'
end = '2021-01-01'
path_out='D:/f_data/temp/bbbbc.csv'
interval='1d'
api_download_ticker(ticker, start, end, path_out, interval)