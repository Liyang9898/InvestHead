from version_master.version import swing_set_20220103
import pandas as pd


def get_stock_ranking():
    df = pd.read_csv(swing_set_20220103)
    df = df[['ticker', 'annual_avg_return']]
    dic = {}
    for i in range(0, len(df)):
        dic[df.loc[i, 'ticker']] = df.loc[i, 'annual_avg_return']
    return dic