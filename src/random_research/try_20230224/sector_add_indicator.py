from api.api import api_gen_indicator
import pandas as pd


tickers = []

path = 'C:/f_data/sector/spy_sector_history.csv'
df = pd.read_csv(path)
print(df)

record = df.to_dict('records')
for r in record:
    print(r)
    tickers.append(r['ticker'])
    
print(tickers)

for ticker in tickers:
    sector_clean_path = "C:/f_data/sector/clean/{ticker}_1W_fmt.csv".format(ticker=ticker)
    sector_idc_path = "C:/f_data/sector/indicator/{ticker}_1W_fmt_idc.csv".format(ticker=ticker)
    # print(sector_clean_path)
    df = pd.read_csv(sector_clean_path)
    # print(df)
    
    start_date = '1990-01-01'
    end_date = '2024-01-01'
    
    api_gen_indicator(sector_clean_path, sector_idc_path, start_date, end_date)