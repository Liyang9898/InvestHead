from datetime import datetime, timedelta
import os

from batch_20201214.util_for_batch.batch_util import get_all_files
from feature_engineering.lib.feature import gen_feature_on_trade_entry, \
    gen_feature_on_entire_trade_batch
from feature_engineering.lib.join_trade_indicator import join_trade_indicator_df
from indicator_master.indicator_compute_lib import tsfilter
import pandas as pd
import plotly.express as px
from version_master.version import (
    t_20210321_myswing,
    indicator_20210404,
    feature_engineering
)


def batch_feature_gen(trade_folder, indicator_folder):
    output_path=feature_engineering+'features.csv'

    files = get_all_files(trade_folder+'detail')
    tickers = list(files.keys())
#     tickers=['AAPL']
    print(tickers)
    dfs = []
    
    for ticker in tickers:
        print('gen_feature:', ticker)

        # read indicator and trade 
        # get trade
        trade_path = trade_folder + 'detail/' + ticker + '_all_entry.csv'
        df_trades = pd.read_csv(trade_path)
        
        # get indicator
        indicator_path = indicator_folder + '/' + ticker + '_downloaded_raw.csv'
        df_indicator = pd.read_csv(indicator_path)
        
        # generate feature
        # join trade with feature
        trade_entry_indicator_df = join_trade_indicator_df(ticker, df_trades, df_indicator)
        # feature based on entry indicator
        trades_with_entry_day_feature=gen_feature_on_trade_entry(trade_entry_indicator_df)
        # feature based on all price information during the holding
        feature_df=gen_feature_on_entire_trade_batch(
            ticker, 
            trades_with_entry_day_feature, 
            df_indicator 
        )
        
        dfs.append(feature_df)

    df_merged = pd.concat(dfs)    
    df_merged.to_csv(output_path, index=False)


def main():
    trade_folder = t_20210321_myswing
    indicator_folder = indicator_20210404
    batch_feature_gen(trade_folder, indicator_folder)


main()