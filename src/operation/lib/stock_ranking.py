from version_master.version import swing_set_2019_2022
import pandas as pd


def get_stock_ranking():
    df = pd.read_csv(swing_set_2019_2022)
    df = df[['ticker', 'win_lose_pnl_ratio']]
    dic = {}
    for i in range(0, len(df)):
        dic[df.loc[i, 'ticker']] = df.loc[i, 'win_lose_pnl_ratio']
    return dic