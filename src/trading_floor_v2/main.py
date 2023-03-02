'''
Created on Mar 1, 2023

@author: spark
'''
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from trading_floor_v2.trade_analysis_lib import gen_ts_with_trades
from trading_floor_v2.trade_infra_lib import run_trading_strategy, \
    ACTION_ENTER, ACTION_EXIT, pair_enter_exit
from trading_floor_v2.trade_plot_lib import plot_trades
from util.general_ui import plot_candle_stick_generic
from util.util_pandas import df_to_dict
from util.util_time import df_filter_dy_date


# path_ticker = "C:/f_data/sector/indicator_day/XLF_1D_fmt_idc.csv"
path_ticker = "C:/f_data/price_with_indicator/BTC_1D_fmt_idc.csv"
path_trades = "C:/f_data/sector/debug2/trades.csv"
path_ts = "C:/f_data/sector/debug2/protafolio_time_series.csv"

'''
get initial ticker price
'''
start_date = '2020-01-01'
end_date = '2024-03-01'

df_ticker = pd.read_csv(path_ticker)
df_ticker = df_filter_dy_date(df_ticker,'date',start_date,end_date)

'''
run trades
'''
df_trades = run_trading_strategy(df_ticker)
df_trades.to_csv(path_trades, index=False)
# get_ts(df_trades)

'''
plot time series after trade
'''
ts_all = gen_ts_with_trades(df_ticker, df_trades, 'date', 'close', 1, True)
ts_all.to_csv(path_ts, index=False)
fig = px.line(ts_all, x="date", y="close", title='AUM time series')
fig.show()


'''
plot enter & exit
'''
img_path = "C:/f_data/sector/debug2/img.html"
plot_trades(df_ticker, df_trades, img_path)