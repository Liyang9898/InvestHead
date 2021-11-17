from cmath import nan

import pandas as pd
from trading_floor.TradeInterface import Trade, TradeBundle
from util.general_ui import plot_candle_stick, plot_trades_simple, \
    plot_trades_ma_only
from util.util_pandas import df_unixtime_filter
from util.util_time import date_formatter_1, \
    time_format_slash_string_to_unixtime
from version_master.version import (
    swing_set1,
    price_asset_path_base,
    indicator_asset_path_base,
    op_close
)


indicator_version = '20210704_swing_only'
image_folder = 'win_holding_period_only'
holding_period_only = True
time_offset = 30*24*60*60

df_close = pd.read_csv(op_close)
df_close.dropna(subset=['close date'], inplace=True)

df_close_lose=df_close[df_close['exit_price']<df_close['enter_price']]
df_close_win=df_close[df_close['exit_price']>df_close['enter_price']]
print(len(df_close_lose), len(df_close_win))

dict_close = df_close_win.to_dict('records')
cnt = 1
start = 1
for trade in dict_close:
    if trade['close date'] == nan:
        continue
    ticker = trade['ticker'].upper()
    print(ticker, trade)
    enter = {date_formatter_1(trade['date']): trade['enter_price']}
    exit = {date_formatter_1(trade['close date']): trade['exit_price']}
    
    cnt = cnt + 1
    
#     if cnt >= start and cnt < start + 3:
    folder_path = indicator_asset_path_base + indicator_version + '/' + ticker + '.csv'
    price_with_indicator = pd.read_csv(folder_path)
    
    if holding_period_only:
        unix_s = time_format_slash_string_to_unixtime(trade['date']) -time_offset
        unix_e = time_format_slash_string_to_unixtime(trade['close date']) +time_offset
        price_with_indicator = df_unixtime_filter(price_with_indicator, 'time', unix_s, unix_e)

    
    
    plot_trades_simple(price_with_indicator, enters=enter, exits=exit, ticker=ticker, is_image=True, image_folder=image_folder)
#     plot_trades_ma_only(price_with_indicator, enters=enter, exits=exit, ticker=ticker, is_image=True, image_folder=image_folder)
#     else:
#         continue

