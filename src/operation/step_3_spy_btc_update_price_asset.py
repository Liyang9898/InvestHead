
import pandas as pd
from price_asset_master.lib.refresh_price_asset_add_indicator import refresh_price_asset_add_indicator
from util.util_finance_chart import plot_candle_stick_with_trace
from datetime import datetime

from operation.lib.trade_lib import batch_tradable
import pandas as pd
from strategy_lib.stratage_param import strat_param_20211006_ma_max_drawdown_cut, \
    strat_param_20211006_ma_macd
from util.util_finance_chart import plot_candle_stick_with_trace
from util.util_time import get_today_date_str


spy_asset_loc = refresh_price_asset_add_indicator(
    time_window=365*2, 
    ticker_list=['spy'], 
    op_path_base='D:/f_data/operation_spy/', 
    interval='1wk'
)


btc_asset_loc = refresh_price_asset_add_indicator(
    time_window=180, 
    ticker_list=['BTC-USD'], 
    op_path_base='D:/f_data/operation_btc/', 
    interval='1d'
)


# df_spy = pd.read_csv(f'{spy_asset_loc}/indicator/spy_downloaded_raw.csv')
# plot_candle_stick_with_trace(
#     df_spy, 
#     traces={}

print(spy_asset_loc,btc_asset_loc)
print('===================================================Price update DONE=================================================================')
# btc_enterabe()
# spy_enterable()
# )
# 
# df_btc = pd.read_csv(f'{btc_asset_loc}/indicator/BTC-USD_downloaded_raw.csv')
# plot_candle_stick_with_trace(
#     df_btc, 
#     traces={}
# )



