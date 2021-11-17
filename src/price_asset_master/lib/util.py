import pandas as pd

def csv_to_ticker_list(ticker_list_csv_path): 
    print('processing: ticker list')
    df = pd.read_csv(ticker_list_csv_path)
    ticker_list = df['ticker'].to_list()
    return ticker_list