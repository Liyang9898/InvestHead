from version_master.version import (
#     t_20210321_myswing,
#     indicator_20210404,
    feature_engineering,
    feature_engineering_by_ticker
)
import pandas as pd
# import random

df = pd.read_csv(feature_engineering+'features.csv')


def split_by_ticker(df,to_csv=False):
    
    # finish off index
    ticker_index = {} # key-ticker, value-list of index
    for idx in range(0,len(df)):
        ticker = df.loc[idx, 'ticker']
        if ticker not in ticker_index.keys():
            ticker_index[ticker] = []
        ticker_index[ticker].append(idx)

    # split df by ticker
    dfs = {}
    cnt = 0
    for ticker in ticker_index.keys():
        idxs=ticker_index[ticker]
        sub = df.iloc[idxs, :]
        print(ticker, len(sub))
        cnt += len(sub)
        if to_csv:
            path = feature_engineering_by_ticker+'features_' + ticker + '.csv'
            sub.to_csv(path, index=False)
        dfs[ticker] = sub.copy()
    
    assert cnt == len(df)
    return dfs



# print(res)