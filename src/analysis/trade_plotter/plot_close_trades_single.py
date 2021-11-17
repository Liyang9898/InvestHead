from cmath import nan

import pandas as pd
from trading_floor.TradeInterface import Trade, TradeBundle
from util.general_ui import plot_candle_stick, plot_trades_simple
from util.util_time import date_formatter_1
from version_master.version import (
    swing_set1,
    price_asset_path_base,
    indicator_asset_path_base,
    op_close
)


indicator_version = '20210704_swing_only'
image_folder = 'temp'
ticker = 'CPRT' # must be upper case
enter_date = '5/24/2021'

df_close = pd.read_csv(op_close)


df_close = df_close[df_close['ticker']==ticker.lower()]
df_close = df_close[df_close['date']==enter_date]
dict_close = df_close.to_dict('records')
trade = dict_close[0]
print(trade)
ticker = trade['ticker'].upper()
enter = {date_formatter_1(trade['date']): trade['enter_price']}
exit = {date_formatter_1(trade['close date']): trade['exit_price']}
print(ticker, enter, exit, trade)

folder_path = indicator_asset_path_base + indicator_version + '/' + ticker + '.csv'
price_with_indicator = pd.read_csv(folder_path)
plot_trades_simple(price_with_indicator, enters=enter, exits=exit, ticker=ticker, is_image=True, image_folder=image_folder)


