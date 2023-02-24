'''
Created on Feb 24, 2023

@author: spark
'''
# from datetime import datetime, timedelta

import pandas as pd


# import plotly.express as px
# from util.general_ui import plot_trades_simple_base
# from util.util_time import df_filter_dy_date 
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
    sector_raw_path = "C:/f_data/sector/raw/BATS_{ticker}, 1W.csv".format(ticker=ticker)
    sector_clean_path = "C:/f_data/sector/clean/{ticker}_1W_fmt.csv".format(ticker=ticker)
    print(sector_raw_path)
    sector_df = pd.read_csv(sector_raw_path)
    sector_df_trimmed = sector_df.iloc[:, [0,1,2,3,4,   5,6,  7,9,11,13]]
    dict_col = {
        'Volume MA': 'volume_ma',
        'MA': 'ma200',
        'MA.1': 'ma50',
        'EMA': 'ema21',
        'EMA.1': 'ema8',
    }
    sector_df_trimmed=sector_df_trimmed.copy()


    sector_df_trimmed.rename(columns=dict_col,inplace=True)
    sector_df_trimmed.to_csv(sector_clean_path, index=False)

    
    
