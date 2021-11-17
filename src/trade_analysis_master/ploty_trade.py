import pandas as pd
from trading_floor.TradeInterface import genTradingBundleFromCSV
from trading_floor.TradePlot import plot_trades
from version_master.version import (
    indicator_20210408,
    t_20210408_myswing
)




def plot_trade(ticker):
    path_inc = indicator_20210408 + ticker + '_downloaded_raw.csv'
    path_trade = t_20210408_myswing + 'detail/' + ticker + '_all_entry.csv'
    print(path_inc)
    print(path_trade)
    
    trade_bundle_all_entry = genTradingBundleFromCSV(path_trade)
    df_inc = pd.read_csv(path_inc)
    plot_trades(df_inc, '', trade_bundle_all_entry, entry_only=False,ticker=ticker)
    
    
ticker = 'PAYC'
plot_trade(ticker)