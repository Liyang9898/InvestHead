import os

from batch_20220310.batch_20220310_lib.constant import RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME, HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME, HIGH_PERF_TICKER_FOLDER
import pandas as pd
from util.util_file import get_all_csv_file_in_folder

"""
this process get the sub set of trades which is in high perf pool 
use ticker list in step 6 to filter step 5, so step 7 is a sub set of step 5's result
"""

path_trades = RAWS_TRADES_FOLDER_COLLECTION_OF_ALL_TIME
path_filtered_trades = HIGH_PERF_TRADES_FOLDER_COLLECTION_OF_ALL_TIME


def ticker_elible_end_year():
    """
    input: high perf ticker pool
    output: dict<ticker, list<end year>>
    """
    raw_price_files = get_all_csv_file_in_folder(HIGH_PERF_TICKER_FOLDER)
    dfs = []
    for file_path in raw_price_files:
        file_name = file_path.split('/')[-1].replace('.csv','')
        tokens = file_name.split('_')
        tokens_small = tokens[1].split('-')
        df = pd.read_csv(file_path)
        df['end_year'] = tokens_small[0]
        df = df[['ticker','end_year']]
        df = df.copy()
        dfs.append(df)
    all_df = pd.concat(dfs)
    gp = all_df.groupby('ticker').agg(list)
    gp_dict = gp.to_dict('index')
    res = {k: v['end_year'] for k, v in gp_dict.items()}
    return res


elible_end_year = ticker_elible_end_year()
for k, v in elible_end_year.items():
    print(k,v)


cnt = 1
for file in os.listdir(path_trades):
    if file.endswith("_all_entry.csv"):
        file_path = path_trades + file 
        ticker = file.split('_')[0]
        df = pd.read_csv(file_path)
        df['end_year'] = df['entry_ts'].str[:4]
        if ticker not in elible_end_year:
            continue
        end_years = elible_end_year[ticker]
        boolean_series = df.end_year.isin(end_years)
        df_filtered = df[boolean_series]
        print(ticker + ' all entry trade cnt, before:' + str(len(df)) + ' after:' + str(len(df_filtered)))
        df_filtered.to_csv(path_filtered_trades + file)
